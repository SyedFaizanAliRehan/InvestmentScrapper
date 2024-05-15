from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import xpaths
import time
import json

BASE_URL = "https://www.techinasia.com/"
DRIVER_PATH = "./chromedriver.exe"
driver = None
chrome_service = webdriver.ChromeService(DRIVER_PATH)

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

def scroll_to_bottom_element(driver, element):
    current_height = driver.execute_script("return arguments[0].scrollHeight;", element)
    while(1):
        driver.execute_script("arguments[0].scrollTo(0,arguments[0].scrollHeight);", element)
        time.sleep(3)
        new_height = driver.execute_script("return arguments[0].scrollHeight;", element)
        if new_height == current_height:
            break
        current_height = new_height

def login(username:str, password:str):
    global driver
    driver.get(f"{BASE_URL}login")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths.login_email))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths.login_password))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths.login_button))).click()
    WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.XPATH, xpaths.loading_banner)))

def get_investors(index:int = 0):
    global driver
    investor_xpath = f"{xpaths.investment_container}[{index + 1}]"
    investor_name = driver.find_element(By.XPATH, f"{investor_xpath}{xpaths.investor_name}").text
    investor_location = driver.find_element(By.XPATH, f"{investor_xpath}{xpaths.investor_location}").text
    total_investments = 0
    try:
        total_investments = driver.find_element(By.XPATH, f"{investor_xpath}{xpaths.total_investments}").text.split()[0]
    except Exception:
        pass
    total_exits = 0
    try:
        total_exits = driver.find_element(By.XPATH, f"{investor_xpath}{xpaths.total_exits}").text.split()[0]
    except Exception:
        pass
    emails = None
    try:
        emails = driver.find_element(By.XPATH, f"{investor_xpath}{xpaths.emails}").text
    except Exception:
        pass
    return {
        "name": investor_name,
        "location": investor_location,
        "total_investments": total_investments,
        "total_exits": total_exits,
        "emails": emails
    }

def get_reviews(index:int = 0):
    global driver
    investor_xpath = f"{xpaths.investment_container}[{index + 1}]"
    investor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"{investor_xpath}{xpaths.investor_name}")))
    investor_name = investor.text
    investor_link= investor.find_element(By.XPATH, "./a").get_attribute("href")
    driver.execute_script("window.open(arguments[0], '_blank');", investor_link)
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.XPATH, f"//h1[contains(text(),'{investor_name}')]")))
    total_ratings = 0
    try:
        total_ratings = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths.total_ratings))).text
    except Exception:
        pass
    funding_experience_ratings = 0
    funding_experience_users = 0
    try:
        funding_experience = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths.fundraiser_experience))).text
        funding_experience_ratings = funding_experience.split("(")[0]
        funding_experience_users = funding_experience.split("(")[1].split(")")[0]
    except Exception:
        pass
    post_funding_experience_ratings = 0
    post_funding_experience_users = 0
    try:
        post_funding_experience = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths.post_funding_experience))).text
        post_funding_experience_ratings = post_funding_experience.split("(")[0]
        post_funding_experience_users = post_funding_experience.split("(")[1].split(")")[0]
    except Exception:
        pass
    questions = None
    try:
        questions = get_review_qa()
    except Exception:
        pass
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return {
        "total_ratings": total_ratings,
        "funding_experience_ratings": funding_experience_ratings,
        "funding_experience_users": funding_experience_users,
        "post_funding_experience_ratings": post_funding_experience_ratings,
        "post_funding_experience_users": post_funding_experience_users,
        "questions": questions
    }

def get_review_qa():
    global driver
    questions = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpaths.questions)))
    op = {}
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths.load_reviews_button))).click()
    for _ in range(len(questions)):
        try:
            question = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths.current_question)))
            question_text = question.text
            if question_text == "":
                time.sleep(5)
                question_text = question.text
            answers_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpaths.answers)))
            op[question_text] = []
            answer_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths.answer_container)))
            scroll_to_bottom_element(driver, answer_container)
            for answer in answers_elements:
                answer_text = answer.text
                op[question_text].append(answer_text)
        except Exception:
            pass
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths.next_question)))
        if(next_button.is_enabled()):
            next_button.click()
    return op
   
if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    skip = int(input("Enter the number of investors to skip: "))
    limit  = int(input("Enter the number of investors to fetch: "))
    driver = webdriver.Chrome(service=chrome_service)
    login(username=username, password=password)
    driver.get(f"{BASE_URL}companies/investors?reviews=true")
    driver.fullscreen_window()
    total_investors_required = skip + limit
    investors = driver.find_elements(By.XPATH, xpaths.investment_container)
    while len(investors) < total_investors_required:
        scroll_to_bottom(driver)
        investors = driver.find_elements(By.XPATH, xpaths.investment_container)
    data =[]
    try:
        with open("investor.json", "r") as f:
            temp = f.read()
            data = json.loads(temp)
    except Exception:
        pass
    for i in range(skip, total_investors_required):
        investor_details = get_investors(i)
        investor_reviews = get_reviews(i)
        investor_details.update(investor_reviews)
        data.append(investor_details)
    data = json.dumps(data, indent=4)
    with open("investors_fetched.json", "w") as f:
        f.write(data)
    driver.quit()