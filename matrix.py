import requests
from bs4 import BeautifulSoup




def explore(p, path):
    print path
    s = BeautifulSoup(p)
    for l in s.find_all('a'):
        link = l.get('href')
        if not link or link.startswith('/')\
            or link.lower().endswith('doc')\
            or link.lower().endswith('pdf'):
            continue
        if link.endswith(".txt"):
            with open(link, "w") as o:
                o.write(requests.get(path + link).text)
        else:
            explore(requests.get(path + link).text, path + link)

r = requests.get("http://www.matrixfiles.com/Scientology%20Materials/Tapes%20in%20order/")
explore(r.text, "http://www.matrixfiles.com/Scientology%20Materials/Tapes%20in%20order/")