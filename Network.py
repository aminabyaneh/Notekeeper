import pickle
import requests


class Network:
    def __init__(self, url):
        self.url = url

    def update_notebook(self, notebook):
        str_notebook = pickle.dumps(notebook)
