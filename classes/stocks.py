class Stocks:
    def __init__(self, wrapper, functions):
        self.wrapper = wrapper
        self.functions = functions()

    def stock_market_value(self):
        response = self.wrapper.get("stockmarket.phtml?type=portfolio", referer="http://www.neopets.com/stockmarket.phtml?type=buy")
        if self.functions.contains(response.text, "<b>Paid NP</b>"):
            market_value = self.functions.regex_find_all(response.text, "<b>", "<\/b><\/td>\n<td")[0]
            if self.functions.contains(market_value, ","):
                market_value = market_value.replace(",", "")
            return market_value
        return 0