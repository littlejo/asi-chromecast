import feedparser
from html.parser import HTMLParser
import requests
import sys
from catt.api import CattDevice

url= "https://api.arretsurimages.net/api/public/rss/emission/arret-sur-images"

class MyHTMLParser(HTMLParser):
    url_list = []

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'href' and attr[1].startswith('http://v42.arretsurimages.net/fichiers') and attr[1].endswith('.mp4'):
                self.url_list.append(attr[1])

def find_ip():
    return "192.168.0.43"

def cast_video(ip, video):
    cast = CattDevice(ip_addr=ip)
    cast.play_url(video, resolve=True, block=True)

def print_video_asi(feed):
    links_list = []
    for i, post in enumerate(feed.entries):
      date = "(%d/%02d/%02d)" % (post.published_parsed.tm_year,\
        post.published_parsed.tm_mon, \
        post.published_parsed.tm_mday)
      links_list.append(post.link)
      print(f"{i} {date}: {post.title}")
    return links_list

def get_download_url(url):
    r = requests.get(url)
    parser = MyHTMLParser()
    parser.feed(r.text)
    return parser.url_list

def check_availability_video(url_list):
    if len(url_list) == 0:
        print("video unavailable")
        sys.exit(1)


feed = feedparser.parse(url)
links_list = print_video_asi(feed)
number = int(input("Choice: "))
url = links_list[number]
url_list = get_download_url(url)
check_availability_video(url_list)
ip = find_ip()
cast_video(ip, url_list[0])
