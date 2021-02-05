from selenium import webdriver
import time
import random
import regex as re
import pandas as pd
from utils import random_delay
import ast
from multiprocessing import Process
from winnowing import winnowing_algorithm, calculate_similarity

###

start_lim = 0
end_lim = 100000000000

window_size = 5
n = 4

proj_pattern = re.compile('(https:\/\/github\.com\/[^\/]*\/[^\/]*\/)(.*)')
number_pattern = re.compile('.* ([0-9,\+]*)')

###

shared_hash = {}

def traverse_proj_structure_parallel(fork_num, proj_url, base_proj_structure, is_parent):
	shared_hash[fork_num] = traverse_proj_structure(proj_url, base_proj_structure, is_parent)

def traverse_proj_structure(proj_url, base_proj_structure, is_parent):
	firefox_options = webdriver.FirefoxOptions()
	firefox_options.set_headless()
	driver = webdriver.Firefox(firefox_options = firefox_options)

	print(proj_url)

	sub_url_queue = [proj_url]
	leaf_hashes = {}
	leaf_similarities = {}

	ignored = ['.github', '.DS_Store']

	# perform bfs on tree
	while len(sub_url_queue):
		popped_url = sub_url_queue.pop(0)
		driver.get(popped_url)
		print(popped_url, len(sub_url_queue))
		time.sleep(random_delay(1, 2))
		# check if raw button exists = file
		try:
			raw_button = driver.find_element_by_id('raw-url')
			raw_button.click()
			relative_path = proj_pattern.search(popped_url).group(2)
			file_code = driver.find_elements_by_tag_name('pre')[0].text
			leaf_hashes[relative_path] = winnowing_algorithm(file_code, window_size, n)
			if not is_parent:
				if relative_path in base_proj_structure:
					leaf_similarities[relative_path] = calculate_similarity(base_proj_structure[relative_path], leaf_hashes[relative_path])
				else:
					leaf_similarities[relative_path] = None
					print(relative_path, "not found in base")
		except:
			file_folder_elems = driver.find_elements_by_xpath('//a[contains(@class, "js-navigation-open link-gray-dark")]')
			child_urls = [f.get_attribute('href') for f in file_folder_elems if f.text not in ignored and '.csv' not in f.text and '.sln' not in f.text]
			sub_url_queue.extend(child_urls)

		time.sleep(random_delay(1, 2))

	driver.close()

	if is_parent:
		return leaf_hashes
	return leaf_similarities

###

firefox_options = webdriver.FirefoxOptions()
# firefox_options.set_headless()
driver = webdriver.Firefox(firefox_options = firefox_options)

cached_structures = {}

### 

fork_start = 1
fork_end = 100000000000000

###

base_urls_ahead = []
fork_links_ahead = []

base_urls_utd = []
fork_links_utd = []
fork_commits_behind = []
fork_files_changed = []

base_url_invalid = []
invalid_fork = []

fork_compare_text = []
base_urls_curr = []

os_proj_data = pd.read_csv('awesome_proj_data_github.csv')
for index, row in list(os_proj_data.iterrows())[start_lim:end_lim + 1]:
	base_url = row['Url']
	forked_urls = ast.literal_eval(row['Fork urls'])[fork_start:fork_end + 1]
	jobs = []
	fork_num = 0
	for f in forked_urls:
		curr_forked_url = f
		print(curr_forked_url)

		driver.get(curr_forked_url)
		time.sleep(random_delay(2, 5))

		try:
			# compare the fork to the base
			compare_elem = driver.find_element_by_xpath("//*[contains(text(), 'This branch is')]")
			curr_fork_text = compare_elem.text
			print(curr_fork_text)
			fork_compare_text.append(curr_fork_text)
		except:
			fork_compare_text.append(None)

		base_urls_curr.append(curr_forked_url)

		# try:
		# 	# compare the fork to the base
		# 	compare_button = driver.find_element_by_xpath('//a[contains(@href, "/compare")]')
		# 	compare_button.click()
		# 	time.sleep(random_delay(5, 10))
		# except:
		# 	base_url_invalid.append(base_url)
		# 	invalid_fork.append(curr_forked_url)
		# 	invalid_df = pd.DataFrame({'Base': base_url_invalid, 'Fork Invalid': invalid_fork})
		# 	invalid_df.to_csv('forks_invalid_' + str(start_lim) + '.csv')
		# 	continue
		
		# try:
		# 	# check to see if fork is ahead by any commits
		# 	nothing_to_compare = driver.find_elements_by_xpath('//div[contains(@class, "blankslate")]')

		# 	# if fork is behind i.e. subset of work done on base
		# 	# switch the base
		# 	base_switch_button = driver.find_element_by_link_text('switching the base')
		# 	base_switch_button.click()
		# 	time.sleep(random_delay(5, 10))

		# 	# grab num commits behind, num files changed by base
		# 	commits_behind_elem = driver.find_element_by_xpath('//a[contains(@data-ga-click, "Compare, tabs, commits")]')
		# 	files_behind_elem = driver.find_element_by_xpath('//a[contains(@data-ga-click, "Compare, tabs, files")]')
			
		# 	base_urls_utd.append(base_url)
		# 	fork_links_utd.append(curr_forked_url)

		# 	if commits_behind_elem:
		# 		fork_commits_behind.append(number_pattern.search(commits_behind_elem.text).group(1))
		# 	else:
		# 		fork_commits_behind.append(None)
		# 	if files_behind_elem:
		# 		fork_files_changed.append(number_pattern.search(files_behind_elem.text).group(1))
		# 	else:
		# 		fork_files_changed.append(None)

		# 	# update subset forks per iteration
		# 	subset_forks_df = pd.DataFrame({
		# 		'Base': base_urls_utd,
		# 		'Fork UTD': fork_links_utd,
		# 		'Num Commits Behind': fork_commits_behind,
		# 		'Num Files Changed': fork_files_changed
		# 		})
		# 	subset_forks_df.to_csv('forks_behind_' + str(start_lim) + '.csv')
		# except:
		# 	# process later
		# 	base_urls_ahead.append(base_url)
		# 	fork_links_ahead.append(curr_forked_url)

		# 	# update process later per iteration
		# 	process_later_df = pd.DataFrame({'Base': base_urls_ahead, 'Fork Ahead': fork_links_ahead})
		# 	process_later_df.to_csv('forks_ahead_' + str(start_lim) + '.csv')

		fork_num += 1

		process_later_df = pd.DataFrame({'Base': base_urls_curr, 'Fork Compare': fork_compare_text})
		process_later_df.to_csv('fork_compare_text_' + str(start_lim) + '.csv')

driver.close()
