import requests
from bs4 import BeautifulSoup


def format(data):
    temp = [raw.strip() for raw in data.strings if raw.strip()
            and "[" not in raw.strip()]
    return temp


def cint(x):
    return x.replace(',', '')


def convert(data):
    try:
        if not ("No data" in data[1] or cint(data[1]).isdigit()):
            return
        return {"country": data[0],
                "cases": cint(data[1]),
                "death": cint(data[2]),
                "recovered": cint(data[3])}
    except Exception:
        return


def scrap_stats():
    html_doc = requests.get(
        'https://en.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory').text

    soup = BeautifulSoup(html_doc, 'html.parser')
    tag_info = soup.find("table", {"id": "thetable"}).find(
        'tbody').find_all('tr')[1:]
    data = []
    for tr in tag_info:
        ctr = convert(format(tr))
        if ctr:
            data.append(ctr)
    return data


def scrap_news():
    URL = "https://www.google.com/search?hl=en&tbm=nws&as_q={query}"
    response = requests.get(URL.format(query="Corona India")).text
    filtered = response.split('<div class="kCrYT">')[1:-1]
    data = []
    for x in range(0, len(filtered)-1, 2):
        link = filtered[x][filtered[x].find(
            "https://"):filtered[x].find("&amp;")]
        title = filtered[x].split('</div>')[0].split('<div')[1].split('>')[1]
        time = filtered[x+1].split('class="r0bn4c rQMQod">')[1].split("<")[0]
        data.append({"title": title, "link": link, "time": time})
    return data
