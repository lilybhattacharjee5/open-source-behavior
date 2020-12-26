import pandas as pd 

open_source_projs = pd.read_csv('open_source_projs.csv')

invalid_proj_names = [
	'Data Mining',
	'R programming language',
	'Environment for DeveLoping KDD-Applications Supported by Index-Structures (ELKI)',
	'Konstanz Information Miner (KNIME)',
	'Orange (software)',
	'RCA open-source application',
	
]
open_source_projs = open_source_projs.loc[!open_source_projs['Project'].isin()]

open_source_projs.to_csv('clean_open_source_projs.csv')