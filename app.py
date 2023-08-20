#Import selenium webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#Import time
import time

#Import datetime
import datetime

#Import csv
import csv

USER_POSTS_URL = "https://zarpgaming.com/index.php/forum/topics/posts/mode-latest/userid-37312"

LOGIN_USERNAME = "sinzscraper"
LOGIN_PASSWORD = "sinzscraper"

CSV_FILE_NAME = "posts.csv"

class Post:
    def __init__(self, title, link, date, category):
        self.title = title
        self.link = link
        self.category = category

        #Date is in format: 19 Aug 2023 09:48
        #Turn into datetime object
        self.date = datetime.datetime.strptime(date, "%d %b %Y %H:%M")

        #Write to csv
        with open(CSV_FILE_NAME, "a", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow([title, link, date, category])


def login(driver, username, password):
    #Navigate to index
    driver.get("https://zarpgaming.com/index.php")

    #Find username and password fields
    #Name of the input field for username is "username"
    username_element = driver.find_element(By.NAME, "username")
    password_element = driver.find_element(By.NAME, "password")
    submit_element = driver.find_element(By.NAME, "Submit")

    #Enter username and password
    username_element.send_keys(username)
    password_element.send_keys(password)

    #Click submit button
    submit_element.click()

def get_posts(driver):
    posts = []

    #Navigate to user posts page
    driver.get(USER_POSTS_URL)

    #Sort by All posts
    time_sort_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/table[1]/tbody/tr/td[2]/form/select/option[1]")
    time_sort_element.click()

    #Get total number of posts
    total_posts_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/table[1]/tbody/tr/td[1]")
    total_posts = int(total_posts_element.text.split(" ")[0])
    
    #There are 35 posts per page
    total_pages = total_posts // 35 + 1

    page_counter = 0
    for page in range(0, total_pages):
        driver.get(USER_POSTS_URL + "?start=" + str(page_counter))
        page_counter += 35

        #Get all posts on page
        posts_container = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/form/div/div[2]/div/table/tbody")

        for post in posts_container.find_elements(By.TAG_NAME, "tr"):
            title = post.find_element(By.XPATH, "td[3]/div/a").text
            link = post.find_element(By.XPATH, "td[3]/div/a").get_attribute("href")
            date = post.find_element(By.XPATH, "td[4]/div/span[2]").get_attribute("title")
            category = post.find_element(By.XPATH, "td[3]/div[2]/span/a").text

            posts.append(Post(title, link, date, category))
    



#Create new instance of chrome
driver = webdriver.Chrome()

#Set size of window
driver.set_window_size(1000, 1000)

login(driver, LOGIN_USERNAME, LOGIN_PASSWORD)
get_posts(driver)