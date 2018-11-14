from elastic_indexer import Indexer
import pickle
import os
import math

from multiprocessing.pool import ThreadPool as Pool


class Page:
    def __init__(self, file_list):
        self.file_list = file_list

    def get_file_list(self):
        return self.file_list

class Paginator:
    def __init__(self, file_list, page_size=50):
        self.file_list = file_list
        self.page_size = page_size
        self.total = len(file_list)

        self.pages = []

        self.num_pages = self._num_pages()
        self.page_range = range(self.num_pages)
        self._populate_pages()

    def _populate_pages(self):
        for i in range(0, self.total, self.page_size):
            self.pages.append(Page(self.file_list[i:i+self.page_size]))

    def _num_pages(self):
        return int(math.ceil(float(self.total) / float(self.page_size)))

    def page(self, index):
        return self.pages[index]

class Index:
    def __init__(self, html_folder='html_processed', text_folder='processed', repo_files='repo_files.pkl', index='test', doc_type='test', page_size=50, recreate=False):
        with open(repo_files, 'rb') as f:
            self.repo_files = pickle.load(f)

        self.reversed_repo_files = self._reverse_repo_files()
        self.html_folder = html_folder
        self.text_folder = text_folder
        self.page_size = page_size

        self.indexer = Indexer(index=index, doc_type=doc_type)
        self.file_list = os.listdir(self.html_folder)

        self.paginator = Paginator(self.file_list, page_size)

        self.recreate = recreate

    def _reverse_repo_files(self):
        return {self.repo_files[key]['filename']: key for key in self.repo_files}

    def _index(self, file_list):
        data = []
        for filename in file_list:
            with open(os.path.join(self.html_folder, filename), 'r', encoding='utf-8') as f: #TODO check if encoding an issue
                html = f.read()
            with open(os.path.join(self.text_folder, filename), 'r', encoding='utf-8') as f:
                text = f.read()

            _id = filename.split('.')[0]

            doc = {
                'filename': filename,
                'url': self.reversed_repo_files[filename],
                'site_text': text,
                'site_html': html,
                'id': _id
            }
            data.append(doc)

        self.indexer.bulk_index_data(data, self.page_size)


    def _worker(self, file_list):
        self._index(file_list)

    def recreate_index(self):
        self.indexer.delete_index()
        # self.indexer.create_index(self.settings)# TODO settings?
        self.indexer.create_empty_index()

    def print_totals(self):
        result = self.indexer.search({'query': {'match_all': {}}})
        print("Indexed {} documents to index {}".format(result['hits']['total'], self.indexer.index))

    def index(self):
        if self.recreate:
            self.recreate_index()# This isn't working TODO
        else:
            self.indexer.create_empty_index()

        pool = Pool(7)
        pool.map(self._worker, [self.paginator.page(pn).get_file_list() for pn in self.paginator.page_range])
        pool.close()
        pool.join()

        self.print_totals()








if __name__ == '__main__':
    i = Index(page_size=4, recreate=False)
    i.index()

