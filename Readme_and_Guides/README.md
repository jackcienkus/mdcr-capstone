# MDCR Capstone
This repository contains information and files regarding the MDCR Capstone project.

## Team Members
Yousif Elya - elyayous@msu.edu<br> 
Anthony Kosinski - kosins34@msu.edu<br>
Jack Cienkus - cienkusj@msu.edu<br>
Kayla Kramer - krame154@msu.edu<br>
Renee Watson - watso351@msu.edu

## MDCR Overview
The Michigan Department of Civil Rights (MDCR) is the state agency responsible for investigating and resolving complaints of unlawful discrimination across Michigan.

## Project
This project aims to build a workflow to assist MDCR in organizing contractor compliance data, compare contractor-reported workforce composition with relevant labor-market reference data, and to help produce drafts of review reports. We will be creating a pipeline which can automatically draft editable reports on equal employment opportunity compliance based on inputted contractor data. 

## Goal
The end goal for this project is to help MDCR reduce manual search time, calculation and re-entry that goes into each review. 

## Research Questions
- How can MDCR systematically compare contractor workforce composition to labor-market availability
by geography and job category?
- Which statistical comparisons are most useful for flagging potential compliance concerns while minimizing false positives?
- What data-integration workflow can automate the matching of contractor submissions to geography-specific reference datasets?
- Which dashboard views best support triage, documentation, and follow-up decisions for compliance
staff?

## Repository Structure
| File / Folder | Description |
| :--- | :--- |
| notebooks/ | Contains exploratory and statistical analysis Jupyter notebooks (`B_Analysis.ipynb`, `C_Analysis.ipynb`). |
| PowerBI_Data/ | Contains data files formatted for PowerBi visualizations |
| .gitignore | Specifies untracked temporary files and local outputs for Git to ignore |
| INSTALL.md | Setup and installation instructions for the project |
| INSTRUCTIONS.md | Guide on how to use the program's interface |
| LICENSE | Creative Commons license governing repository usage and distribution |
| README.md| Project overview, research questions, and repository guide |
| environment.yml |  Conda environment specification and Python package dependencies |
| pipeline.py | Main data processing and compliance report generation pipeline |
| program.py| GUI application used to select datafiles and run the pipeline |
| template-report.docx | Word document template used to generate the reports |

## Install & Usage Instructions
* For detailed setup instructions, please see the [Installation & Usage Guide](INSTALL.md)<br>
* For usage instructions, please see the [Instructions Guide](INSTRUCTIONS.md)


