import requests
import json
import time
import random
import os
from classes.functions import Functions

class Wrapper:
    def __init__(self, username, password, proxy):
        self.session = requests.Session()
        self.functions = Functions()
        self.base = "http://www.neopets.com/"
        self.minimum_delay = self.functions.parse_settings()[0]
        self.maximum_delay = self.functions.parse_settings()[1]
        self.user_agent = self.functions.parse_settings()[2]
        self.username = username
        self.password = password
        if self.functions.contains(proxy, ":"):
            self.set_proxy(proxy)

    def set_proxy(self, proxy):
        self.session.proxies.update({"http": f"http://{proxy}", "https": f"https://{proxy}"})

    def url(self, path):
        return f"{self.base}{path}"

    def get(self, path, referer = None):
        self.functions.delay(self.minimum_delay, self.maximum_delay)
        accept, accept_encoding, accept_language = self.functions.pull_header("accept"), self.functions.pull_header("accept-encoding"), self.functions.pull_header("accept-language")
        return self.session.get(self.url(path), headers={"Accept": accept, "Accept-Encoding": accept_encoding, "Accept-Language": accept_language, "Referer": referer, "User-Agent": self.user_agent})

    def post(self, path, data = None, referer = None, requested_with = None):
        self.functions.delay(self.minimum_delay, self.maximum_delay)
        accept, accept_encoding, accept_language = self.functions.pull_header("accept"), self.functions.pull_header("accept-encoding"), self.functions.pull_header("accept-language")
        if data:
            return self.session.post(self.url(path), data=data, headers={"Accept": accept, "Accept-Encoding": accept_encoding, "Accept-Language": accept_language, "Referer": referer, "User-Agent": self.user_agent})
        return self.session.post(self.url(path), headers={"Accept": accept, "Accept-Encoding": accept_encoding, "Accept-Language": accept_language, "Referer": referer, "User-Agent": self.user_agent, "X-Requested-With": requested_with})

    def login(self):
        response = self.post("login.phtml", data={"destination": "", "return_format": "1", "username": self.username, "password": self.password})
        if not self.functions.contains(response.text, "npanchor"):
            print(f"[-] Unable to login as {self.username}. Check your username/password?")
            return False
        print(f"[+] Logged in as {self.username}")
        return True
