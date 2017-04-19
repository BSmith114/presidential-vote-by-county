from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import csv
import logging

# shannon county changed named to oglala lakota. FIPS code changes from 46113 to a 46102 in 2016 but site still used 46113
# county fips 8014 missing for 2000, it was part of boulder 08013

def get_muni_results(fips, year, muni):
    records = []
    base = ''
    params = {
        'year': year,        
        'f':'1',
        'off':'0',
        'elect':'0',
        'fips': fips
    }
    if muni == 'c':
        base = 'http://uselectionatlas.org/RESULTS/statesub.php?' 
        params['minper'] = '0'
    elif muni == 's':
        base = 'http://uselectionatlas.org/RESULTS/state.php?' 
    else:
        raise ValueError('Muni paramter can be only c (for county) or s (state)')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Accept': 'text/html'
    }
    url = base + urlencode(params) 
    req = Request(url, headers=headers)    
    soup = bs(urlopen(req).read(), 'lxml')
    results = soup.select('table.result tbody tr')
    for result in results:
        row = result.select('td')
        records.append([fips, year, row[1].text, row[3].text, int(row[4].text.replace(',',''))])   
    return records

def create_results_csv(outfile, year):
    headers = ['fips','county','state']
    with open(outfile, 'a', newline='') as fout:
        with open('data/geo/fips/fips.csv') as fin:
            reader = csv.reader(fin)
            writer = csv.writer(fout)
            writer.writerow(headers)
            for fips in reader:
                try:
                    vote = []
                    print(fips[0])
                    if fips[0] != 2:
                        vote = get_muni_results(fips[0], year, 'c')
                        writer.writerows(vote)
                    elif fips[0] == 2:
                        vote = get_muni_results(fips[0], year, 's')
                    else:
                        print(fips[0], ' has no results')
                except:
                    print(fips[0] + ' FAILED')

if __name__ == '__main__':
    years = [2000,2004,2008,2012, 2016]
    for year in years:
        create_results_csv('2000-thru-2016-presidential-vote-by-county.csv', year)
