import ssl
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import operator
import time


def calc_pagerank(link_index):
    pr_value = 1-d/links_count
    pr_sum = 0

    for i in range(links_count):
        if (matrix[i][link_index] == 1):
            pr_sum += pagerank_map[links[i]]/len(list(filter(lambda x: x == 1, matrix[i])))
    return pr_value + d*pr_sum


##base ssl config for https
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

matrix = []
links_count = 158
d = 0.85

links_file = open("index.txt", "r")
links = [link.rstrip() for link in links_file.readlines()]
links_file.close()
pagerank_map = dict.fromkeys(links, 0)

for link in links:
    try:
        html = urllib.request.urlopen(link, context=ctx).read()
        soup = BeautifulSoup(html, features="html5lib")
    except urllib.error.HTTPError:
        time.sleep(3)
        try:
            html = urllib.request.urlopen(link, context=ctx).read()
            soup = BeautifulSoup(html, features="html5lib")
        except urllib.error.HTTPError:
            print("error: " + link)
            continue

    try:
        parsed_links = [el['href'] for el in soup.findAll('a')]
    except KeyError:
        pass

    matrix.append(list(map(lambda link: 1 if link in parsed_links else 0, links)))


matrix_file = open('matrix.txt', "w")
for row in matrix:
    matrix_file.write(''.join(map(str, row))+'\n')
matrix_file.close()

pagerank = []
base_pr_val = 1/links_count

for i in range(links_count):
    pagerank_map[links[i]] = base_pr_val

for i in range(links_count):
    pagerank_map[links[i]] = calc_pagerank(i)

sorted_pagerank_map = sorted(pagerank_map.items(), key=operator.itemgetter(1))

pagerank_file = open('pagerank.txt', "w")
for item in sorted_pagerank_map[::-1]:
    print(item[0] + ' ' + str(item[1]))
    pagerank_file.write(item[0] + ' ' + str(item[1]) + '\n')

pagerank_file.close()
