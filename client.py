import threading
import time
from classes.wrapper import Wrapper
from classes.functions import Functions
from classes.jelly_neo import JellyNeo
from classes.neopoints import Neopoints
from classes.inventory import Inventory
from classes.shop import Shop
from classes.stocks import Stocks
from classes.sdb import SDB
from classes.gallery import Gallery
from classes.user_info import UserInfo
from classes.pets import Pets
from classes.user_lookup import UserLookup
from classes.price_cache import PriceCache

class Client:
    def __init__(self, username, password, proxy):
        self.wrapper = Wrapper(username, password, proxy)
        self.neopoints = Neopoints(self.wrapper, Functions)
        self.inventory = Inventory(self.wrapper, Functions)
        self.shop = Shop(self.wrapper, Functions)
        self.stocks = Stocks(self.wrapper, Functions)
        self.sdb = SDB(self.wrapper, Functions)
        self.gallery = Gallery(self.wrapper, Functions, username)
        self.user_info = UserInfo(self.wrapper, Functions)
        self.pets = Pets(self.wrapper, Functions)
        self.user_lookup = UserLookup(self.wrapper, Functions, username)
        self.price_cache = PriceCache()
        self.functions = Functions()
        self.proxy = proxy
        self.username = username

    def scan_account(self):
        inventory_information = ""
        box_information = ""
        gallery_information = ""
        pets_information = ""
        gold = ""
        silver = ""
        bronze = ""
        site_event_trophies = ""
        site_feature_trophies = ""
        account_statistics = ""
        total_inventory_value = 0
        total_box_value = 0
        total_gallery_value = 0

        if self.wrapper.login():
            neopoints = self.neopoints.get_neopoints_on_hand()
            bank = self.neopoints.get_neopoints_in_bank()
            inventory, inventory_quantity = self.inventory.get_inventory()
            
            for inv, qty in zip(inventory, inventory_quantity):
                cache = self.price_cache.get_cached_item_price(inv)
                if cache == "item_does_not_exist":
                    price = JellyNeo(inv, self.proxy).get_item_price()
                    if price != "N/A":
                        price = int(price) * int(qty)
                        total_inventory_value += price
                    self.price_cache.create_cached_item_price(inv, price)
                else:
                    price = cache
                    if int(time.time()) - self.price_cache.get_last_updated(inv) >= self.price_cache.max_cache:
                        price = JellyNeo(inv, self.proxy).get_item_price()
                        self.price_cache.update_cached_item_price(inv, price)
                    if price != "N/A":
                        total_inventory_value += int(price)
                inventory_information += f"--> {inv} x{qty} || {price}\n"

            shop_till = self.shop.shop_till()
            stocks = self.stocks.stock_market_value()
            sdb, sdb_qty = self.sdb.get_sdb()

            for box, qty in zip(sdb, sdb_qty):
                for inv, _qty in zip(box, qty):
                    cache = self.price_cache.get_cached_item_price(inv)
                    if cache == "item_does_not_exist":
                        price = JellyNeo(inv, self.proxy).get_item_price()
                        if price != "N/A":
                            price = int(price) * int(_qty)
                            total_box_value += price
                        self.price_cache.create_cached_item_price(inv, price)
                    else:
                        price = cache
                        if int(time.time()) - self.price_cache.get_last_updated(inv) >= self.price_cache.max_cache:
                            price = JellyNeo(inv, self.proxy).get_item_price()
                            self.price_cache.update_cached_item_price(inv, price)
                        if price != "N/A":
                            total_box_value += int(price)
                    box_information += f"--> {inv} x{_qty} || {price}\n"

            gallery_items, gallery_quantity = self.gallery.get_gallery()

            if gallery_items:
                for inv, qty in zip(gallery_items, gallery_quantity):
                    cache = self.price_cache.get_cached_item_price(inv)
                    if cache == "item_does_not_exist":
                        price = JellyNeo(inv, self.proxy).get_item_price()
                        if price != "N/A":
                            price = int(price) * int(qty)
                            total_gallery_value += price
                        self.price_cache.create_cached_item_price(inv, price)
                    else:
                        price = cache
                        if int(time.time()) - self.price_cache.get_last_updated(inv) >= self.price_cache.max_cache:
                            price = JellyNeo(inv, self.proxy).get_item_price()
                            self.price_cache.update_cached_item_price(inv, price)
                        if price != "N/A":
                            total_gallery_value += int(price)
                    gallery_information += f"--> {inv} x{qty} || {price}\n"

            dob = self.user_info.get_dob()
            pet_names, level, strength, defence, movement, hp, colour, fishing_skill, jobs_completed, jobs_failed, job_rank = self.pets.get_pets()

            for pets, _level, _strength, _defence, _movement, _hp, _colour, _fishing_skill, _jobs_completed, _jobs_failed, _job_rank in zip(pet_names, level, strength, defence, movement, hp, colour, fishing_skill, jobs_completed, jobs_failed, job_rank):
                pets_information += f"--> Name: {pets}\n----> Level: {_level}\n----> Strength: {_strength}\n----> Defence: {_defence}\n----> Movement: {_movement}\n----> HP: {_hp}\n----> Colour: {_colour}\n----> Fishing Skill: {_fishing_skill}\n----> Jobs Completed: {_jobs_completed}\n----> Jobs Failed: {_jobs_failed}\n----> Job Rank: {_job_rank}\n\n"

            site_event, site_features, gold_trophies, silver_trophies, bronze_trophies, avatars, stamps, site_themes, shop_size, gallery_size = self.user_lookup.get_user_lookup()

            if site_event:
                for event in site_event:
                    site_event_trophies += f"--> {event}\n"
            else:
                site_event_trophies += "--> None\n"

            for feature in site_features:
                site_feature_trophies += f"--> {feature}\n"

            if gold_trophies:
                for g in gold_trophies:
                    gold += f"--> {g}\n"
            else:
                gold += "--> None\n"

            if silver_trophies:
                for s in silver_trophies:
                    silver += f"--> {s}\n"
            else:
                silver += f"--> None\n"

            if bronze_trophies:
                for b in bronze_trophies:
                    bronze += f"--> {b}\n"
            else:
                bronze += f"--> None\n"

            account_statistics += f"-> Avatars\n--> {avatars}\n\n-> Stamps\n--> {stamps}\n\n-> Site Themes\n--> {site_themes}\n\n-> Shop Size\n--> {shop_size}\n\n-> Gallery Size\n--> {gallery_size}"

            self.save_account(neopoints, bank, inventory_information, total_inventory_value, shop_till, stocks, box_information, total_box_value, gallery_information, total_gallery_value, dob, pets_information, site_event_trophies, site_feature_trophies, gold, silver, bronze, account_statistics)

    def save_account(self, neopoints, bank, inventory, inventory_value, shop_till, stocks, sdb, sdb_value, gallery, gallery_value, dob, pets, site_event_trophies, site_feature_trophies, gold, silver, bronze, account_statistics):
        with open(f"data/{self.username}.txt", "w") as f:
            f.write(f"################################################\n#                                              #\n#              Inks Account Scan               #\n#                                              #\n################################################\n\n-> Neopoints On Hand\n--> {neopoints}\n\n-> Neopoints In The Bank\n--> {bank}\n\n-> Inventory\n{inventory}\n-> Total Inventory Value\n--> {inventory_value}\n\n-> Shop Till\n--> {shop_till}\n\n-> Stock Market Value\n--> {stocks}\n\n-> Safety Deposit Box\n{sdb}\n-> Total Safety Deposit Box Value\n--> {sdb_value}\n\n-> Gallery\n{gallery}\n-> Gallery Value\n--> {gallery_value}\n\n-> Date of Birth\n--> {dob}\n\n-> Pets\n{pets}-> Site Event Trophies\n{site_event_trophies}\n-> Site Feature Trophies\n{site_feature_trophies}\n-> Gold Trophies\n{gold}\n-> Silver Trophies\n{silver}\n-> Bronze Trophies\n{bronze}\n{account_statistics}")

if __name__ == "__main__":
    account = Functions().get_account_total()
    threads = []
    for i in range(len(account)):
        username, password, proxy = Functions().pull_account(account[i])
        thread = threading.Thread(target=Client(username, password, proxy).scan_account)
        threads.append(thread)
    for i in range(len(account)):
        threads[i].start()
    for i in range(len(account)):
        threads[i].join()
