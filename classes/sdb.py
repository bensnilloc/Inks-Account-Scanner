import re

class SDB:
    def __init__(self, wrapper, functions):
        self.wrapper = wrapper
        self.functions = functions()

    def get_sdb(self):
        items = []
        quantity = []
        response = self.wrapper.get("safetydeposit.phtml", referer="http://www.neopets.com/")
        items.append(self.functions.regex_find_all(response.text, "\"left\"><b>", "<br><span class=\"medtext\">"))
        quantity.append(self.functions.regex_find_all(response.text, "<td align=\"center\"><b>", "</b></td>"))
        sdb_pages = list(set(map(int, re.findall(r"<option value='(\d+?)'>", response.text))))
        sdb_pages.sort()
        for pages in sdb_pages:
            response = self.wrapper.get(f"safetydeposit.phtml?offset={pages}&obj_name=&category=0", referer=response.url)
            items.append(self.functions.regex_find_all(response.text, "\"left\"><b>", "<br><span class=\"medtext\">"))
            quantity.append(self.functions.regex_find_all(response.text, "<td align=\"center\"><b>", "</b></td>"))
        return items, quantity