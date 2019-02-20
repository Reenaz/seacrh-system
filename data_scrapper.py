import re
import ssl
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

base_url = "https://lenta.ru/"
base_file_directory="pages/"

links = []
links.append("")

##base ssl config for https
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def filter_visible_txt(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(filter_visible_txt, texts)
    return u" ".join(t.strip() for t in visible_texts)

def write_txt_to_file(filename, txt):
    file = open(filename, "w")
    file.write(txt)
    file.close()


def parse_url(url):
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, features="html5lib")

    return [a.get('href') for a in soup.find_all('a', {'href' : re.compile('^[^(http|www|mailto)]')})]

i = 0
while len(links) < 100:
    url = base_url + links[i]
    links.extend(parse_url(url))
    links = list(set(links))
    i += 1

links = links[:100]


for index, link in enumerate(links):
    print(link)
    html = urllib.request.urlopen(base_url + link, context=ctx).read()
    write_txt_to_file(base_file_directory + "page" + str(index) + ".txt", text_from_html(html))


