# Inks Account Scanner

Are you looking to pull information from your own neopets account(s) but you don't want to keep manually logging in/changing proxies each time? Inks account scanner does just that. With this tool you'll be able to scan all of your accounts within a couple of minutes as this comes with multi-threading support.

# What does this scan?
- Neopoints on hand
- Neopoints in your bank
- Inventory (with item quantity + prices based on Jelly Neos database)
- Shop till
- Stock market value
- Safety deposit box items (with item quantity + prices based on Jelly Neos database)
- Gallery items (with item quantity + prices based on Jelly Neos database)
- Date of birth
- Pet statistics
- Site event trophies
- Site feature trophies
- Gold trophies
- Silver trophies
- Bronze trophies
- Avatars
- Stamps
- Site themes
- Shop size
- Gallery size

# Features
- Jelly neo price caching
- Local database with cached prices

# Installation
- Download the repository
- Add your accounts into accounts/accounts.json
- Open your terminal/command line and make sure you're in the programs directory
- Then based on your operating system:

<b>Windows</b><br>
<code>python client.py</code>
<br>

<b>Linux/Mac OS</b><br>
<code>python3 client.py</code>

Once finished this will generate files in the "data" folder labeled "YourUsername.txt" with all of the results from the account scan
