# # # # # # # # # # # # # #
# MDCR Pipeline Prototype #
# # # # # # # # # # # # # #

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

	dataset_url = "https://api.census.gov/data/2024/acs/acs5"
	api_key = "32685a5c4ce6a6c58598b54cce7cf23a6608f8f0"

	metadata_url = f"{dataset_url}/variables.json"
	meta_response = requests.get(metadata_url)
	variables_meta = meta_response.json()["variables"]
	var_label_map = {
	    var_id: meta["label"].replace("!!", " ")
	    for var_id, meta in variables_meta.items()
	    if "label" in meta
	}

	if region == "us":
		for_region = "us:1"
	else:
		for_region = f"state:{STATE_TO_FIPS[region]}"
	
	params = {"get": "NAME,group(B03002)", "for": f"{for_region}", "key": api_key}
	data_response = requests.get(dataset_url, params=params)
	raw_data = data_response.json()

	df = pd.DataFrame(raw_data[1:], columns=raw_data[0])

	df = df.rename(columns=var_label_map)

	return df

def main():
	same_xlsx = True

	if same_xlsx:
		cur_df, prev_df = df_loader(same_xlsx) # two sheets in one
	else:
		df = df_loader(same_xlsx) # one sheet

	census_df = census_loader(region="us")

	print(census_df)

if __name__ == "__main__":
    main()