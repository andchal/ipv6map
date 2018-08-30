from zipfile import ZipFile
import requests
from io import BytesIO
import os

src = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City-CSV.zip'
dst = os.path.join(os.path.dirname(__file__), 'ipv6data.csv')

resp = requests.get(src).content
zipfile = ZipFile(BytesIO(resp))
with open(dst, 'w') as f:
    for line in zipfile.open('GeoLite2-City-CSV_20180807/GeoLite2-City-Blocks-IPv6.csv').readlines():
        f.write(line.decode('utf-8'))
