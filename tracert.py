import subprocess
import re
import requests
from bs4 import BeautifulSoup
import random


site = input()
print("Start to find ip locations, this may take a few minutes")
class run_cmd():
  def __init__(self) -> None:
    self.result = ""
    self.ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    self.ip_addresses = []
  def run(self, site: str) -> None:
    result = subprocess.run(f"tracert {site}", shell=True, stdout=subprocess.PIPE, text=True)
    result = result.stdout
    self.ip_addresses = re.findall(self.ip_pattern, result)
class get_location(run_cmd):
  def __init__(self) -> None:
    super().__init__()
    self.user_agent_list = [
      "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
    ]
    self.headers = {
      'User-Agent':'Mozilla/5.0',
      'Content-Type':'application/json',
      'method':'GET',
      'Accept':'application/vnd.github.cloak-preview'
    }
  def get_html(self):
    for i, ip in enumerate(self.ip_addresses, start=1):
      url = f"https://ip.900cha.com/{ip}.html"
      print(f"IP address {i}: {ip}")
      header = random.choice(self.user_agent_list)
      self.headers['User-Agent'] = header
      response = requests.get(url, headers=self.headers)
      html = response.text
      soup = BeautifulSoup(html, 'html.parser')
      content = soup.select("body > div > div > div > div.row.mt-3 > div.col-md-8 > ul > li:nth-child(3)")
      try:
        location = content[0].text.replace(" ", "")
        print(location)
      except:
        print("Unable to find the location of the ip")
a = run_cmd()
a = get_location()
a.run(site)
a.get_html()