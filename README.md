# Overview

This is a bot that scrapes all restaurants in TripAdvisor in a selected region and 
saves the information into MySQL Database.
The main objective was to exctract data from internet to be able to make a 
market research in order to open a restaurant in Verona, Italy. This could be useful 
for someone who wants to start a new business and want to know the competitors.

The intention is to check what type of restaurants perform the best and make a 
prototipe, so we can stick to what is the trend and what is that the costumers consider 
the most valuable caracteristic in a restaurant. 

### Based on the information on TriAdvisor the overview of the outcomes were: 

--- INSERT OUTCOMES --- 

## RESOURCES / PACKAGES: 
	- Selenium: WebDriver, to scrap the web. 
	https://www.selenium.dev/
	- Pandas: To create and organize data tables. 
	https://pandas.pydata.org/
	- mysql / my.sql.connector: To interact with MySQL Database
	https://www.w3schools.com/python/python_mysql_getstarted.asp
	- MySQL: To create Databases
	https://www.mysql.com/
	- Excel: To store the Raw Data
	-Tableau: Data visualization 
	https://www.tableau.com/es-es
	

## STEPS AND APPROACH TO THE PROJECT:
(Running Time 3 hours aprox. Dipending on your computer and your internet connection)

	0. Set the database and the tables in MySQL and design the structure
	1. Get all links from the restaurants by page and save into Excel File
	2. Pass through all links and scrap all the valuable information, save it 
	into MySQL and also into Excle (Back Up)
	(My method was saving all links and restaurants information by pages, 
	so in case that an error appears I have all information saved until the 
	page where the code crashed)
	3. Do a data preprocessing and cleaning
	4. Upload the data to MySQL and separate it into tables
	5. Fetch all data from MySQL and make the analysis with Tableau

### 0. Set Database: 
	I used a total of 5 tables: 
		- Contact Information: Name, Address, Phone, Webpage ... 
		- Additional Info: Type of food, special_diets, price_range
		- Ratings: Trip Advisor's, nº reviews, service's, food's, value's
		- Food categories: Separate the types of food into columns
		- Special Categories: Separate special diets into columns
		- Ratings Ponderation: I gave a ponderation (0-3) to every restaturant based
		on the nº of reviews. So when making the prototipe the ones with more reviews
		will affect more to the result. My personal methor to deal mith bias.
		(This research is already biassed because only take into accoount the restaurnts
		in Trip Advisor Webpage)

### 1. Get the links: (links_getter)
	I decided to srap the links and save them into excel sheets for every page, 
	because in case that the code crashes I can start from the page I was before, 
	and not from very the beginning.
	And Links are also saved into a variable in the code. 

### 2. Save data into MySQL: (sql_administrator)
	For every links Scrap the info and save it into MySQL tables and into Excel file
	
### 3. Do data preprocessing and cleaning (data_cleaning)
	Change spaces for '_'
	Set N.A values for Null values

### 4. Upload data into MySQL: (sql_administrator)
	Once all restaurants were scraped fetch all food types and special diets and 
	create two tables with all options.
	Then create another table with rating poinderation. 
	

### IF ERROR APPEARS:
	Sometimes an error occur during scraping due to internet connection so you have to 
	Check the New_RestaurantsLinks.xlsx file if you have all the links you need
	If not: Re-run the script, or go to parts_scrap/links_getter and run it. 
	else: Go to parts_scrap/scrap_rest_info_from_excel_links('New_RestaurantsLinks.xlsx') and 
	run it. 


