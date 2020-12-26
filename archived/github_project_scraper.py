from selenium import webdriver
import time
import configparser
import random
from selenium.webdriver.common.keys import Keys
import regex as re
import pandas as pd

###

company_lower_lim = 78
company_upper_lim = 500
curr_idx = company_lower_lim
count = 0

###

numbers = re.compile('([0-9,]*).*')
tab_counts = re.compile('.*\n([0-9]*).*')
proj_url = re.compile('https:\/\/github\.com(.*)')
forked_repo_format = re.compile('([^ ]*) \/ ([^ ]*)')

def random_delay(lower_lim, upper_lim):
	return random.random() * (upper_lim - lower_lim) + lower_lim

cp = configparser.ConfigParser()
cp.optionxform = str
cp.read("config.ini")
config_parameters = dict(cp.items("configs"))

USERNAME = config_parameters['USERNAME']
PASSWORD = config_parameters['PASSWORD']

driver = webdriver.Firefox()
driver.get('https://github.com/login')

assert 'GitHub' in driver.title

time.sleep(random_delay(1, 3))

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
num_issues_data = []
num_prs_data = []
num_commits_data = []
forked_repo_urls = []
proj_urls = []

###

# read open source project names
open_source_projs = pd.read_csv('open_source_projs.csv')
proj_names = list(open_source_projs['Project'])

for os_proj_name in proj_names[company_lower_lim:company_upper_lim + 1]:
	print(os_proj_name)
	try:
		driver.get('https://github.com')

		time.sleep(random_delay(1, 3))

		search_field = driver.find_element_by_xpath('//input[@data-scoped-placeholder="Search or jump to…"]')

		search_field.send_keys(os_proj_name, Keys.ENTER)

		time.sleep(random_delay(2, 5))

		# grab the 1st result from the repository search
		repo_results = driver.find_elements_by_xpath('//li[@class="repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"]')
		if len(repo_results) > 0:
			first_result = repo_results[0]
			repo_links = first_result.find_elements_by_xpath('//a[@class="v-align-middle"]')
			if len(repo_links) > 0:
				repo_link = repo_links[0]
				repo_link.click()

				time.sleep(random_delay(2, 3))

				proj_urls.append(driver.current_url)

				# grab relevant data: NUMBER of watchers, stars, forks, branches, tags
				watch_elements = driver.find_elements_by_xpath('//a[contains(@aria-label, "users are watching this repository")]')
				star_elements = driver.find_elements_by_xpath('//a[contains(@aria-label, "users starred this repository")]')
				fork_elements = driver.find_elements_by_xpath('//a[contains(@aria-label, "users forked this repository")]')

				# maintaining initialized value for later click
				fork_element = None

				if len(watch_elements) > 0:
					watch_element = watch_elements[0]
					num_watchers = int(numbers.search(watch_element.get_attribute('aria-label')).group(1))
					num_watchers_data.append(num_watchers)
				else:
					num_watchers_data.append(None)

				if len(star_elements) > 0:
					star_element = star_elements[0]
					num_stars = int(numbers.search(star_element.get_attribute('aria-label')).group(1))
					num_stars_data.append(num_stars)
				else:
					num_stars_data.append(None)

				if len(fork_elements) > 0:
					fork_element = fork_elements[0]
					num_forks = int(numbers.search(fork_element.get_attribute('aria-label')).group(1))
					num_forks_data.append(num_forks)
				else:
					num_forks_data.append(None)

				# grab NUMBER of issues
				issue_elements = driver.find_elements_by_xpath('//a[contains(@data-ga-click, "Repository, Navigation click, Issues tab")]')
				if len(issue_elements) > 0:
					num_issues = int(tab_counts.search(issue_elements[0].text).group(1))
					num_issues_data.append(num_issues)
				else:
					num_issues_data.append(None)

				# grab NUMBER of pull requests
				pr_elements = driver.find_elements_by_xpath('//a[contains(@data-ga-click, "Repository, Navigation click, Pull requests tab")]')
				if len(pr_elements) > 0:
					num_prs = int(tab_counts.search(pr_elements[0].text).group(1))
					num_prs_data.append(num_prs)
				else:
					num_prs_data.append(None)

				extension = proj_url.search(driver.current_url).group(1)
				commits_url = extension + '/commits/master'
				commit_xpath = '//a[contains(@href, "{}")]'.format(commits_url)

				# grab NUMBER of commits
				commit_elements = driver.find_elements_by_xpath(commit_xpath)
				if len(commit_elements) > 0:
					num_commits = int(numbers.search(commit_elements[0].text).group(1).replace(',', ''))
					num_commits_data.append(num_commits)
				else:
					num_commits_data.append(None)

				# grab names of forks
				if fork_element:
					fork_element.click()

				time.sleep(random_delay(1, 3))

				repo_elements = driver.find_elements_by_class_name('repo')
				curr_forked_repo_urls = []
				for forked_repo in repo_elements:
					grouped_repo = forked_repo_format.search(forked_repo.text)
					forked_user = grouped_repo.group(1)
					forked_repo_name = grouped_repo.group(2)
					forked_url = 'https://github.com/' + forked_user + '/' + forked_repo_name
					curr_forked_repo_urls.append(forked_url)
				forked_repo_urls.append(curr_forked_repo_urls)
	except:
		print('Encountered exception')

	if len(proj_urls) < count + 1:
		proj_urls.append(None)
	if len(num_watchers_data) < count + 1: 
		num_watchers_data.append(None)
	if len(num_forks_data) < count + 1:
		num_forks_data.append(None)
	if len(num_issues_data) < count + 1:
		num_issues_data.append(None)
	if len(num_prs_data) < count + 1:
		num_prs_data.append(None)
	if len(num_commits_data) < count + 1:
		num_commits_data.append(None)
	if len(forked_repo_urls) < count + 1:
		forked_repo_urls.append([])

	# consolidate into dataframe in each iteration
	print(len(forked_repo_urls))
	proj_df = pd.DataFrame({
		'Project': proj_names[company_lower_lim:curr_idx + 1],
		'Url': proj_urls,
		'Number of watchers': num_watchers_data,
		'Number of forks': num_forks_data,
		'Number of issues': num_issues_data,
		'Number of pull requests': num_prs_data,
		'Number of commits': num_commits_data,
		'Fork urls': forked_repo_urls,
		})
	proj_df.to_csv("proj_data_github_78.csv")
	curr_idx += 1
	count += 1

# print collected data
# print(num_watchers_data)
# print(num_stars_data)
# print(num_forks_data)
# print(num_issues_data)
# print(num_prs_data)
# print(num_commits_data)
# print(forked_repo_urls)
