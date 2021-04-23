class Inventory:
    def __init__(self, wrapper, functions):
        self.wrapper = wrapper
        self.functions = functions()

    def get_inventory(self):
        response = self.wrapper.post("np-templates/ajax/inventory.php?itemType=np&alpha=&action=", referer="http://www.neopets.com/inventory.phtml", requested_with="XMLHttpRequest")
        if self.functions.contains(response.text, "inv-total-count"):
            items = self.functions.regex_find_all(response.text, "data-itemname=\"", "\" data-itemquantity")
            quantity = self.functions.regex_find_all(response.text, "data-itemquantity=\"", "\">")
            if items:
                return items, quantity
        return 0, 0