import requests
from bs4 import BeautifulSoup
from bs4 import element
import re
import pandas as pd

wiki_open_source_page = requests.get('https://en.wikipedia.org/wiki/List_of_free_and_open-source_software_packages')
wiki_parsed = BeautifulSoup(wiki_open_source_page.content, 'html.parser')

new_list_pattern_1 = re.compile('Free [a-zA-Z -]* software')
new_list_pattern_2 = re.compile('List of [a-zA-Z -]* software')
open_source_projs = []
lists_to_parse = []
loop_break = False

uls = wiki_parsed.findAll('ul')
for ul in uls:
	for li in ul.findAll('li'):
		found_a = li.find('a')
		if found_a:
			inner_text = found_a.contents[0]
			# check if inner text contains html
			if type(inner_text) == element.NavigableString and inner_text[:7] != 'List of':
				open_source_projs.append(inner_text)
			if new_list_pattern_1.match(str(inner_text)) or new_list_pattern_2.match(str(inner_text)):
				lists_to_parse.append(inner_text)
			if str(inner_text) == 'The SWORD Project':
				loop_break = True
				break
	if loop_break:
		break

print('Projects')
print(open_source_projs)
print()
print('New lists')
print(lists_to_parse)

proj_df = pd.DataFrame({'Project': open_source_projs}).drop_duplicates(keep = 'first')
proj_df.to_csv("open_source_projs.csv")
