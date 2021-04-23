class Shop:
    def __init__(self, wrapper, functions):
        self.wrapper = wrapper
        self.functions = functions()

    def shop_till(self):
        response = self.wrapper.get("market.phtml?type=till", referer="http://www.neopets.com/market.phtml?type=your")
        if self.functions.contains(response.text, "You currently have"):
            shop_till = self.functions.get_between(response.text, "You currently have <b>", " NP</b>")
            if self.functions.contains(shop_till, ","):
                shop_till = shop_till.replace(",", "")
            return shop_till
        return 0