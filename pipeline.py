# # # # # # # # # # # # # #
# MDCR Pipeline Prototype #
# # # # # # # # # # # # # #

# PURPOSE OF FILE
# This pipeline python file controls the data pipeline for data analysis of contractor data.
# It intakes a selected file from the user, pulls US Census API data, compares the two, and outputs the result.

# HOW TO USE
# See INSTALL.md for instructions on how to set up and use pipeline

# data loading & analysis libraries
import pandas as pd
import numpy as np
import pymupdf
import requests

# file loader
import tkinter as tk
from tkinter import filedialog

# state loading dictionary for census
STATE_TO_FIPS = { # Michigan is 26
	"AL": "01",
	"AK": "02",
	"AZ": "04",
	"AR": "05",
	"CA": "06",
	"CO": "08",
	"CT": "09",
	"DE": "10",
	"DC": "11",
	"FL": "12",
	"GA": "13",
	"HI": "15",
	"ID": "16",
	"IL": "17",
	"IN": "18",
	"IA": "19",
	"KS": "20",
	"KY": "21",
	"LA": "22",
	"ME": "23",
	"MD": "24",
	"MA": "25",
	"MI": "26",
	"MN": "27",
	"MS": "28",
	"MO": "29",
	"MT": "30",
	"NE": "31",
	"NV": "32",
	"NH": "33",
	"NJ": "34",
	"NM": "35",
	"NY": "36",
	"NC": "37",
	"ND": "38",
	"OH": "39",
	"OK": "40",
	"OR": "41",
	"PA": "42",
	"RI": "44",
	"SC": "45",
	"SD": "46",
	"TN": "47",
	"TX": "48",
	"UT": "49",
	"VT": "50",
	"VA": "51",
	"WA": "53",
	"WV": "54",
	"WI": "55",
	"WY": "56",
	"PR": "72",
}

def df_loader(same_xlsx=True):
	"""
	Launches file prompt to load XLSX data files.

	same_xlsx: bool
	 - If current year and previous year data exist on the same file, then True

	returns: constructed dataframe(s)
	"""
	root = tk.Tk()
	root.withdraw()

	selected_file = filedialog.askopenfilename(
		title="Select a File"
	)

	file_name = selected_file.split("/")[-1]
	print(f"Selected '{file_name}', loading...", end='\r')

	# If current year and previous year data exists on the same XLSX
	if same_xlsx:
		df = pd.read_excel(f'{selected_file}', skiprows=7, sheet_name=None)
		print(f"Loaded '{file_name}'!              ")

		previous_year_df = df['Workforce Data Previous Year']
		current_year_df = df['Workforce Data Current Year']

		previous_year_df.columns = ['Job Role', 'Hispanic/Latino Male', 'Hispanic/Latina Female', 'White Male', 'Black or African American Male',
			'Asian Male', 'Native Hawaiian or Other Pacific Islander Male',
			'American Indian or Alaskan Native Male', 'Two or more races Male', 'White Female',
			'Black or African American Female', 'Asian Female',
			'Native Hawaiian or Other Pacific Islander Female',
			'American Indian or Alaskan Native Female', 'Two or more races Female',
			'Row Total']
		previous_year_df = previous_year_df.iloc[1:13].fillna(0)

		current_year_df.columns = ['Job Role', 'Hispanic/Latino Male', 'Hispanic/Latina Female', 'White Male', 'Black or African American Male',
			'Asian Male', 'Native Hawaiian or Other Pacific Islander Male',
			'American Indian or Alaskan Native Male', 'Two or more races Male', 'White Female',
			'Black or African American Female', 'Asian Female',
			'Native Hawaiian or Other Pacific Islander Female',
			'American Indian or Alaskan Native Female', 'Two or more races Female',
			'Row Total']
		current_year_df = current_year_df.iloc[1:13].fillna(0)

		return current_year_df, previous_year_df

	# If XLSX only contains a single sheet
	else:
		df = pd.read_excel(f'{selected_file}', skiprows=7)
		print(f"Loaded '{file_name}'!               ")
		df.columns = ['Job Role', 'Hispanic/Latino Male', 'Hispanic/Latina Female', 'White Male', 'Black or African American Male',
			'Asian Male', 'Native Hawaiian or Other Pacific Islander Male',
			'American Indian or Alaskan Native Male', 'Two or more races Male', 'White Female',
			'Black or African American Female', 'Asian Female',
			'Native Hawaiian or Other Pacific Islander Female',
			'American Indian or Alaskan Native Female', 'Two or more races Female',
			'Row Total']
		df = df.iloc[1:13].fillna(0)

		return df

