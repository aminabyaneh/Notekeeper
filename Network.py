import pickle
import requests
import json


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

    def update_notebook(self, notebook):
        str_notebook = pickle.dumps(notebook)
        res = self.send_request("note/add/", {"notebook": str_notebook}, "POST")
        print(res.text)
        return (res.status_code == 200), res.text, res.status_code

    def download_notebook(self, username):
        res = self.send_request("note/get/", {"name": username}, "GET")
        return (res.status_code == 200), res.json(), res.status_code

