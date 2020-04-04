from urllib.parse import urljoin
import base64
import configparser
from datetime import datetime
import json

from bs4 import BeautifulSoup
import requests
import xmltodict

from idloader.lib import Game
from idloader.lib.database import Mod

class Quake(Game):

    def __init__(self, config_file, session):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.session = session

        self.mod_download_url = self.config.get("mods", option="download_url")
        self.mod_manifest_url = self.config.get("mods", option="manifest_url")
        self.mod_screenshot_url = self.config.get("mods", option="screenshot_url")


    def update_modlist(self):
        mod_types = {
                "1": "Single BSP File(s)", 
                "2": "Partial conversion",
                "4": "Speedmapping",
                "5": "Misc. files"
        }

        for item in self.manifest:

            if self.session.query(Mod).filter_by(mod_md5sum=item.get("md5sum")).first():
                continue

            date = datetime.strptime(item.get("date"), "%d.%m.%y").isoformat()

            description = item.get("description")

            if not description:
                description = "No description provided."
            else:
                description = self.strip_tags(description)

            size = int(int(item.get("size")) / 1000) # Round up + convert from KB to MB

            mod = Mod(
                mod_id=item.get("@id"),
                mod_md5sum=item.get("md5sum"),
                mod_type=mod_types.get(item.get("@type")),
                mod_rating=item.get("@rating"),
                mod_size_megabytes=size,
                mod_authors=item.get("author"),
                mod_title=item.get("title"),
                mod_screenshot=None,
                mod_description=description,
                mod_date=date
            )

            self.session.add(mod)
            self.session.commit()

        self.session.close()

    def update_manifest(self):
        print("Downloading manifest...")
        quaddicted_database = requests.get(self.mod_manifest_url).text
        self.manifest = [mod for mod in xmltodict.parse(quaddicted_database).get("files").get("file")]

    def get_mod_screenshot(self, mod_id):
        url = urljoin(self.mod_screenshot_url, f"{mod_id}.jpg")
        return base64.b64encode(requests.get(url).content)