def census_loader(region="us"):
	"""
	Pulls and returns regional EEO data from the US Census API

	region: str
	 - Region to pull data from
	 - use "us" for United States
	 - for other states, consult the STATE_TO_FIPS dictionary

	returns: constructed dataframe
	"""
	import requests

	dataset_url = "https://api.census.gov/data/2018/acs/acs5/eeo" # 2018
	api_key = "32685a5c4ce6a6c58598b54cce7cf23a6608f8f0"

	metadata_url = f"{dataset_url}/variables.json"
	meta_response = requests.get(metadata_url)
	variables_meta = meta_response.json()["variables"]
	var_label_map = {
		var_id: meta["label"].replace("!!", " ")
		for var_id, meta in variables_meta.items()
		if "label" in meta
	}

	# params for loading
	# for: state:26 is michigan
	# do: for: us-1 for USA
	params = {
		"get": "group(EEOALL1R)",
		"EEO": "0000",
		"ucgid": "0400000US26",
		"key": api_key
	}
	data_response = requests.get(dataset_url, params=params)
	raw_data = data_response.json()

	df = pd.DataFrame(raw_data[1:], columns=raw_data[0])

	df = df.rename(columns=var_label_map)

	return df

def calculate_contractor_ratios(df):
	"""
	Takes contractor demographic data and compiles ratios for each group

	df: dataframe
	 - contractor demographic data
	 - 

	returns: dictionary {demographic:ratio}
	"""

    #Labels for each ratio
	updated_categories = ['Hispanic/Latino Male', 'Hispanic/Latina Female',
	   'White Male', 'Black or African American Male', 'Asian Male',
	   'Pacific Male',
	   'Native Am Male', 'Two or more races Male',
	   'White Female', 'Black or African American Female', 'Asian Female',
	   'Pacific Female',
	   'Native Am Female', 'Two or more races Female',
	   'Row Total']

	vals = []

	for i in df_categories: # for each identity
		a = df[i][11] / df["Row Total"][11] * 100 # find percentage relative to total worker count
		b = round(a, 2)
		vals.append(b)
	
	
	contractor_ratio = np.column_stack((updated_categories, vals)) # stack the categories and ratios
	contractor_ratio_dict = dict(contractor_ratio) # convert into a dictionary for comparison 
	
	return contractor_ratio_dict

def calculate_region_ratios(df):
	"""
	Takes regional demographic data and compiles ratios for each group

	df: dataframe
	 - region demographic data

	returns: dictionary {demographic:ratio}
	"""

	categories = [
	"Total Pop",
	"Total Male",
	"Total Female",
	"Hispanic/Latino Pop",
	"Hispanic/Latino Male",
	"Hispanic/Latina Female",
	"White Pop",
	"White Male",
	"White Female",
	"Black or African American Pop",
	"Black or African American Male",
	"Black or African American Female",
	"Native Am Pop",
	"Native Am Male",
	"Native Am Female",
	"Asian Pop",
	"Asian Male",
	"Asian Female",
	"Pacific Pop",
	"Pacific Male",
	"Pacific Female",
	"Other Pop",
	"Other Male",
	"Other Female"]

	df = df.dropna(axis = 1) # percentage is already calculated, just need to extract
	df = df.loc[:, df.columns.str.contains('Percent')]
	
	vals = []
	for i in df.columns: 
		vals.append(df[i].item()) # list of ratios

	region_ratio = np.column_stack((categories, vals)) # stack categories with their respective ratios
	region_ratio_dict = dict(region_ratio) # saves as dictionary for comparison

	return region_ratio_dict


def calculate_differences(regional_df, contractor_df):
	"""

	Finds differences of demographic ratio data between region selected and contractor

	regional_df: dataframe
	 - region demographic data

	contractor_df: dataframe
	 - contractor demographic data

	returns: list (demographic,difference)
	(positive value is over represented, negative value is under represented)

	"""

	regional_dict = calculate_region_ratios(regional_df) # get regional demographic ratios
	contractor_dict = calculate_contractor_ratios(contractor_df) # get contractor demographic ratios

	result = []

	for key, val in contractor_dict.items():
		if key in regional_dict:
			result.append([key, round(float(val), 2) - round(float(regional_dict[key]),2)])

	return result, regional_dict, contractor_dict

