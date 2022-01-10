from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep

# Tags, credentials and Urls
email = "Linkedin_email"
password = "Linkedin_password"
email_input_id = 'username'
password_input_id = 'password'
googleSearchName = 'q'
inputTextGoogleSearch = 'Πωλητής αυτοκινήτων'
googleAgreeButton_id = 'L2AGLb'
linkedin_url = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
google_url = 'https://www.google.com/'
user_name_tag = 'text-heading-xlarge inline t-24 v-align-middle break-words'
user_location_tag = 'text-body-small inline t-black--light break-words'
user_last_work_tag = 'inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp inline'

# initialize chrome
driver = webdriver.Chrome("/usr/bin/chromedriver")
driver.maximize_window()

# Ask 1
driver.get(linkedin_url)

email_input = driver.find_element_by_id(email_input_id)
email_input.send_keys(email)

password_input = driver.find_element_by_id(password_input_id)
password_input.send_keys(password)

password_input.send_keys(Keys.ENTER)

# Ask 2
driver.get(google_url)

googleSearch = driver.find_element_by_name(googleSearchName)
googleAgreeButton = driver.find_element_by_id(googleAgreeButton_id)
googleAgreeButton.click()

googleSearch.send_keys('site:linkedin.com/in ' + inputTextGoogleSearch)
googleSearch.submit()

# Ask 3
soup = BeautifulSoup(driver.page_source, 'html.parser')
urls = []
usersInfo = []
search = soup.find_all('div', class_='g')
for h in search:
    url = h.a.get('href')
    urls.append(url)
for url_ in urls:
    driver.get(url_)
    sleep(3)
    soup_new = BeautifulSoup(driver.page_source, 'html.parser')
    user_name = soup_new.find(class_=user_name_tag)
    user_location = soup_new.find(class_=user_location_tag)
    user_last_work = soup_new.find(class_=user_last_work_tag)
    if user_name:
        user_name = user_name.get_text().replace("\n", "").strip()
    if user_location:
        user_location = user_location.get_text().replace("\n", "").strip()
    if user_last_work:
        user_last_work = user_last_work.get_text().replace("\n", "").strip()
    usersInfo.append({"user_name": user_name, "user_location": user_location, "user_last_work": user_last_work})
print(usersInfo)
driver.quit()
