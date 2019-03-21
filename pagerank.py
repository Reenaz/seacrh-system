import ssl
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import operator


##base ssl config for https
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

matrix = []
links_count = 159

links_file = open("index.txt", "r")
links = [link.rstrip() for link in links_file.readlines()]
links_file.close()

pagerank_map = dict.fromkeys(links, 0)

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

matrix_file = open('matrix.txt', "w")
for row in matrix:
    matrix_file.write(''.join(map(str, row))+'\n')
    for index, value in enumerate(row):
        try:
            pagerank_map[links[index]] = pagerank_map[links[index]] + value
        except IndexError:
            pass


matrix_file.close()

sorted_pagerank_map = sorted(pagerank_map.items(), key=operator.itemgetter(1))


pagerank_file = open('pagerank.txt', "w")
for item in sorted_pagerank_map[::-1]:
    print(item[0] + ' ' + str(item[1]))
    pagerank_file.write(item[0] + ' ' + str(item[1]) + '\n')

pagerank_file.close()
