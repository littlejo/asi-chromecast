import feedparser
from html.parser import HTMLParser
import requests
from catt.api import CattDevice

url= "https://api.arretsurimages.net/api/public/rss/emission/arret-sur-images"
feed = feedparser.parse(url)

links_list = []
url_list = []

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'href' and attr[1].startswith('http://v42.arretsurimages.net/fichiers') and attr[1].endswith('.mp4'):
                url_list.append(attr[1])


def cast_video(ip, video):
    cast = CattDevice(ip_addr=ip)
    cast.play_url(video, resolve=True, block=True)

for i, post in enumerate(feed.entries):
  date = "(%d/%02d/%02d)" % (post.published_parsed.tm_year,\
    post.published_parsed.tm_mon, \
    post.published_parsed.tm_mday)
  

  links_list.append(post.link)
  print(f"{i} {date}: {post.title}")

number = int(input("Choice: "))

url = links_list[number]
r = requests.get(url)

parser = MyHTMLParser()
parser.feed(r.text)

if len(url_list) > 0:
    print(url_list[0])
    cast_video("192.168.0.43", url_list[0])
else:
    print("video unavailable")

