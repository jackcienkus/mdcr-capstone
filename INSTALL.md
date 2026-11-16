# MDCR Install & Usage Instructions

## Installation Steps
*Step 1*<br>
Clone the repository to your local machine with the command<br>
```git clone https://github.com/jackcienkus/mdcr-capstone.git```

*Step 2*<br>
**Using Conda**<br>
Navigate to the folder of the repository on your local machine using cd, for example:<br>
```cd Path\to\mdcr-capstone```

Once there, if you prefer to set up a conda virtual environment, open a conda command prompt and run the following commands:

```conda env create --file environment.yml```<br>
This creates the conda environment on your machine using the instructions provided in the YAML file

```conda activate mdcr-capstone```<br>
This activates the environment created from the previous command. You'll need to activate the environment before using the pipeline.

**Using local install**<br>
Alternatively, if you would prefer to install the required packages on your machine, use pip:<br>
```pip install -r requirements.txt```

With this, you should now have the necessary tools installed to use the pipeline.

## Usage Instructions
For instructions on running the pipeline and program, go to INSTRUCTIONS.md