#!/usr/bin/env python3

from floatingutils.reddit import Reddit
from floatingutils.conf import YamlConf
from floatingutils.log import Log
import webbrowser
import pickle
import time

l = Log()

r = Reddit()

l.info("Logging in...")

config = YamlConf("reddit.login")


username = config.getValue("reddit", "username")
cli_id = "CzlpOR3KW0oNBg"
headless = config.getValue("headless")

api_key  = config.getValue("reddit", "api")

l.info("Using {}".format(username))

r.api.set_oauth_app_info(client_id = cli_id, client_secret = api_key, 
                         redirect_uri="http://localhost/reddit_auth")

url = r.api.get_authorize_url("uniqueKey", "identity submit read", True)

l.info(url)
print(url)


l.info("Opening verification...")

if not headless:
  webbrowser.open(url)
else:
  print(url)
  l.info(url)

code = input("Copy the code here: ")

l.info("Setting access...")
access_information = r.api.get_access_information(code)

r.api.set_access_credentials(**access_information)
l.info("Logged in.")

l.info(r.api.get_me())

seen = []
try:
  with open("seen_posts.dat", "rb") as f:
    seen = pickle.load(f)
except:
  pass

while 1:
  s = r.api.get_subreddit("catsstandingup").get_new(limit=5)
  for i in s:
    if i.id not in seen:
      seen.append(i.id)
      with open("seen_posts.dat", "wb") as f:
        pickle.dump(seen, f)
      i.add_comment("Cat.")
      time.sleep(1)

  
