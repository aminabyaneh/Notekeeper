import pickle
import requests
import json
from Notebook import Notebook
from Note import Note
from Section import Section


class Network:
    def __init__(self, url="http://127.0.0.1:8000/noteserver/"):
        self.server = None
        self.url = None
        self.token = None
        self.server = requests.session()
        self.url = url
        self.refresh_csrf()

    def refresh_csrf(self):
        server_res = self.server.get(self.url + "login/")
        if 'csrftoken' in server_res.cookies:
            self.token = server_res.cookies['csrftoken']
        else:
            self.token = 'null'

    def send_request(self, url_page, dict_data, type_request):
        headers = {'Content-type': 'application/json', "X-CSRFToken": self.token, "Referer": (self.url + url_page)}
        dict_data['csrfmiddlewaretoken'] = self.token
        if type_request is "POST":
            return self.server.post(self.url + url_page, data=json.dumps(dict_data), headers=headers)
        elif type_request is "GET":
            return self.server.get(self.url + url_page, data=json.dumps(dict_data), headers=headers)
        else:
            print("No type other than GET or POST is supported yet")

    def send_request_c(self, url_page, dict_data, type_request):
        headers = {'Content-type': 'application/json', "X-CSRFToken": self.token, "Referer": (self.url + url_page)}
        dict_data['csrfmiddlewaretoken'] = self.token
        if type_request is "POST":
            return self.server.post(self.url + url_page, data=json.dumps(dict_data), headers=headers)
        elif type_request is "GET":
            return self.server.get(self.url + url_page, data=json.dumps(dict_data), headers=headers)
        else:
            print("No type other than GET or POST is supported yet")

    def login_user(self, username, password):
        res = self.send_request("login/", {"username": username, "password": password}, "POST")
        self.refresh_csrf()
        print(res.text)
        return (res.status_code == 200), res.text, res.status_code

    def logout_user(self):
        res = self.send_request("logout/", {}, "POST")
        print(res.text)
        return (res.status_code == 200), res.text, res.status_code

    def signup_user(self, username, password):
        res = self.send_request("signup/", {'username': username, 'password': password}, "POST")
        print(res.text)
        return (res.status_code == 200), res.text, res.status_code

    def create_notebook(self, notebook):
        print(notebook.username)
        res = self.send_request("create/", {"name": notebook.username, "data": "empty"}, "POST")
        print(res.text)
        return (res.status_code == 200), res.text, res.status_code

    def update_notebook(self, notebook):
        print(notebook.username)
        json_notebook = self.notebook_to_json(notebook)
        res = self.send_request("update/", {"name": notebook.username, "data": json_notebook}, "POST")
        print(res.text)
        return (res.status_code == 200), res.text, res.status_code

    def download_notebook(self, username):
        print(username)
        res = self.send_request("get/", {"name": username}, "GET")
        print(json.loads(res.text))
        json_notebook = json.loads(res.text)['data']
        if res.status_code == 200:
            return Network.json_to_notebook(json_notebook)
        else:
            return None

    @staticmethod
    def json_to_notebook(nb):
        nb = json.loads(nb)
        notebook = Notebook(nb[0])

        for s in nb[1]:
            print(s[0])
            notebook.add_section(Section(s[0]))
            for n in s[1]:
                print(n)
                notebook.sections[-1].add_note(Note(n[0], n[1]))
        return notebook

    @staticmethod
    def notebook_to_json(notebook):
        sections = []
        for s in notebook.sections:
            sections.append((s.name, [(n.name, n.data) for n in s.notes]))
        nb = [notebook.username, sections]
        return json.dumps(nb)
