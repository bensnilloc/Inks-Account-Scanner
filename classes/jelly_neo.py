import requests
import re
from classes.functions import Functions

class JellyNeo:
    def __init__(self, item, proxy):
        self.session = requests.Session()
        self.base = "https://items.jellyneo.net/search/?name="
        self.functions = Functions()
        self.item = item
        if self.functions.contains(proxy, ":"):
            self.set_proxy(proxy)
        
    def set_proxy(self, proxy):
        self.session.proxies.update({"http": f"http://{proxy}", "https": f"https://{proxy}"})

    def url(self, path):
        return f"{self.base}{path}"

    def get_item_price(self):
        if self.functions.contains(self.item, " "):
            self.item = self.item.replace(" ", "+")
        response = self.session.get(self.url(f"{self.item}&name_type=3"), headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Referer": "https://items.jellyneo.net/", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0"})
        if self.functions.contains(response.text, "price-history"):
            item_price = re.findall(r"\">([\d,]+)", response.text)[0]
            if self.functions.contains(item_price, ","):
                item_price = item_price.replace(",", "")
            return item_price
        return "N/A"
