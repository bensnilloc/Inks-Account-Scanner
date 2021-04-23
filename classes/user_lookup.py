import re

class UserLookup:
    def __init__(self, wrapper, functions, username):
        self.wrapper = wrapper
        self.functions = functions()
        self.username = username

    def get_user_lookup(self):
        site_event = []
        site_feature = []
        shop_size = ""
        gallery_size = ""

        response = self.wrapper.get(f"userlookup.phtml?user={self.username}")

        try:
            site_event_html = self.functions.get_between(response.text.lower(), "site event", "site feature")
        except IndexError:
            site_event_html = ""
        if site_event_html:
            site_event_output = self.functions.regex_find_all(site_event_html, "<br><b>", "</b>")
            for data in site_event_output:
                site_event.append(data.replace("<br>", " - "))

        site_feature_html = self.functions.get_between(response.text.lower(), "site feature", "game trophies")
        if site_feature_html:
            site_feature_output = self.functions.regex_find_all(site_feature_html, "<br><b>", "</b>")
            for data in site_feature_output:
                site_feature.append(data.replace("<br>", " - "))

        gold_trophies = self.functions.regex_find_all(site_feature_html, "champion!!!'><br /><b>", "champion!!!</b></td>")
        silver_trophies = self.functions.regex_find_all(site_feature_html, "second place at <br>", "!!</td>")
        bronze_trophies = self.functions.regex_find_all(site_feature_html, "third place at <br>", "!!</td>")

        avatars = self.functions.regex_find_all(response.text, "secret avatars:</b><br>\n\t\t", "\t\t<br>")[0]
        stamps = self.functions.regex_find_all(response.text, "stamps:</b><br>\n\t\t", "\t\t<br>")[0]
        site_themes = self.functions.regex_find_all(response.text, "site themes:</b><br>\n\t\t", "\t\t<\/td>")[0]
        if self.functions.contains(response.text, "<b>Shop:</b>"):
            shop_size = re.findall(r"<b>size:</b> (.*?)<br><br>", response.text.lower())[0]
        if self.functions.contains(response.text, "<b>Gallery:</b>"):
            gallery_size = re.findall(r"<\/a><br><b>size:</b> (\d+?)    \t\t\t<\/td>", response.text.lower())[0]

        return site_event if site_event else None, site_feature if site_feature else None, gold_trophies if gold_trophies else None, silver_trophies if silver_trophies else None, bronze_trophies if bronze_trophies else None, avatars, stamps, site_themes, shop_size if shop_size else None, gallery_size if gallery_size else None