from bs4 import BeautifulSoup
import os
import shutil
import re
from random import random

def tags_below_index(lst, x):
    cur_x = 0
    count = 0
    while cur_x < x:
        count += lst[cur_x]
    return count

def tags_above_index(lst, x):
    cur_x = x + 1
    count = 0
    while cur_x < len(lst):
        count += lst[cur_x]
    return count

def non_tags_between_index(lst, i, j):
    cur_x = i + 1
    count = 0
    while cur_x < j:
        count += 1 - lst[cur_x]
    return count

def lst_score(lst, i, j):
    return tags_below_index(lst, i) + non_tags_between_index(lst, i, j) + tags_above_index(lst, j)

def neighbor(lst, i, j):
    # find randomized neighbor
    max_move_dist = round(len(lst) * .20)
    new_i += i + (2*max_move_dist*random()) - max_move_dist
    new_j += j + (2*max_move_dist*random()) - max_move_dist
    if new_i < 0:
        new_i = 0
    if new_j >= len(lst):
        new_j = len(lst) - 1
    if new_i >= new_j and new_j > 0:
        new_i = new_j - 1
    else:
        new_i = 0
        new_j = 1
    return new_i, new_j

class ContentProcessor:

    def process_repository(self, src_repo='repository'):
        self.src_repo = src_repo
        self.initialize_dst_repo()
        self.initialize_dst_html_repo()
        for file in os.listdir(self.src_repo):
            self.process_file(os.path.join(self.src_repo, file), file)

    def remove_attrs(self, soup):
        whitelist = ['a','img']
        attrs_whitelist = ['id','src','href']
        for tag in soup.find_all(True):
            if tag.name not in whitelist:
                attrs = dict(tag.attrs)
                for attr in attrs:
                    if attr not in ['id']:
                        del tag.attrs[attr]
            else:
                attrs = dict(tag.attrs)
                for attr in attrs:
                    if attr not in attrs_whitelist:
                        del tag.attrs[attr]
        return soup

    def remove_tags(self, soup):
        blacklist = ['script','nav','aside','video','footer','form','input','noscript']
        whitelist = []
        for tag in soup.find_all(True):
            if tag.name in blacklist:
                tag.extract()
        return soup

    def remove_div_extra(self, soup):
        div_content = soup.body.find('div', id=re.compile(".*(content|main).*"))
        if div_content is not None:
            for pre_sibling in div_content.previous_siblings:
                if pre_sibling.name == 'div':
                    pre_sibling.attrs['id'] = 'delete'
            for next_sibling in div_content.next_siblings:
                if next_sibling.name == 'div':
                    next_sibling.attrs['id'] = 'delete'

        for tag in soup.body.find_all('div', id='delete'):
            tag.extract()

        return soup

    def process_file(self, filename, fname):
        with open(filename, 'r') as f:
            # f = open(filename) # file never gets closed otherwise
            try:
                soup = BeautifulSoup(f, 'html.parser')
                new_content = self.clean_html(soup)

                with open (os.path.join('html_processed', fname), 'w') as f2:
                    f2.write(str(new_content))

                clean_content = ''
                for string_soup in new_content.stripped_strings:
                    clean_content += string_soup + " "
                with open (os.path.join('processed', fname), 'w') as f3:
                    f3.write(clean_content)
            except UnicodeDecodeError:
                pass

    def clean_html(self, soup):

        new_body = ""
        soup = self.remove_attrs(soup)
        soup = self.remove_tags(soup)
        new_body += str(soup.title)
        new_body += str(soup.body)
        new_body = BeautifulSoup(new_body)
        new_body = self.remove_div_extra(new_body)

        return new_body

    def initialize_dst_repo(self):
        '''
        If repository exists from previous run, it is deleted
        Creates repository
        '''
        self.dst_repo = 'processed'
        if os.path.isdir(self.dst_repo):
            shutil.rmtree(self.dst_repo)
        os.mkdir(self.dst_repo)

    def initialize_dst_html_repo(self):
        '''
        If repository exists from previous run, it is deleted
        Creates repository
        '''
        self.dst_repo = 'html_processed'
        if os.path.isdir(self.dst_repo):
            shutil.rmtree(self.dst_repo)
        os.mkdir(self.dst_repo)
