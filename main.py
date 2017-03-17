import os, csv, re

headers = ['fips','county','state','year','candidate','vote']



with open('pres-vote-2012.csv', 'w') as fout:
    wout = csv.writer(fout)
    wout.writerow(headers)
    for file in ['2012_pres_vote_by_county.csv']:
        print('Processing', file)
        with open(file, 'r') as fin:
            reader = csv.reader(fin)
            reader.__next__()
            for row in reader:
                row.insert(3, 2012)
                wout.writerow(row)



# modifies 2016 to tall and skinny
# with open('pres-vote.csv', 'w') as fout:
#     wout = csv.writer(fout)
#     wout.writerow(headers)
#     for file in ['2016_pres_vote_by_county.csv']:
#         print('Processing', file)
#         with open(file, 'r') as fin:
#             reader = csv.reader(fin)
#             reader.__next__()
#             for row in reader:
#                 trump = row[0:3]
#                 clinton = row[0:3]
#                 trump.extend([2016,'Trump',row[3]])
#                 clinton.extend([2016,'Clinton', row[4]])
#                 wout.writerow(clinton)
#                 wout.writerow(trump)