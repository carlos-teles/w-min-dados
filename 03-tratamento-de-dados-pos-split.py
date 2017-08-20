import sys
import glob
import os
import requests
import argparse
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
	else:
		return path

def verify_file_exists_and_split( name ):
	list_files = glob.glob('/tmp/'+name+'*')
	#path = os.path.join('/tmp/', '{}.csv'.format(name))
	#print path
	#if not os.path.exists(path):
	#	print "DOWNLOAD file: "+name
	if len(list_files) <= 1:
		print "DOWNLOAD and SPLIT file: "+name
		sys.exit(0)

def rcpt_part_to_dataframe(part_name):
	"""
	Import a slide of the RCPT_CD table prepared for this notebook.
	"""
	file_name = "rcpt_cd_parta{}".format(part_name)
	path = os.path.join('/tmp/', file_name)
	return pandas.read_csv(path, sep=',', dtype="unicode")

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

def call_generate_csv_propose( num_of_propose ):

	verify_file_exists_and_split( "rcpt_cd" )
	ff_path = verify_file_exists( "filer_filings_cd" )

	itemized_receipts_df_h = rcpt_part_to_dataframe("h")
	itemized_receipts_df_i = rcpt_part_to_dataframe("i")
	itemized_receipts_df_j = rcpt_part_to_dataframe("j")
	itemized_receipts_df_k = rcpt_part_to_dataframe("k")

	recent_itemized_receipts = pandas.concat([
	    itemized_receipts_df_h,
	    itemized_receipts_df_i,
	    itemized_receipts_df_j,
	    itemized_receipts_df_k
	])

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

	supporting_dict_proposes = {
		53: [ {"COMMITTEE_ID":"1376040","COMMITTEE_NAME":"Yes on 53 - Stop Blank Checks"} ],
		54: [ {"COMMITTEE_ID":"1389997","COMMITTEE_NAME":"California Common Cause -- Yes on 54 and 59 (NonProfit 501(C)(4)"},
	    			{"COMMITTEE_ID":"1386494","COMMITTEE_NAME":"Proteus Action League Non-Profit 501 (C)(4) Organization, Opposing Measure 66 and Supporting Measures 54 and 59"},
	    			{"COMMITTEE_ID":"1381029","COMMITTEE_NAME":"Yes on 54 - Voters First, Not Special Interests - Sponsored by Hold Politicians Accountable"}],
		55: [
			{"COMMITTEE_ID":"1385538","COMMITTEE_NAME":"California Kids Campaign, Yes on Props 55 & 56, Sponsored by Common Sense Kids Action, Inc."},
			{"COMMITTEE_ID":"1390602","COMMITTEE_NAME":"Common Sense Kids Action, Inc., Yes on Props. 55 and 56 (NonProfit 501(C)(4))"},
			{"COMMITTEE_ID":"1384591","COMMITTEE_NAME":"Million Voter Project Action Fund, Sponsored by Social Justice Organizations"},
			{"COMMITTEE_ID":"1391170","COMMITTEE_NAME":"Million Voter Project Action Fund - Yes on 55, 56, 57, 58, 62, and No on 66, Sponsored by Social Justice Organizations"},
			{"COMMITTEE_ID":"1372760","COMMITTEE_NAME":"PICO California-Yes on 55, 56 and 57 (Non Profit 501 (C)(3))"},
			{"COMMITTEE_ID":"931704","COMMITTEE_NAME":"United Teachers Los Angeles-Political Action Council of Educators (PACE) Issues, a Committee for Propositions 55 and 58"},
			{"COMMITTEE_ID":"1381382","COMMITTEE_NAME":"Yes on 55 - Californians for Budget Stability, Sponsored by Teachers, Health Care Providers, Doctors and Labor Organizations"},
		],
		56: [
			{"COMMITTEE_ID":"1385538","COMMITTEE_NAME":"California Kids Campaign, Yes on Props 55 & 56, Sponsored by Common Sense Kids Action, Inc."},
			{"COMMITTEE_ID":"1390602","COMMITTEE_NAME":"Common Sense Kids Action, Inc., Yes on Props. 55 and 56 (NonProfit 501 (C) (4))"},
			{"COMMITTEE_ID":"1383858","COMMITTEE_NAME":"Fight Cancer - Yes on 56, Sponsored by American Cancer Society, Inc. and American Cancer Society Cancer Action Network, Inc."},
			{"COMMITTEE_ID":"1384591","COMMITTEE_NAME":"Million Voter Project Action Fund, sponsored by Social Justice Organizations"},
			{"COMMITTEE_ID":"1391170","COMMITTEE_NAME":"Million Voter Project Action Fund - Yes on 55, 56, 57, 58, 62, and No on 66, Sponsored by Social Justice Organizations"},
			{"COMMITTEE_ID":"1372760","COMMITTEE_NAME":"PICO California-Yes on 55, 56 and 57 (Non Profit 501 (C)(3))"},
			{"COMMITTEE_ID":"1377991","COMMITTEE_NAME":"Yes on 56 - Saves Lives California, a Coalition of Doctors, Dentists, Health Plans, Labor, Hospitals, and Non-Profit Health Advocate Organizations"},
			{"COMMITTEE_ID":"1388518","COMMITTEE_NAME":"Yes on 56 Stop Cancer - Planned Parenthood Advocates Mar Monte (Non Profit 501(C)(4))"},
			{"COMMITTEE_ID":"1389668","COMMITTEE_NAME":"Yes on 56 Stop Cancer - Planned Parenthood of Orange and San Bernardino Counties' Community Action Fund (Non Profit 501(C)(4))"}
		],
		57: [
			{"COMMITTEE_ID":"1378703","COMMITTEE_NAME":"California Calls Action Fund (NonProfit 501(C)(4))"},
			{"COMMITTEE_ID":"1387648","COMMITTEE_NAME":"California Calls Action Fund - Yes on 57 (NonProfit 501(C)(4))"},
			{"COMMITTEE_ID":"1346267","COMMITTEE_NAME":"California Statewide Law Enforcement Association Issues Committee (Non-Profit 501(C)5): Yes on Proposition 57"},
			{"COMMITTEE_ID":"1387575","COMMITTEE_NAME":"Civic Participation Action Fund - Yes on 57 (NonProfit 501(C)(4))"},
			{"COMMITTEE_ID":"1385745","COMMITTEE_NAME":"Fund for Policy Reform Nonprofit 501(c)(4), sponsored by the Fund for Policy Reform, Yes on Propositions 57, 62, and 64, K, and L and No on Proposition 66, in support of marijuana legalization, parole for nonviolent offenders, repeal of the death penalty, November runoffs and voting on initiatives and referenda in November."},
			{"COMMITTEE_ID":"1392066","COMMITTEE_NAME":"FWD.us (nonprofit 501(c)(4)) in support of Proposition 57 with help from citizens for public safety and opportunity"},
			{"COMMITTEE_ID":"1384591","COMMITTEE_NAME":"Million Voter Project Action Fund, sponsored by Social Justice Organizations"},
			{"COMMITTEE_ID":"1391170","COMMITTEE_NAME":"Million Voter Project Action Fund - Yes on 55, 56, 57, 58, 62, and No on 66, Sponsored by Social Justice Organizations"},
			{"COMMITTEE_ID":"1391327","COMMITTEE_NAME":"Open Philanthropy Action Fund Yes on 57 (NonProfit 501(C)(4))"},
			{"COMMITTEE_ID":"1372760","COMMITTEE_NAME":"PICO California-Yes on 55, 56 and 57 (Non Profit 501 (C)(3))"},
			{"COMMITTEE_ID":"1382912","COMMITTEE_NAME":"Yes on Prop. 57, Californians for Public Safety and Rehabilitation"}
		],
		58:[
			{"COMMITTEE_ID":"1374153","COMMITTEE_NAME":"Californians for a 21st Century Economy - Yes on 58, a Ricardo Lara Ballot Measure Committee"},
			{"COMMITTEE_ID":"1391170","COMMITTEE_NAME":"Million Voter Project Action Fund - Yes on 55, 56, 57, 58, 62, and No on 66, Sponsored by Social Justice Organizations"},
			{"COMMITTEE_ID":"931704","COMMITTEE_NAME":"United Teachers Los Angeles-Political Action Council of Educators (PACE) Issues, a Committee for Propositions 55 and 58"},
			{"COMMITTEE_ID":"1386477","COMMITTEE_NAME":"Yes on 58, Californians for E	nglish Proficiency Sponsored by Teachers and Service Employees Organizations"}
		],
		59:[
			{"COMMITTEE_ID":"1389997","COMMITTEE_NAME":"California Common Cause - Yes on 54 and 59 (NonProfit 501(C)(4)"},
			{"COMMITTEE_ID":"1387856","COMMITTEE_NAME":"Make Them Listen - Yes on 59"},
			{"COMMITTEE_ID":"1360075","COMMITTEE_NAME":"Move to Amend Yes on Prop 59"},
			{"COMMITTEE_ID":"1386909","COMMITTEE_NAME":"Overturn Citizens United, Yes on 59"},
			{"COMMITTEE_ID":"1386494","COMMITTEE_NAME":"Proteus Action League Non-Profit 501 (C)(4) Organization, Opposing Measure 66 and Supporting Measures 54 and 59"},
			{"COMMITTEE_ID":"1381423","COMMITTEE_NAME":"Yes on 59, California Clean Money Action Fund to Overturn Citizens United (Non Profit 501(C)4)"}
		],
		60: [ {"COMMITTEE_ID":"1356566","COMMITTEE_NAME":"Yes on Prop 60, For Adult Industry Responsibility (FAIR) Committee, With Major Funding By AIDS Healthcare Foundation"} ],
		61: [ 
			{"COMMITTEE_ID":"1387641","COMMITTEE_NAME":"Consumer Watchdog Campaign to Lower Drug Prices, Yes on 61, Major Funding by AIDS Healthcare Foundation"},
			{"COMMITTEE_ID":"1376791","COMMITTEE_NAME":"Yes on Prop 61, Californians for Lower Drug Prices, with major funding by AIDS Healthcare Foundation and California Nurses Association PAC"} 
		],

	}


	opposing_dict_proposes = {
		53: [ {"COMMITTEE_ID":"761010","COMMITTEE_NAME":"CA Business PAC, Sponsored by CA Chamber of Commerce (aka CALBUSPAC) - No on Proposition 53"},
	    		{"COMMITTEE_ID":"1378875","COMMITTEE_NAME":"No on Prop 53 - Californians to Protect Local Control, a Coalition of Public Safety, Local Government, Business and Labor Organizations, and Taxpayers"},
	    		{"COMMITTEE_ID":"1389930","COMMITTEE_NAME":"No on 53, Neighbors Defending Local Control"}],
		54: [ {"COMMITTEE_ID":"1385928","COMMITTEE_NAME":"Californians for an Effective Legislature"} ],
		55: [ {"COMMITTEE_ID":"1385886","COMMITTEE_NAME":"California's Future PAC, Sponsored by the Kersten Institute for Governance & Public Policy"} ],
		56: [ {"COMMITTEE_ID":"1389484","COMMITTEE_NAME":"California Citizens Against Special Interests and Wasteful Taxes, No on Prop. 56"},
	    		{"COMMITTEE_ID":"1386637","COMMITTEE_NAME":"No on 56 - Stop the Special Interest Tax Grab. Major Funding by Philip Morris USA Inc. and R.J. Reynolds Tobacco Company, with a Coalition of Taxpayers, Educators, Healthcare Professionals, Law ..."},
	    		{"COMMITTEE_ID":"1388865","COMMITTEE_NAME":"Protect Small Business and Smoke Free Alternatives, No on 56; Sponsored by Smoke-Free Alternatives Trade Association"}],
		57:[
	    		{"COMMITTEE_ID":"1336580","COMMITTEE_NAME":"Los Angeles Police Protective League Issues PAC - Yes on 66, No on 57"},
	    		{"COMMITTEE_ID":"1386627","COMMITTEE_NAME":"No on 57 - Stop Early Release of Violent Criminals (SERVC)"}
		],
		58: [],
		59: [],
		60: [ {"COMMITTEE_ID":"1385139","COMMITTEE_NAME":"No on Proposition 60, Californians Against Worker Harassment, Sponsored by the Free Speech Coalition"} ],
		61: [ {"COMMITTEE_ID":"1379198","COMMITTEE_NAME":"No on Prop 61 - Californians Against the Deceptive RX Proposition, a Coalition of Veterans Doctors Patient Advocates Seniors Taxpayers and Members of Pharmaceutical Research and Manufacturers of Amer."} ],
	}

	supporting_committees = pandas.DataFrame( supporting_dict_proposes[num_of_propose] )
	supporting_committees['COMMITTEE_POSITION'] = 'SUPPORT'

	opposing_committees = pandas.DataFrame( opposing_dict_proposes[num_of_propose] )
	opposing_committees['COMMITTEE_POSITION'] = 'OPPOSE'
	"""
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
	"""

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

	prop_64_itemized.drop('FILER_ID', axis=1, inplace=True)
	prop_64_itemized.to_csv("/tmp/prop_"+str(num_of_propose)+"_contributions.csv", index=False)

	sys.exit(0)

parser = argparse.ArgumentParser(description="Generate CSVs PROPOSITIONS")
parser.add_argument("propNumber", type=int, help="the proposition number 51 to 67")
args = parser.parse_args()

#print args.propNumber
if args.propNumber > 50 and args.propNumber < 68:
	call_generate_csv_propose( args.propNumber )
else:
	print "ERROR: INVALID PROP NUMBER"
	sys.exit(0)
