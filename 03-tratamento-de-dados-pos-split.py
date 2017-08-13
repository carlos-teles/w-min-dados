import sys
import glob
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

def verify_file_exists ( name ):
	path = os.path.join('/tmp/', '{}.csv'.format(name))
	if not os.path.exists(path):
		print "DOWNLOAD file: "+path
		sys.exit(0)

def verify_file_exists_and_split( name ):
	list_files = glob.glob('/tmp/'+name+'*')
	#path = os.path.join('/tmp/', '{}.csv'.format(name))
	#print path
	#if not os.path.exists(path):
	#	print "DOWNLOAD file: "+name
	if len(list_files) <= 1:
		print "DOWNLOAD and SPLIT file: "+name
		sys.exit(0)

verify_file_exists_and_split( "rcpt_cd" )
verify_file_exists( "filer_filings_cd" )

def rcpt_part_to_dataframe(part_name):
	"""
	Import a slide of the RCPT_CD table prepared for this notebook.
	"""
	file_name = "rcpt_cd_parta{}".format(part_name)
	path = os.path.join('/tmp/', file_name)
	return pandas.read_csv(path, sep=',', dtype="unicode")

itemized_receipts_df_h = rcpt_part_to_dataframe("h")
itemized_receipts_df_i = rcpt_part_to_dataframe("i")
itemized_receipts_df_j = rcpt_part_to_dataframe("j")

recent_itemized_receipts = pandas.concat([
    itemized_receipts_df_h,
    itemized_receipts_df_i,
    itemized_receipts_df_j
])

def remove_amended_filings(df):
	"""
	Accepts a dataframe with FILING_ID and AMEND_ID files.
	
	Returns only the highest amendment for each unique filing id.
	"""
	max_amendments = df.groupby('FILING_ID')['AMEND_ID'].agg("max").reset_index()
	merged_df = pandas.merge(df, max_amendments, how='inner', on=['FILING_ID', 'AMEND_ID'])
	print "Removed {} amendments".format(len(df)-len(merged_df))
	print "DataFrame now contains {} rows".format(len(merged_df))
	return merged_df

real_recent_itemized_receipts = remove_amended_filings(recent_itemized_receipts)
real_sked_a = real_recent_itemized_receipts[
    real_recent_itemized_receipts['FORM_TYPE'] == 'A'
]
trimmed_itemized = real_sked_a[[
    'FILING_ID',
    'AMEND_ID',
    'CTRIB_NAMF',
    'CTRIB_NAML',
    'CTRIB_CITY',
    'CTRIB_ST',
    'CTRIB_ZIP4',
    'CTRIB_EMP',
    'CTRIB_OCC',
    'RCPT_DATE',
    'AMOUNT',
]]

clean_itemized = trimmed_itemized.rename(
    index=str,
    columns={
        "CTRIB_NAMF": "FIRST_NAME",
        "CTRIB_NAML": "LAST_NAME",
        "CTRIB_CITY": "CITY",
        "CTRIB_ST": "STATE",
        "CTRIB_ZIP4": "ZIPCODE",
        "CTRIB_EMP": "EMPLOYER",
        "CTRIB_OCC": "OCCUPATION",
        "RCPT_DATE": "DATE"
    }
)

filer_filings_df = pandas.read_csv(ff_path, sep=',', index_col=False, dtype='unicode')

filer_to_filing = filer_filings_df[['FILER_ID', 'FILING_ID']].drop_duplicates()

supporting_committees = pandas.DataFrame([
    {"COMMITTEE_ID":"1343793","COMMITTEE_NAME":"Californians for Responsible Marijuana Reform, Sponsored by Drug Policy Action, Yes on Prop. 64"},
    {"COMMITTEE_ID":"1376077","COMMITTEE_NAME":"Californians for Sensible Reform, Sponsored by Ghost Management Group, LLC dba Weedmaps"},
    {"COMMITTEE_ID":"1385506","COMMITTEE_NAME":"Drug Policy Action - Non Profit 501c4, Yes on Prop. 64"},
    {"COMMITTEE_ID":"1385745","COMMITTEE_NAME":"Fund for Policy Reform (Nonprofit 501(C)(4))"},
    {"COMMITTEE_ID":"1371855","COMMITTEE_NAME":"Marijuana Policy Project of California"},
    {"COMMITTEE_ID":"1382525","COMMITTEE_NAME":"New Approach PAC (MPO)"},
    {"COMMITTEE_ID":"1386560","COMMITTEE_NAME":"The Adult Use Campaign for Proposition 64"},
    {"COMMITTEE_ID":"1381808","COMMITTEE_NAME":"Yes on 64, Californians to Control, Regulate and Tax Adult Use of Marijuana While Protecting Children, Sponsored by Business, Physicians, Environmental and Social-Justice Advocate Organizations"}
])
supporting_committees['COMMITTEE_POSITION'] = 'SUPPORT'

opposing_committees = pandas.DataFrame([
    {"COMMITTEE_ID":"1382568","COMMITTEE_NAME":"No on Prop. 64, Sponsored by California Public Safety Institute"},
    {"COMMITTEE_ID":"1387789","COMMITTEE_NAME":"Sam Action, Inc., a Committee Against Proposition 64 with Help from Citizens (NonProfit 501(C)(4))"}
])
opposing_committees['COMMITTEE_POSITION'] = 'OPPOSE'

prop_64_committees = pandas.concat([supporting_committees, opposing_committees])

prop_64_filings = filer_to_filing.merge(
    prop_64_committees,
    how="inner",
    left_on='FILER_ID',
    right_on="COMMITTEE_ID"
)

prop_64_itemized = prop_64_filings.merge(
    clean_itemized,
    how="inner",
    left_on="FILING_ID",
    right_on="FILING_ID"
)
print len(prop_64_itemized)




sys.exit(0)
