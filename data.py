import random
from datetime import datetime

random.seed(datetime.now())

n_prof = 10
n_proj = 50

vars_fn = "filename_here"
prof_fn = "profile_data.csv"
proj_fn = "project_data.csv"

'''
TODO: load spreadsheet into Python
'''

profile_vars = dict()
'''
TODO: make data structure with all profile variables and values
ex. {'Service': ['Technology', 'Strategy & Consulting', 'Interactive', 'Operations'],
	 'Talent Segment': ['Account Leadership, Business', ...],
	 ...}
'''
with open(prof_fn, "w+") as profiles:
	for uid in range(n_prof):
		line = ""
		'''
		TODO: randomly select profile values from each profile variable
		and append to line separated by comma
		'''
		profiles.write(line + "\n")


project_vars = dict()
'''
TODO: make data structure with all project variables and values
ex. {'Chargeability': ['Yes', 'No'],
	 'Start Date': ['1/1/2020', '2/1/2020', ...],
	 ...}
'''
with open(proj_fn, "w+") as projects:
	for uid in range(n_proj):
		line = ""
		'''
		TODO: randomly select project values from each project variable
		and append to line separated by comma
		'''
		projects.write(line + "\n")