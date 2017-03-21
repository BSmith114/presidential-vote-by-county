from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import csv

# shannon county FIPS code changes from 46113 to a 46102 all years use 46113
# county fips 8014 missing for 2000, it was part of boulder 08013


def get_county_level_results(fips, year):
    records = []
    base = 'http://uselectionatlas.org/RESULTS/statesub.php?' 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Accept': 'text/html'
    }
    params = {
        'year': year,
        'minper':'0',
        'f':'1',
        'off':'0',
        'elect':'0',
        'fips': fips
    }

    url = base + urlencode(params) 
    req = Request(url, headers=headers)    
    soup = bs(urlopen(req).read(), 'lxml')
    results = soup.select('table.result tbody tr')
    for result in results:
        row = result.select('td')
        records.append([fips, year, row[1].text, row[3].text, int(row[4].text.replace(',',''))])   
    return records

with open('2004-scrape.csv', 'w', newline='') as fout:
    with open('data/county/2016-pres-vote-by-county.csv') as fin:
        reader = csv.reader(fin)
        reader.__next__() # skips over header
        writer = csv.writer(fout)
        for county in reader:
            try:
                vote = get_county_level_results(county[0], 2000)
                if vote:
                    writer.writerows(vote)
                else:
                    print(county[0], ' has no results')
            except:
                print(county[0] + ' FAILED')

