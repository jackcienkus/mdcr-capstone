# # # # # # # # # # # # # #
# MDCR Pipeline Prototype #
# # # # # # # # # # # # # #

# PURPOSE OF FILE
# This pipeline Python file controls the data pipeline for data analysis of contractor data.
# It intakes a selected file from the user, pulls US Census API data, compares the two, and outputs the result.

# HOW TO USE
# See INSTALL.md for instructions on how to set up and use pipeline

# data loading & analysis libraries are imported when needed below
import os
import sys
import time
from typing import Dict
from typing import cast
from copy import deepcopy
from pathlib import Path
import pandas as pd
import numpy as np

# file loader
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# state loading dictionary for census
STATE_TO_FIPS = { # Michigan is 26
	"AL": "01", "AK": "02", "AZ": "04", "AR": "05",
    "CA": "06", "CO": "08", "CT": "09", "DE": "10",
    "DC": "11", "FL": "12", "GA": "13", "HI": "15",
    "ID": "16", "IL": "17", "IN": "18", "IA": "19",
    "KS": "20", "KY": "21", "LA": "22", "ME": "23",
    "MD": "24", "MA": "25", "MI": "26", "MN": "27",
    "MS": "28", "MO": "29", "MT": "30", "NE": "31",
    "NV": "32", "NH": "33", "NJ": "34", "NM": "35",
    "NY": "36", "NC": "37", "ND": "38", "OH": "39",
    "OK": "40", "OR": "41", "PA": "42", "RI": "44",
    "SC": "45", "SD": "46", "TN": "47", "TX": "48",
    "UT": "49", "VT": "50", "VA": "51", "WA": "53",
    "WV": "54", "WI": "55", "WY": "56", "PR": "72",
}


# Function for implementing the loading animation
def load_animation(load_str: str):
	# String to be displayed when the application is loading
	ls_len = len(load_str)

	# String for creating the rotating line
	animation = "|/-\\"
	anicount = 0

	# used to keep the track of
	# the duration of animation
	counttime = 0

	# pointer for traveling the loading string
	i = 0

	while counttime != 100:

		# used to change the animation speed
		# smaller the value, faster will be the animation
		time.sleep(0.075)

		# converting the string to list
		# as string is immutable
		load_str_list = list(load_str)

		# x->obtaining the ASCII code
		x = ord(load_str_list[i])

		# y->for storing altered ASCII code
		y = 0

		# if the character is "." or " ", keep it unaltered
		# switch uppercase to lowercase and vice-versa
		if x != 32 and x != 46:
			if x > 90:
				y = x - 32
			else:
				y = x + 32
			load_str_list[i] = chr(y)

		# for storing the resultant string
		res = ''
		for j in range(ls_len):
			res = res + load_str_list[j]

		# displaying the resultant string
		sys.stdout.write("\r" + res + animation[anicount])
		sys.stdout.flush()

		# Assigning loading string
		# to the resultant string
		load_str = res

		anicount = (anicount + 1) % 4
		i = (i + 1) % ls_len
		counttime += 1

	# for windows OS
	if os.name == "nt":
		os.system("cls")

	# for linux / Mac OS
	else:
		os.system("clear")

def df_loader(same_xlsx=True):
	"""
	Launches file prompt to load XLSX data files.

	same_xlsx: bool
	 - If current year and previous year data exist on the same file, then True

	returns: constructed dataframe(s)
	"""
	file_select_ok = False
	selected_file = None
	file_name = None
	root = Tk()
	root.withdraw()
	messagebox.showinfo("Welcome", "Please select data you want to analyze.")
	while not file_select_ok:
		selected_file = filedialog.askopenfilename(
			title="Select a File"
		)

		file_name = selected_file.split("/")[-1]
		file_select_ok = messagebox.askokcancel("File Selected", f"Selected '{file_name}'. OK to continue?")
	load_animation("Loading...")
	# Show the picker before loading the data-analysis libraries.

	# If current year and previous year data exists on the same XLSX
	if same_xlsx:
		df = pd.read_excel(f'{selected_file}', skiprows=7, sheet_name=None)
		print(f"Loaded {file_name}.")
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

def gooey_loader(load_path, save_path):
	"""
	Run entire process given an absolute path (for the gooey)
	"""

	from docx import Document

	# Load file
	df = pd.read_excel(f'{load_path}', skiprows=7, sheet_name=None)
	print(f"Loaded {load_path}.")
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

	tags = dict()
	template_path = Path(__file__).resolve().parent / "template-report.docx"
	document = Document(str(template_path))
	workforce_data_analysis(current_year_df, previous_year_df, save_path, document, tags)
	power_bi_csv(current_year_df, previous_year_df, save_path)

