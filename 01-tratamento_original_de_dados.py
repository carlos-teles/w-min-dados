import sys
import os
import requests
from datetime import datetime
from clint.textui import progress
import pandas
pandas.set_option('display.float_format', lambda x: '%.2f' % x)
pandas.set_option('display.max_columns', None)

#
#	Ultimo Download da base foi feito dia 09/08/2017
#
#def download_csv(name):
#    """
#    Accepts the name of a calaccess.download CSV and returns its path.
#    """
#    path = os.path.join(os.getcwd(), '{}.csv'.format(name))
#    if not os.path.exists(path):
#        url = "http://calaccess.download/latest/{}.csv".format(name)
#        r = requests.get(url, stream=True)
#        with open(path, 'w') as f:
#            total_length = int(r.headers.get('content-length'))
#            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
#                if chunk:
#                    f.write(chunk)
#                    f.flush()
#    return path
#
#rcpt_path = download_csv("rcpt_cd")
#ff_path = download_csv("filer_filings_cd")
sys.exit(0)
