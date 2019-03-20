import ssl
from bs4 import BeautifulSoup
import urllib.request
import urllib.error


##base ssl config for https
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

matrix = []

links_file = open("index.txt", "r")
links = [link.rstrip() for link in links_file.readlines()]
links_file.close()

for link in links:
    try:
        html = urllib.request.urlopen(link, context=ctx).read()
        soup = BeautifulSoup(html, features="html5lib")
    except urllib.error.HTTPError:
        continue

    try:
        parsed_links = [el['href'] for el in soup.findAll('a')]
    except KeyError:
        pass

    matrix.append(list(map(lambda link: 1 if link in parsed_links else 0, links)))

pagerank_file = open('pagerank.txt', "w")
for row in matrix:
    pagerank_file.write(''.join(map(str, row))+'\n')

pagerank_file.close()