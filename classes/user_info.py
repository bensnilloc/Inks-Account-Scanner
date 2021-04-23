class UserInfo:
    def __init__(self, wrapper, functions):
        self.wrapper = wrapper
        self.functions = functions()

    def get_dob(self):
        return self.functions.get_between(self.wrapper.get("userinfo.phtml").text, "Date of Birth</b><br>\n</td><td>\n", "</td></tr>").strip()