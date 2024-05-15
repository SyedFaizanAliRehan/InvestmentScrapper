# Investors Scrapper

1. Create a virtual environment using the below formula

#### python -m venv .venv

2. Activate the virtual environment
   i. Open terminal in VSCode as CMD profile
   ii. If your virtual environment is active the path will be as (.venv) C:\Users\...
   iii. If virtual environment is not active then use the below command to activate it

#### .\.venv\Scripts\activate.bat

3. Run the below commands to install the requirements

#### pip install -r requirements.txt

4. Download the compatible chromedriver from the website: and paste it in the folder where main.py is present
5. Run the code using

#### python main.py

6. Enter your credentials
   i. set skip = 0 and investors to fetch = 1 by defaults
7. Your result will be available in investors_fetched.json file