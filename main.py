from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import csv

# shannon county FIPS code changes from 46113 to a 46102 all years use 46113
# county fips 8014 missing for 2000, it was part of boulder 08013

def get_state_level_results(fips, year):
    records = []
    base = 'http://uselectionatlas.org/RESULTS/state.php?' 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Accept': 'text/html'
    }
    params = {
        'year': year,        
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

def create_results_csv(outfile):
    with open(outfile, 'w', newline='') as fout:
        with open('data/fips/fips.csv') as fin:
            reader = csv.reader(fin)
            reader.__next__() # skips over header
            writer = csv.writer(fout)
            for county in reader:
                try:
                    vote = []
                    if county[0] != 2:
                        vote = get_county_level_results(county[0], 2016)
                        writer.writerows(vote)
                    elif county[0] == 2:
                        vote = get_state_level_results(county[0], 2000)
                    else:
                        print(county[0], ' has no results')
                except:
                    print(county[0] + ' FAILED')

if __name__ == '__main__':
    # do something
