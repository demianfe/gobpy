import json
import csv
import os
import http.client
import urllib.parse
import urllib.request
from html import unescape

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5', # --compressed 
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.presidencia.gov.py',
    'Connection': 'keep-alive',
    'Referer': 'https://www.presidencia.gov.py/decretos/',
    'Connection': 'keep-alive'
}

payload = {
	"_search": "true",
	"nd": "1615298190607",
	"rows": "50",
	"page": "1",
	"sidx": "titulo",
	"sord": "desc",
	"filters": "{\"groupOp\":\"AND\",\"rules\":[{\"field\":\"copete\",\"op\":\"cn\",\"data\":\"mitic\"}]}"
}

csvFileName = 'files_meta.csv'
ids = []
if os.path.isfile(csvFileName):
    with open(csvFileName, newline='') as csvfile:
        csvr = csv.reader(csvfile)
        for row in csvr:
            if len(row) > 0:
                ids.append(row[0])
                
if not (os.path.isdir('pdf')):
    os.mkdir('pdf')

conn = http.client.HTTPSConnection('www.presidencia.gov.py')
conn.request('POST', '/tmpl/grillas/decretos.php', urllib.parse.urlencode(payload),headers=headers)
r = conn.getresponse()
data = json.loads(r.read())

data_file = open(csvFileName, 'a+')
csv_writer = csv.writer(data_file)

count = len(ids)

rows = []
for row in data['rows']:
    if count == 0:
        header = ['id', 'date','title', 'link']
        csv_writer.writerow(header)
        count += 1

    val = row['cell']
    row_id = row['id']
    if (row_id not in ids):
        print(row_id)
        link = unescape(val[3])
        link = link[link.find('href="')+6: link.find('" target')]
        csv_writer.writerow([row_id, val[1], unescape(val[2]), link])
        # download file
        pdfFileName = link.split('/')[5]
        urllib.request.urlretrieve(link, r'pdf/'+ pdfFileName)

data_file.close()