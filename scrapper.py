from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import os, main
from flask import session


def hello_text():
    return 'this is import text field'


result_table = []
global login_error
profile_table = []


def authentication(x, y):
    # global profile_table

    global login_error

    # Github credentials
    username = x
    password = y

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    # initialize the Chrome driver
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver = webdriver.Chrome("chromedriver")

    # head to github login page
    driver.get("https://lms.uom.lk/login.php")
    # find username/email field and send the username itself to the input field
    driver.find_element_by_name("LearnOrgUsername").send_keys(username)
    # find password input field and insert password as well
    driver.find_element_by_name("LearnOrgPassword").send_keys(password)
    # click login button
    driver.find_element_by_name("LearnOrgLogin").click()

    # wait the ready state to be complete
    WebDriverWait(driver=driver, timeout=5).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    error_mis_match = "Login Incorrect"
    error_less_fill = "Please Enter User Name & Password"

    # get the errors (if there are)
    errors = driver.find_elements_by_class_name("errortext")
    # print(errors)

    # print the errors optionally
    for e in errors:
        print(e.text)
    # if we find that error message within errors, then login is failed
    if any(error_mis_match in e.text for e in errors):
        print("[!] Login failed caused by mis matching")
        login_error = "mismatch"
        result = False
        # close the driver
        driver.close()
    elif any(error_less_fill in e.text for e in errors):
        print("[!] Login failed caused by less filling")
        login_error = "incomplete"
        result = False
        # close the driver
        driver.close()
    else:
        print("[+] Login successful")
        driver.get("https://lms.uom.lk/mis_exam/reports/view_my_results.php")
        html_content = driver.page_source
        # print(html_content)

        soup = BeautifulSoup(html_content, "html.parser")

        count = 1

        # re-setting lists -> profile_table & result_table
        profile_table.clear()
        result_table.clear()

        for item in soup.find_all("table", {"class": "bodytextbold"}):
            print(item)
            print(count, item.text)
            # tag_array.append(item.text)
            profile_table.append(item)
            count += 1

        for item in soup.find_all("table", {"class": "Text_table"}):
            print(item)
            print(count, item.text)
            # tag_array.append(item.text)
            result_table.append(item)
            count += 1

        print(profile_table)
        print(result_table)

        # main.data[x]['profile_data'] = profile_table[0]

        result = True
        # close the driver
        driver.close()

    return result