def census_loader():
	"""
	Pulls and returns regional EEO data from the US Census API

	region: str
	 - Region to pull data from
	 - use "us" for United States
	 - for other states, consult the STATE_TO_FIPS dictionary

	returns: constructed dataframe
	"""
	import pandas as pd
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
	# for: state:26 is Michigan
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
	import numpy as np
	#Labels for each ratio
	updated_categories = ['Hispanic/Latino Male', 'Hispanic/Latina Female',
	   'White Male', 'Black or African American Male', 'Asian Male',
	   'Native Hawaiian or Other Pacific Islander Male',
	   'American Indian or Alaskan Native Male', 'Two or more races Male',
	   'White Female', 'Black or African American Female', 'Asian Female',
	   'Native Hawaiian or Other Pacific Islander Female',
	   'American Indian or Alaskan Native Female', 'Two or more races Female']

	vals = []

	for i in updated_categories: # for each identity
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
	(positive value is over-represented, negative value is underrepresented)

	"""

	regional_dict = calculate_region_ratios(regional_df) # get regional demographic ratios
	contractor_dict = calculate_contractor_ratios(contractor_df) # get contractor demographic ratios

	# Match wording for dictionaries
	regional_dict["Native Hawaiian or Other Pacific Islander Female"] = regional_dict.pop("Pacific Female")
	regional_dict["American Indian or Alaskan Native Female"] = regional_dict.pop("Native Am Female")
	regional_dict["Native Hawaiian or Other Pacific Islander Male"] = regional_dict.pop("Pacific Male")
	regional_dict["American Indian or Alaskan Native Male"] = regional_dict.pop("Native Am Male")
	regional_dict["Two or more races Male"] = regional_dict.pop("Other Male")
	regional_dict["Two or more races Female"] = regional_dict.pop("Other Female")

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
	(positive value is over-represented, negative value is underrepresented)

	"""
	import numpy as np

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


def workforce_data_analysis(cur_df, prev_df, path: Path,
							document, textbox_tags: Dict[str, str]):
	"""
	Does a workforce analysis on provided contractor data and outputs the results with proper language.
	Output is in form of a csv document and txt file.

	cur_df: DataFrame
	 - Current year contractor data as a dataframe
	prev_df: DataFrame
	 - Previous year contractor data as a dataframe

	returns: None
	"""
	import numpy as np
	from docx.oxml import OxmlElement
	from docx.oxml.ns import qn
	from docx.oxml.text.run import CT_R

	census_df = census_loader()

	diff_dict, regional_dict, contractor_dict = calculate_differences(census_df, cur_df)
	# yr_diff_dict, cur_dict, prev_dict = calculate_year_differences(prev_df, cur_df)
	diff_dict, regional_dict, contractor_dict = dict(diff_dict), dict(regional_dict), dict(contractor_dict)
	# yr_diff_dict, cur_dict, prev_dict = dict(yr_diff_dict), dict(cur_dict), dict(prev_dict)

	# DEMOGRAPHIC CHANGE FILES
	# Writes to file
	csv_text = numeric_analysis(diff_dict)
	print("Saving 'contractor_census_ratio.csv'...")
	with open(f"contractor_census_ratio.csv", "w", encoding="utf-8") as file:
		file.write(csv_text)
	print("Saved 'contractor_census_ratio.csv' successfully.")
	# YoY CHANGE FILES
	#csv_text = numeric_analysis(yr_diff_dict)

	# FILENAME is a global var
	#with open(f"{FILENAME}_year_change_ratio.csv", "w", encoding="utf-8") as file:
	#	file.write(csv_text)

	n_employees = int(cur_df[cur_df['Job Role'] == 'Total Workers']['Row Total'].iloc[0])
	n_prev_employees = int(prev_df[prev_df['Job Role'] == 'Total Workers']['Row Total'].iloc[0])

	statements = list()
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
	# statements.append("Contractor’s reported current workforce represented a surplus or deficit of the available workforce for:")

	findings = ""
	for key in diff_dict:
		findings += f"{key} at {round(diff_dict[key], 1)}% (or {int((diff_dict[key]/100) * n_employees)} employees), "

	findings = findings[:len(findings)-2] + "."

	analysis = " ".join(statements)
	words = analysis + "\n" + findings

	for control in document.element.xpath(".//w:sdt"):
		if control.find(".//" + qn("w:sdt")) is not None:
			continue

		properties = control.find(qn("w:sdtPr"))
		content = control.find(qn("w:sdtContent"))

		tag = properties.find(qn("w:tag"))
		control_id = properties.find(qn("w:id"))

		key = (
			tag.get(qn("w:val"))
			if tag is not None
			else control_id.get(qn("w:val"))
		)

		# current_text = "".join(content.itertext(qn("w:t")))
		# print(f"{key}: {current_text}")
		if key == "workforce_data_analysis":
			textbox_tags[key] = analysis
		elif key == "workforce_data_findings":
			textbox_tags[key] = findings
		if key not in textbox_tags:
			continue

		if content.find(qn("w:tbl")) is not None:
			raise ValueError(f"{key} contains a table; expected a text field")
		paragraph = content.find(qn("w:p"))

		text = str(textbox_tags[key])

		# Keep the selected value and visible label of a dropdown in sync.
		# dropdown = properties.find(qn("w:dropDownList"))
		# if dropdown is not None:
		# 	items = dropdown.findall(qn("w:listItem"))
		# 	selected = next(
		# 		(item for item in items
		# 		 if text in (item.get(qn("w:value")), item.get(qn("w:displayText")))),
		# 		None,
		# 	)
		# 	if selected is None:
		# 		choices = [item.get(qn("w:displayText"), item.get(qn("w:value")))
		# 				   for item in items]
		# 		raise ValueError(f"{key}: {text!r} is not a dropdown option. Choose from {choices}")
		# 	dropdown.set(qn("w:lastValue"), selected.get(qn("w:value")))
		# 	text = selected.get(qn("w:displayText"), selected.get(qn("w:value")))

		# This template displays dates as 'August 13, 2026'. Update the stored
		# date as well, so opening the date picker shows the filled date.
		# date_control = properties.find(qn("w:date"))
		# if date_control is not None:
		# 	try:
		# 		selected_date = datetime.strptime(text, "%B %d, %Y")
		# 	except ValueError as error:
		# 		raise ValueError(f"{key}: use a date such as 'August 13, 2026'") from error
		# 	date_control.set(qn("w:fullDate"), selected_date.strftime("%Y-%m-%dT00:00:00Z"))

		# Create replacement text using the control's font formatting.
		run_element = OxmlElement("w:r")
		formatting = properties.find(qn("w:rPr"))
		if formatting is not None:
			run_element.append(deepcopy(formatting))

		cast(CT_R, run_element).text = text

		# Paragraph controls need a paragraph wrapper, including its formatting.
		replacement = run_element
		if paragraph is not None:
			replacement = OxmlElement("w:p")
			paragraph_formatting = paragraph.find(qn("w:pPr"))
			if paragraph_formatting is not None:
				replacement.append(deepcopy(paragraph_formatting))

			replacement.append(run_element)  # type: ignore[bad-argument-type]

		for child in list(content):
			content.remove(child)
		content.append(replacement)

		# Tell Word this is a filled value, not placeholder text.
		placeholder = properties.find(qn("w:showingPlcHdr"))
		if placeholder is not None:
			properties.remove(placeholder)

	print("Saving 'contractor_analysis.docx'...")
	if type(path) == str:
		document.save(str(path + "/" + "contractor_analysis.docx"))
	else:
		document.save(str(path / "contractor_analysis.docx"))
	print("Saved 'contractor_analysis.docx' successfully.")
	with open(f"contractor_analysis.txt", "w", encoding="utf-8") as file:
		file.write(words)

