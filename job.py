from bs4 import BeautifulSoup
import urllib.request as ur
import re
import sys

url_base = "https://www.indeed.com/jobs?q=software+engineer&l=Chicago,+IL&jt=fulltime&explvl=entry_level"
pgno = 0

try:
    response = ur.urlopen(url_base+str(pgno))
    html_doc = response.read()
except:
    print("URL not accesible")
    exit()

soup = BeautifulSoup(html_doc, 'html.parser')


p1 = re.compile(r'[2-9]\s*\+?-?\s*[1-9]?\s*[yY]e?a?[rR][Ss]?')
p2 = re.compile('[Cc]itizens?(ship)?')

for job in soup.find_all(class_='result clickcard'):
    link = job.find(class_="turnstilelink").get('href')
    title = link.get('title')
    name = job.find(class_='company').get_text()


# pgno lets me go through all the pages
if pgno > 0:
    try:
        response = ur.urlopen(url_base+str(pgno))
        html_doc = response.read()
    except:
        sys.exit()

    soup = BeautifulSoup(html_doc, 'html.parser')

for job in soup.find_all(class_='result'):
        link = job.find(class_="turnstileLink")
        try:
            jt = link.get('title')
        except:
            jt = ""
        try:
            comp = job.find(class_='company').get_text().strip()
        except:
            comp = ""


        toVisit = "http://www.indeed.com"+link.get('href')
        try:
            html_doc = ur.urlopen(toVisit).read().decode('utf-8')
        except:
            continue
        m = p1.search(html_doc)
        n = p2.search(html_doc)
        if not m and not n:
            print(jt,",",comp,":",toVisit,"\n")
