import os
import json

paths = ["data", "settings"]

for folders in paths:
    if not os.path.exists(folders):
        os.mkdir(folders)

if not os.path.exists("settings/settings.json"):
    with open("settings/settings.json", "w") as f:
        json.dump({"delay": {"minimum": 1.7,"maximum": 5.8},"user agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0","headers": {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","accept-encoding": "gzip, deflate","accept-language": "en-US,en;q=0.5","content-type": "application/x-www-form-urlencoded"}}, f, indent=4)

if not os.path.exists("data/database"):
    os.mkdir("data/database")