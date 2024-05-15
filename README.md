# Investors Scrapper

## Description:

This repository contains an automation script designed to scrape investor details from [Tech in Asia](https://www.techinasia.com/), a leading platform for technology news, events, and startup information in Asia. The script extracts relevant information about investors, making it easier to compile data for analysis, reporting, or other purposes.

## Installation

To get started with the script, clone this repository and install the required dependencies:

- git clone https://github.com/SyedFaizanAliRehan/InvestorsScrapper

1. Create a virtual environment using the below formula

   #### python -m venv .venv

2. Activate the virtual environment

   - Open terminal in VSCode as CMD profile
   - If your virtual environment is active the path will be as (.venv) C:\\Users\\username\\...
   - If virtual environment is not active then use the below command to activate it
     #### .\\.venv\\Scripts\\activate.bat

3. Run the below commands to install the requirements

   #### pip install -r requirements.txt

4. Download the compatible chromedriver from the website "https://googlechromelabs.github.io/chrome-for-testing/", extract and paste it in the folder where main.py is present

5. Run the code using

   #### python main.py

6. Enter your credentials
   - set skip = 0 and investors to fetch = 1 by defaults
7. Your result will be available in investors_fetched.json file
