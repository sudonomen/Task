
### INSTALLATION DEPENDENCIES ##
# PYTHON
# SQL
# MICROSOFT SQL SERVER MANAGEMENT STUDIO {SSMS}
# VISUAL STUDIO CODE (VSC is what I use OR OTHER PYTHON GUI)
# Power BI


############################ START HERE ################################

####                “Do or do not. There is no try.”               #####


###################### TASK 1 ######################
############## Install (as needed) and import the following packages 
### Abbreviate package with alias if viable
######## if any packages are deprecated or unavailable substitue with similar package
######## additional packages may need to be downloaded for dependencies

# %%  INSTALL AND IMPORT
# math

# operator

# pandas

# gc

# os 

# re

# openpyxl

# fnmatch

# pyodbc

# datetime

# schedule

# time

# datetime

# sqlalchemy.exc

# psycopg2

# urllib

# sqlalchemy

#numpy

#urllib


# %% 

## if you determine additional packages are needed to complete the following tasks please import, alias and explain why you used them.

# %%
# Import "Data.csv"



# %%
# Convert Data to Dataframe label it DF1

# %%
# Create empty DataFrame label it DF2 with Columns Full Name, Department, Title, Date

# %%
# convert DF1 strings to columns and rows  i.e. you will need to "split", "replace","fillna","convert" the strings 
# example the first row and first column is a comman delimited string that needs to be converted into columns Full Name, Department, Title, Date
# example the remaining rows and first column are comma delimited strings that needs to be converted to information for Full Name, Department, Title, Date


# %%
#Show "print" data types for DF1 and DF2

# %%
# Export DF2 to an XLSX file and name it OrgChart.xlsx

# %%
#Connect to SQL
# Before you can import to SQL you must install SSMS for "DEVELOPER"  NOT EXPRESS! ssms developer is free to download and install
# Create new Database and Table
# Name Database "Reporting"
# Name Table "Data" 

# %%
# import DF2 from python into SQL "Reporting" DB "Data" Table. 

# %%
# Import SQL "Data" table into Power BI   if you cannot accomplish this task, use the exported DF2 excel file and import it into Power BI

# Create a generic report with the limited information

# Include  a filter by Date

# Save PBI report as "OrgchartReport.pbix" 

# Publish PBi Report to a Web view

# Create a Gateway for PBI Report connection and set up auto refesh every 3 hours a day starting at 1 A.M.

# Save Python file as "Orgchart XLSX_SQL_PBI.py"

# Email Python file "Orgchart XLSX_SQL_PBI.py", Excel File  "Orgchart.xlsx", 
# ScreenShots of SQL DB and Table in a word document, PBI file "OrgchartReport.pbix", Web Link to Report


####  If you are able to complete the following tasks, the following bonus question is provided.

##  Bonus Build Mini Web App that is a form you fill out with Full Name, Department, Title, Date and 
#saves the data either to Excel, SQL or other data source to update the database and table you just created.