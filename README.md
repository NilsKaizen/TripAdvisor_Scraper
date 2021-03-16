This is a bot that scrapes all restaurants in TripAdvisor in a selected region.
The main objective was to exctract data from internet to be able to make a 
market research in order to open a restaurant in Verona, Italy. 
Based on the information on TripSdvisor the outcomes were: 

--- INSERT OUTCOMES --- 

RESOURCES / PACKAGES: 
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
	

STEPS AND APPROACH TO THE PROJECT:

	0. Set the database and the tables in MySQL and design the structure
	1. Get all links from the restaurants by page and save into Excel File
	2. Pass through all links and scrap all the valuable information, save it 
	into MySQL adn also into Excle (Back Up)
	(My method was saving all links and restaurants information by pages, 
	so in case that an error appears I have all information saved until the 
	page where the code crashed)
	3. Fetch all data from MySQL and make the analysis with Tableau
