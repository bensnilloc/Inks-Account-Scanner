class Neopoints:
    def __init__(self, wrapper, functions):
        self.wrapper = wrapper
        self.functions = functions()

    def get_neopoints_on_hand(self):
        response = self.wrapper.get("inventory.phtml", referer="http://www.neopets.com/")
        neopoints = self.functions.get_between(response.text, "id=\"npanchor\" class=\"np-text__2020\">", "</span>")
        if self.functions.contains(neopoints, ","):
            neopoints = neopoints.replace(",", "")
        return int(neopoints)

    def get_neopoints_in_bank(self):
        response = self.wrapper.get("bank.phtml", referer="http://www.neopets.com/")
        if not self.functions.contains(response.text, "I see you don't currently have an account"):
            neopoints = self.functions.get_between(response.text, "Current Balance: ", " NP</span>")
            if self.functions.contains(neopoints, ","):
                neopoints = neopoints.replace(",", "")
            return int(neopoints)
        return 0