def calculate_year_differences(prev_year, cur_year):
	"""

	Finds differences of demographics between previous year and current year

	prev_year: dataframe
	 - previous year demographic data

	cur_year: dataframe
	 - current year demographic data

	returns: list (demographic,difference)
	(positive value is over represented, negative value is under represented)

	"""

	prev_dict = calculate_contractor_ratios(prev_year) # get previous contractor demographic ratios
	cur_dict = calculate_contractor_ratios(cur_year) # get current contractor demographic ratios

	result = []

	for key, val in prev_dict.items():
		if key in cur_dict:
			result.append([key, round(float(val), 2) - round(float(prev_dict[key]),2)])

	return result, cur_dict, prev_dict

def numeric_analysis(diff_dict):
	"""
	Writes basic analysis results into a csv format

	diff_dict: dict
	 - Dictionary of ratio differences between contractor data and census data

	returns: csv-like string of data
	"""
	rows = ["Demographic,Percent_Difference"]
	for key in diff_dict:
		rows.append(f"{key},{round(diff_dict[key]/100, 3)}")

	return "\n".join(rows)


def workforce_data_analysis(cur_df, prev_df):
	"""
	Does a workforce analysis on provided contractor data and outputs the results with proper language.
	Output is in form of a csv document and txt file.

	cur_df: DataFrame
	 - Current year contractor data as a dataframe
	prev_df: DataFrame
	 - Previous year contractor data as a dataframe

	returns: None
	"""
	census_df = census_loader(region="us")

	diff_dict, regional_dict, contractor_dict = calculate_differences(census_df, cur_df)
	yr_diff_dict, cur_dict, prev_dict = calculate_year_differences(prev_df, cur_df)
	diff_dict, regional_dict, contractor_dict = dict(diff_dict), dict(regional_dict), dict(contractor_dict)
	yr_diff_dict, cur_dict, prev_dict = dict(yr_diff_dict), dict(cur_dict), dict(prev_dict)

	# DEMOGRAHPIC CHANGE FILES
	# Writes to file
	csv_text = numeric_analysis(diff_dict)

	with open(f"contractor_census_ratio.csv", "w", encoding="utf-8") as file:
		file.write(csv_text)

	# YoY CHANGE FILES
	#csv_text = numeric_analysis(yr_diff_dict)

	# FILENAME is a global var
	#with open(f"{FILENAME}_year_change_ratio.csv", "w", encoding="utf-8") as file:
	#	file.write(csv_text)

	n_employees = int(np.sum(cur_df['Row Total']))
	n_prev_employees = int(np.sum(prev_df['Row Total']))

	statements = []
	statements.append(f"Contractor returned the completed Workforce Data Form, which indicated it had {n_employees} employees as of the review date.")

	# Employment number changes
	YEAR = 2025
	CHANGE = n_employees - n_prev_employees
	RATIO_CHANGE = round(np.abs(CHANGE) / n_prev_employees * 100, 1)
	if CHANGE > 0:
		PHRASE = f"Contractor reported an increase of {CHANGE} employees; a {RATIO_CHANGE}% change in employment."
	elif CHANGE < 0:
		PHRASE = f"Contractor reported a decrease of {CHANGE*-1} employees; a {RATIO_CHANGE*-1}% change in employment."
	else:
		PHRASE = f"Contractor reported no change in the number of employees."
	statements.append(f"Regarding its difference in workforce from {YEAR-1} to {YEAR}, {PHRASE}")

	# TODO: Disability demographics too
	#/////

	# Demographics
	statements.append("Contractor’s reported current workforce represented a surplus or deficit of the available workforce for:")

	words = ""
	for key in diff_dict:
		words += f"{key} at {round(diff_dict[key], 1)}% (or {int((diff_dict[key]/100) * n_employees)} employees), "

	words = words[:len(words)-2] + "."

	analysis = " ".join(statements)

	analysis += "\n" + words

	with open(f"contractor_analysis.txt", "w", encoding="utf-8") as file:
		file.write(analysis)

def main():
	import os
	import sys

	# Force the working directory to be the script's actual folder
	# 	important for writing the csv files
	script_dir = os.path.dirname(os.path.abspath(__file__))
	os.chdir(script_dir)

	same_xlsx = True

	if same_xlsx:
		cur_df, prev_df = df_loader(same_xlsx) # two sheets in one
	else:
		df = df_loader(same_xlsx) # one sheet

	workforce_data_analysis(cur_df, prev_df)


if __name__ == "__main__":
	main()