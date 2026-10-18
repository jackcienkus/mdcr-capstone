# MDCR Install & Usage Instructions

## Installation Steps
*Step 1*<br>
Clone the repository to your local machine with the command<br>
```git clone https://github.com/jackcienkus/mdcr-capstone.git```

*Step 2*<br>
**Using Conda**
Navigate to the folder of the repository on your local machine.
Once there, if you prefer to set up a conda virtual environment, open a conda command prompt and run the following commands:

```conda env create --file environment.yml```<br>
This creates the conda environment on your machine using the instructions provided in the YAML file

```conda activate mdcr-capstone```<br>
This activates the environment created from the previous command. You'll need to activate the environment before using the pipeline.

**Using local install**
Alternatively, if you would prefer to install the required packages on your machine, use pip:<br>
```pip install pymupdf openpyxl requests pandas numpy```

With this, you should now have the necessary tools installed to use the pipeline.

## Usage Instructions
To demo the pipeline, MDCR contractor data is required. For this demo, you can find usable data by navigating to:<br>
CMSE 495 Teams Channel > General > Shared > MDCR > Demo Data<br>
Once here, download the excel file "Contractor D Workforce Data Form.xlsx", this data is real but anonymized contractor data, thus it is safe to use without an NDA.

Once the file is downloaded somewhere on your local machine, go to your terminal with your activated conda environment (or just any terminal if packages were installed locally), make sure you are inside the mdcr-capstone directory, and run the following command inside your terminal:<br>
```python pipeline.py```

Once this is ran, a file dialogue window will appear. Use your file finder to find the previously downloaded Contractor D XLSX file and select it. It should state inside the terminal "Selected 'Contractor D Workforce Data Form', Loading..."

Once your terminal says "Loaded 'Contractor D Workforce Data Form'!" You can look inside your folder to find two new files, labelled "contractor_analysis.txt" and "contractor_census_ratio.csv", this two files both show the results of the pipeline analysis on the contractor data. The "contractor_analysis.txt" offers a written breakdown of the employment demographics and how they compare to general hirable population as well as the previous year. The "contractor_census_ratio.csv" file offers a formatted version of the demographic comparison data.
