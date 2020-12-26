from selenium import webdriver
from utils import random_delay
import pandas as pd
import time
import regex as re

main_proj_url_format = re.compile('(https:\/\/github\.com\/[^\/]+\/[^\/]+\/)')

driver = webdriver.Firefox()
driver.get('https://github.com/MunGell/awesome-for-beginners')

assert 'GitHub' in driver.title

time.sleep(random_delay(1, 3))

proj_link_elements = driver.find_elements_by_xpath('//a[contains(@href, "/labels/")]')
proj_names = [i.text for i in proj_link_elements]
proj_links = [str(main_proj_url_format.search(i.get_attribute('href')).group(1)) for i in proj_link_elements]

print(proj_names)
print(proj_links)

assert len(proj_names) == len(proj_links)

print(len(proj_names))

proj_df = pd.DataFrame({'Project Name': proj_names, 'Project Link': proj_links}).drop_duplicates(keep = 'first')
proj_df.to_csv("awesome_open_source_projs.csv")

driver.close()
