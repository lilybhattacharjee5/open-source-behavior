from selenium import webdriver
import time
import configparser
import random
from selenium.webdriver.common.keys import Keys

def random_delay(lim):
	return random.random() * lim

cp = configparser.ConfigParser()
cp.optionxform = str
cp.read("config.ini")
config_parameters = dict(cp.items("configs"))

USERNAME = config_parameters['USERNAME']
PASSWORD = config_parameters['PASSWORD']

driver = webdriver.Firefox()
driver.get('https://github.com/login')

assert 'GitHub' in driver.title

time.sleep(random_delay(3))

username_field = driver.find_element_by_id('login_field')
password_field = driver.find_element_by_id('password')
sign_in_button = driver.find_element_by_xpath('//input[@value="Sign in"]')

username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)

sign_in_button.click()

###

num_watchers_data = []
num_stars_data = []
num_forks_data = []

###

time.sleep(random_delay(3))

search_field = driver.find_element_by_xpath('//input[@data-scoped-placeholder="Search or jump to…"]')

search_field.send_keys('OpenCog', Keys.ENTER)

time.sleep(random_delay(2))

# grab the 1st result from the repository search
repo_results = driver.find_elements_by_xpath('//li[@class="repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"]')
if len(repo_results) > 0:
	first_result = repo_results[0]
	repo_links = first_result.find_elements_by_xpath('//a[@class="v-align-middle"]')
	if len(repo_links) > 0:
		repo_link = repo_links[0]
		repo_link.click()

		time.sleep(random_delay(3))

		# grab relevant data: NUMBER of watchers, stars, forks, branches, tags
		watch_elements = driver.find_elements_by_xpath('//a[contains(@aria-label, "users are watching this repository")]')
		star_elements = driver.find_elements_by_xpath('//a[contains(@aria-label, "users starred this repository")]')
		fork_elements = driver.find_elements_by_xpath('//a[contains(@aria-label, "users forked this repository")]')

		if len(watch_elements) > 0:
			watch_element = watch_elements[0]
			num_watchers = watch_element.get_attribute('aria-label')
			num_watchers_data.append(num_watchers)

		if len(star_elements) > 0:
			star_element = star_elements[0]
			num_stars = star_element.get_attribute('aria-label')
			num_stars_data.append(num_stars)

		if len(fork_elements) > 0:
			fork_element = fork_elements[0]
			num_forks = fork_element.get_attribute('aria-label')
			num_forks_data.append(num_forks)

		# grab names of forks

		# grab NUMBER of issues

		# grab NUMBER of pull requests

		# grab NUMBER of commits

# print collected data
print(num_watchers_data)
print(num_stars_data)
print(num_forks_data)

