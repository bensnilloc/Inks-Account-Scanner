class Gallery:
    def __init__(self, wrapper, functions, username):
        self.wrapper = wrapper
        self.functions = functions()
        self.username = username

    def get_gallery(self):
        response = self.wrapper.get(f"gallery/index.phtml?view=all&gu={self.username}")
        if self.functions.contains(response.text, "to report gallery."):
            items = self.functions.regex_find_all(response.text, "<b class=textcolor>", "</b><br></td>")
            quantity = self.functions.regex_find_all(response.text, "font class=textcolor>qty:", "</font>")
            if items:
                return items, quantity
        return 0, 0