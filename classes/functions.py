import time
import random
import json
import re

class Functions:
    def contains(self, data, string):
        return True if string in data else False

    def get_between(self, data, first, last):
        return data.split(first)[1].split(last)[0]

    def delay(self, minimum, maximum):
        return time.sleep(random.uniform(minimum, maximum))

    def parse_settings(self):
        with open("settings/settings.json", "r") as f:
            data = json.load(f)
        return data["delay"]["minimum"], data["delay"]["maximum"], data["user agent"]

    def pull_header(self, header):
        with open("settings/settings.json", "r") as f:
            data = json.load(f)
        return data["headers"][header]

    def pull_account(self, username):
        with open("accounts/accounts.json", "r") as f:
            data = json.load(f)
        for accounts in data:
            if accounts == username:
                return accounts, data[accounts]["password"], data[accounts]["proxy"]

    def get_account_total(self):
        accounts = []
        with open("accounts/accounts.json", "r") as f:
            data = json.load(f)
        for account in data:
            accounts.append(account)
        return accounts

    def regex_find_all(self, data, first, last):
        return re.findall(rf"{first}(.*?){last}", data.lower())