import csv
import os
import shutil
import requests
import time
import fnmatch
import sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from queue import Queue
from IPython.display import display, HTML
import time
from multiprocessing.pool import ThreadPool
import threading
import pickle
import json
from reppy.robots import Robots
def pp(obj):
    print(json.dumps(obj, indent=2))

class CSVInputError(Exception):
    pass

class InputError(Exception):
    pass

class WebCrawler:
    '''
    Can be initialized with a csv file containing one 2 or 3 length line OR
        with kwargs
    Params: seed, num_pages, domain
    '''
    def __init__(self, num_pages=10, threaded=False, process_robot=False):
        self.threaded = threaded
        self.num_pages = num_pages
        self.seed = 'http://www.nba.com/'
        self.domain = 'www.nba.com'
        self.crawl_delay = 0.5
        self.robots_url = f'{self.seed}/robots.txt'

        num_pages = self.validate_input(num_pages)


        self.repo_files = {}
        self.file_count = 0
        self.main_link_queue = set()
        self.domain_dict = {}
        self.visited_robots = set()


        self._process_robot(process_robot)


        self.initialize_repo()
        self.initialize_seed()
        self.process_main_link_queue()

    def process_sitemap(self, sitemap):
        urls = []
        sr = requests.get(sitemap)
        # time.sleep(1)
        sr.encoding = 'utf-8'
        soup = BeautifulSoup(sr.text)
        sitemapTags = soup.find_all("sitemap")
        if sitemapTags:
            for sitemap in sitemapTags:
                self.sitemaps.append(sitemap.findNext('loc').text)
        else:
            _urls = soup.find_all('url')
            for url in _urls:
                self.main_link_queue.add(url.findNext('loc').text)
        time.sleep(self.crawl_delay)

    def pickle_initial_main_link_queue(self):
        with open('pickled_main_link_queue.pkl', 'wb') as f:
            pickle.dump(self.main_link_queue, f)

    def unpickle_initial_main_link_queue(self):
        with open('pickled_main_link_queue.pkl', 'rb') as f:
            self.main_link_queue |= pickle.load(f)

    def _process_robot(self, process_robot):
        r = Robots.fetch(self.robots_url)
        self.agent = r.agent('*')
        if process_robot:
            self.sitemaps = list(r.sitemaps)
            self.sitemap_urls = []
            while(self.sitemaps):
                s = self.sitemaps.pop(0)
                self.process_sitemap(s)
            self.pickle_initial_main_link_queue()
        else:
            self.unpickle_initial_main_link_queue()


    def validate_input(self, num_pages):
        '''
        Validates
            that num_pages is int (and coerces it),
        '''
        try:
            num_pages = int(num_pages)
        except ValueError as e:
            raise InputError('num_pages input is invalid. Must be coercible to int')

        return num_pages

    def initialize_repo(self):
        '''
        If repository exists from previous run, it is deleted
        Creates repository
        '''
        st = time.time()
        self.repo = 'repository'
        if os.path.isdir(self.repo):
            shutil.rmtree(self.repo)
        os.mkdir(self.repo)
        e = time.time() - st
        # print(f'initialize_repo took {e}')

    def initialize_seed(self):
        '''
        Calls process url on seed url
        '''
        st = time.time()
        self.process_url(self.seed)
        e = time.time() - st
        # print(f'initialize_seed took {e}')

    def process_url(self, url):
        '''
        Checks if a robot exists for url
        Checks if the url is in the domain input
        Gets url and adds file to repository
        Finds links from file and adds them to main_link_queue
        '''
        st = time.time()
        # crawl_delay = self.check_for_robot(url)
        parsed_url = urlparse(url)
        add_to_repo = self.check_domain(parsed_url.netloc)
        # print(add_to_repo)
        if add_to_repo and self.agent.allowed(url):
            time.sleep(self.crawl_delay)
            added = self.add_file_to_repo(url)
            # print(added)
            if added:
                self.find_links(url)
        e = time.time() - st
        # print(f'process_url took {e}')

    def worker(self, domain):

        for url in self.domain_dict[domain]:
            # print('{}: {}'.format(threading.current_thread().name, url))
            if self.check_file_count_no_display():
                self.process_url(url)
            else:
                return

    def process_main_link_queue(self):
        '''
        process entire main_link_queue into a dictionary organized by domain (domain_dict)
        Per domain, calls process_url on each url
        Recurses if there are still urls in main_link_queue and the file_count has not been met
        '''

        st = time.time()
        while bool(self.main_link_queue):
            link = self.main_link_queue.pop()

            parsed_link = urlparse(link)
            if parsed_link.netloc not in self.domain_dict and link not in self.repo_files and self.check_domain(parsed_link.netloc):
                self.domain_dict[parsed_link.netloc] = set()
                self.domain_dict[parsed_link.netloc].add(link)
            elif parsed_link.netloc in self.domain_dict and link not in self.repo_files and self.check_domain(parsed_link.netloc):
                self.domain_dict[parsed_link.netloc].add(link)

        if self.threaded:

            pool = ThreadPool(8)

            pool.map(self.worker, (self.domain_dict.keys()))

            pool.close()
            pool.join()


        else:
            for domain in self.domain_dict:
                for url in self.domain_dict[domain]:
                    if self.check_file_count():
                        self.process_url(url)
                    else:
                        return

        if bool(self.main_link_queue) and self.check_file_count():
            self.process_main_link_queue()
        e = time.time() - st
        # print(f'process_main_link_queue took {e}')

    def check_domain(self, domain):
        '''
        If class domain input exists, returns False if url domain not equal to it
        In all other cases returns True
        Controls if the url will be hit with a request
        '''
        if self.domain:
            return domain == self.domain
        return True

    def check_ext(self, url):
        s = url.split('.')
        if s:
            return s[-1] not in ['mp4', 'jpg', 'png']
        return False

    def add_file_to_repo(self, url):
        '''
        Gets the url and saves filename and status in repo_files
        Saves file in repository
        TODO: error handling for request and file save
        '''
        st = time.time()
        if url not in self.repo_files and self.check_ext(url):
            try:
                r = requests.get(url)
                # print(dir(r))
                # print(r.headers)
                # print(r.apparent_encoding)
                # print()
                if 'Content-Type' in r.headers and'text/html' in r.headers['Content-Type']:
                    self.file_count += 1
                    self.repo_files[url] = {'filename': f'{self.file_count}.html', 'status': r.status_code}
                    with open(os.path.join(self.repo, self.repo_files[url]['filename']), 'wb') as f:
                        f.write(r.content)
                    return True
            except:
                pass
        e = time.time() - st
        # print(f'add_file_to_repo took {e}')
        return False

    def find_links(self, url):
        '''
        Opens a url's file and finds all links within, and all images
        Saves links to main_link_queue and images to url's repo_files entry
        '''
        st = time.time()
        with open(os.path.join(self.repo, self.repo_files[url]['filename']), 'rb') as f:
            soup = BeautifulSoup(f, 'html.parser')
            links = soup.find_all('a')
            self.repo_files[url]['links'] = 0
            for link in links:
                try:
                    parsed_url = urlparse(link['href'])
                    if parsed_url.scheme and parsed_url.netloc:
                        link_url = f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}'
                    else:
                        parsed_host_url = urlparse(url)
                        link_url = f'{parsed_host_url.scheme}://{parsed_host_url.netloc}{parsed_url.path}'
                    self.repo_files[url]['links'] += 1
                    self.main_link_queue.add(link_url)
                except KeyError as e: # <a> tag without href
                    pass
            images = soup.find_all('img')
            self.repo_files[url]['images'] = len(images)
        e = time.time() - st
        # print(f'find_links took {e}')

    def check_file_count_no_display(self):
        if self.file_count >= self.num_pages:
            return False
        return True

    def check_file_count(self):
        '''
        Checks if added files is equal to or greater than the input num_pages
        Displays the files if so and returns a False boolean to indicate that crawling should stop
        '''
        st = time.time()
        if self.file_count >= self.num_pages:
            self.display()
            self.output()
            e = time.time() - st
            # print(f'check_file_count took {e}')
            return False
        e = time.time() - st
        # print(f'check_file_count took {e}')
        return True

    def display(self):
        print(len(self.main_link_queue))
        '''
        For jupyter notebook, displays a table of all files in repo
        '''
        # st = time.time()
        # html = '<table><tr><td>Live URL</td><td>File</td><td>Status</td><td># Links</td><td># Images</td></tr>'
        # for key in self.repo_files:
        #     skey = key.rstrip('/')
        #     status = self.repo_files[key]['status']
        #     filename = self.repo_files[key]['filename']
        #     filename = f'repository/{filename}'
        #     links = self.repo_files[key]['links']
        #     images = self.repo_files[key]['images']
        #     html += f'<tr><td><a href={skey}>{skey}<td><a href={filename}>{key}</a></td><td>{status}</td><td>{links}</td><td>{images}</td></tr>'
        # html += '</table>'
        # display(HTML(html))
        # e = time.time() - st
        # # print(f'display took {e}')

    def output(self):

        # html = '<html><body><table><tr><td>Live URL</td><td>File</td><td>Status</td><td># Links</td><td># Images</td></tr>'
        # for key in self.repo_files:
        #     skey = key.rstrip('/')
        #     status = self.repo_files[key]['status']
        #     filename = self.repo_files[key]['filename']
        #     filename = f'repository/{filename}'
        #     links = self.repo_files[key]['links']
        #     images = self.repo_files[key]['images']
        #     html += f'<tr><td><a href={skey}>{skey}<td><a href={filename}>{key}</a></td><td>{status}</td><td>{links}</td><td>{images}</td></tr>'
        # html += '</table></body></html>'
        # with open('report.html', 'w') as f:
        #     f.write(html)

        with open('repo_files.pkl', 'wb') as f:
            pickle.dump(self.repo_files, f)









