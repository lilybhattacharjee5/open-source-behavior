from selenium import webdriver
import time
import configparser
import random
from selenium.webdriver.common.keys import Keys
import regex as re
import pandas as pd
from utils import random_delay

###

company_lower_lim = 0
company_upper_lim = 500
curr_idx = company_lower_lim
count = 0

###

numbers = re.compile('([0-9,]*).*')
tab_counts = re.compile('.*\n([0-9]*).*')
proj_url = re.compile('https:\/\/github\.com(.*)')
forked_repo_format = re.compile('([^ ]*) \/ ([^ ]*)')

driver = webdriver.Firefox()

###

num_watchers_data = []
num_stars_data = []
num_forks_data = []
num_issues_data = []
num_prs_data = []
num_commits_data = []
forked_repo_urls = []
proj_urls = []
contributors = []

###

# read open source project names
open_source_projs = pd.read_csv('awesome_open_source_projs.csv')
# proj_names = list(open_source_projs['Project Name'])
proj_names = ['SirixDB', 'PublicLab.org']
# proj_urls = list(open_source_projs['Project Link'])
proj_urls = [str(open_source_projs.loc[open_source_projs['Project Name'] == i].iloc[0]['Project Link']) for i in proj_names]

for os_proj_url in proj_urls[company_lower_lim:company_upper_lim + 1]:
	print(os_proj_url)
	try:
		# driver.get(os_proj_url)

		time.sleep(random_delay(1, 3))

		# # grab relevant data: NUMBER of watchers, stars, forks, branches, tags
		# watch_elements = driver.find_elements_by_xpath('//a[contains(@aria-label, "users are watching this repository")]')
		# star_elements = driver.find_elements_by_xpath('//a[contains(@aria-label, "users starred this repository")]')
		# fork_elements = driver.find_elements_by_xpath('//a[contains(@aria-label, "users forked this repository")]')

		# # maintaining initialized value for later click
		# fork_element = None

		# if len(watch_elements) > 0:
		# 	try:
		# 		watch_element = watch_elements[0]
		# 		num_watchers = int(numbers.search(watch_element.get_attribute('aria-label')).group(1))
		# 		num_watchers_data.append(num_watchers)
		# 	except:
		# 		num_watchers_data.append(None)
		# else:
		# 	num_watchers_data.append(None)

		# if len(star_elements) > 0:
		# 	try:
		# 		star_element = star_elements[0]
		# 		num_stars = int(numbers.search(star_element.get_attribute('aria-label')).group(1))
		# 		num_stars_data.append(num_stars)
		# 	except:
		# 		num_stars_data.append(None)
		# else:
		# 	num_stars_data.append(None)

		# if len(fork_elements) > 0:
		# 	try:
		# 		fork_element = fork_elements[0]
		# 		num_forks = int(numbers.search(fork_element.get_attribute('aria-label')).group(1))
		# 		num_forks_data.append(num_forks)
		# 	except:
		# 		num_forks_data.append(None)
		# else:
		# 	num_forks_data.append(None)

		# # grab NUMBER of issues
		# issue_elements = driver.find_elements_by_xpath('//a[contains(@data-ga-click, "Repository, Navigation click, Issues tab")]')
		# if len(issue_elements) > 0:
		# 	try:
		# 		num_issues = int(tab_counts.search(issue_elements[0].text).group(1))
		# 		num_issues_data.append(num_issues)
		# 	except:
		# 		num_issues_data.append(None)
		# else:
		# 	num_issues_data.append(None)

		# # grab NUMBER of pull requests
		# pr_elements = driver.find_elements_by_xpath('//a[contains(@data-ga-click, "Repository, Navigation click, Pull requests tab")]')
		# if len(pr_elements) > 0:
		# 	try:
		# 		num_prs = int(tab_counts.search(pr_elements[0].text).group(1))
		# 		num_prs_data.append(num_prs)
		# 	except:
		# 		num_prs_data.append(None)
		# else:
		# 	num_prs_data.append(None)

		# grab contributors
		try:
			driver.get(os_proj_url + 'graphs/contributors')
			# time.sleep(random_delay(10, 12))
			time.sleep(random_delay(20, 30))
			curr_contributor_elems = driver.find_elements_by_xpath('//a[contains(@data-hovercard-type, "user")]')
			contributors.append([c.text for c in curr_contributor_elems if c.text != ''])
		except:
			contributors.append([])

		# insights_elements = driver.find_element_by_xpath('//a[contains(@data-ga-click, "Repository, Navigation click, Insights tab")]')
		# if len(insights_elements) > 0:
		# 	try:
		# 		_ 
		# 	except:
		# 		contributors.append(None)
		# else:
		# 	contributors.append(None)

		# try:
		# 	main_branch_summary = driver.find_element_by_xpath('//summary[contains(@title, "Switch branches or tags")]')
		# 	main_branch_span = main_branch_summary.find_element_by_xpath('.//span[contains(@class, "css-truncate-target")]')
		# 	main_branch_name = main_branch_span.text

		# 	extension = proj_url.search(driver.current_url).group(1)
		# 	commits_url = extension + 'commits/' + main_branch_name
		# 	commit_xpath = '//a[contains(@href, "{}")]'.format(commits_url)

		# 	# grab NUMBER of commits
		# 	commit_elements = driver.find_elements_by_xpath(commit_xpath)
		# 	if len(commit_elements) > 0:
		# 		try:
		# 			num_commits = int(numbers.search(commit_elements[0].text).group(1).replace(',', ''))
		# 			num_commits_data.append(num_commits)
		# 		except:
		# 			num_commits_data.append(None)
		# 	else:
		# 		num_commits_data.append(None)
		# except:
		# 	num_commits_data.append(None)

		# # grab names of forks
		# if fork_element:
		# 	fork_element.click()

		# time.sleep(random_delay(1, 3))

		# repo_elements = driver.find_elements_by_class_name('repo')
		# curr_forked_repo_urls = []
		# for forked_repo in repo_elements:
		# 	grouped_repo = forked_repo_format.search(forked_repo.text)
		# 	forked_user = grouped_repo.group(1)
		# 	forked_repo_name = grouped_repo.group(2)
		# 	forked_url = 'https://github.com/' + forked_user + '/' + forked_repo_name
		# 	curr_forked_repo_urls.append(forked_url)
		# forked_repo_urls.append(curr_forked_repo_urls)
	except:
		print('Encountered exception')

	# if len(proj_urls) < count + 1:
	# 	proj_urls.append(None)
	# if len(num_watchers_data) < count + 1: 
	# 	num_watchers_data.append(None)
	# if len(num_forks_data) < count + 1:
	# 	num_forks_data.append(None)
	# if len(num_issues_data) < count + 1:
	# 	num_issues_data.append(None)
	# if len(num_prs_data) < count + 1:
	# 	num_prs_data.append(None)
	# if len(num_commits_data) < count + 1:
	# 	num_commits_data.append(None)
	# if len(forked_repo_urls) < count + 1:
	# 	forked_repo_urls.append([])
	if len(contributors) < count + 1:
		contributors.append([])

	# consolidate into dataframe in each iteration
	# print(len(forked_repo_urls))
	# proj_df = pd.DataFrame({
	# 	'Project': proj_names[company_lower_lim:curr_idx + 1],
	# 	'Url': proj_urls[company_lower_lim:curr_idx + 1],
	# 	'Number of watchers': num_watchers_data,
	# 	'Number of forks': num_forks_data,
	# 	'Number of issues': num_issues_data,
	# 	'Number of pull requests': num_prs_data,
	# 	'Number of commits': num_commits_data,
	# 	'Fork urls': forked_repo_urls,
	# 	})
	proj_df = pd.DataFrame({
		'Project': proj_names[company_lower_lim:curr_idx + 1],
		'Contributors': contributors,
		})
	proj_df.to_csv("awesome_proj_data_contributors_rescrape2.csv")
	curr_idx += 1
	count += 1

driver.close()

# print collected data
# print(num_watchers_data)
# print(num_stars_data)
# print(num_forks_data)
# print(num_issues_data)
# print(num_prs_data)
# print(num_commits_data)
# print(forked_repo_urls)