def power_bi_csv(cur_df, prev_df, path: Path):
	import pandas as pd

	census_df = census_loader()

	diff_dict, _, _ = calculate_differences(census_df, cur_df)
	diff_df = pd.DataFrame(diff_dict, columns=['Demographic', 'Percent Difference'])

	script_dir = Path(__file__).resolve().parent
	target_dir = script_dir / "PowerBI_Data"

	target_dir.mkdir(parents=True, exist_ok=True) # create folder if it doesn't exist

	cur_df = cur_df.replace(r'^\s*$', 0, regex=True) # replace empty white space with 0
	prev_df = prev_df.replace(r'^\s*$', 0, regex=True)
	cur_df.iloc[:, 1:] = cur_df.iloc[:, 1:].astype(int) # turn all number rows to ints (just in case)
	prev_df.iloc[:, 1:] = prev_df.iloc[:, 1:].astype(int)
	cur_df.iloc[:, 1:] = cur_df.iloc[:, 1:] / 10 # fixing weird issue where csv saves with all results multiplied by ten?
	prev_df.iloc[:, 1:] = prev_df.iloc[:, 1:] / 10

	diff_df.to_csv(target_dir / "difference.csv", index=False)
	cur_df.to_csv(target_dir / "current_year.csv", index=False)
	prev_df.to_csv(target_dir / "previous_year.csv", index=False)

def main():
	# The key-based conditions in workforce_data_analysis populate this mapping.
	tags = dict()
	home_dir = Path.home()
	os.chdir(home_dir)

	same_xlsx = True

	if same_xlsx:
		cur_df, prev_df = df_loader(same_xlsx) # two sheets in one
	# else:
	# 	df = df_loader(same_xlsx) # one sheet

	from docx import Document

	# PyInstaller places bundled data beside the script's __file__ at runtime.
	template_path = Path(__file__).resolve().parent / "template-report.docx"
	document = Document(str(template_path))

	load_animation("Starting...")
	workforce_data_analysis(cur_df, prev_df, home_dir, document, tags)
	# power_bi_csv(cur_df, prev_df, home_dir)
	print(f"Files saved to: {home_dir}")
	messagebox.showinfo("Saved!",
						f"Files 'contractor_analysis.docx'"
						f"\nand 'contractor_census_ratio.csv'"
						f"\nsaved to:'{home_dir}'\n\nGoodbye!")
	load_animation("Closing...")
if __name__ == "__main__":
	main()
