import random
from datetime import datetime
from openpyxl import load_workbook

def get_value(cell):
	return cell.value

random.seed(datetime.now())

n_cand = 1000
n_role = 5000

prof_fn = "candidate_data.csv"
proj_fn = "project_data.csv"

wb = load_workbook(filename='Dataset.xlsx')
ws = wb['Sheet1']

candidate_vars = dict()
role_vars = dict()

for col in ws.iter_cols(min_col=1, max_col=9, min_row=2):
	candidate_vars[col[0].value] = [i for i in map(get_value, col[1:]) if i is not None]

candidate_keys = candidate_vars.keys()

for col in ws.iter_cols(min_col=11, max_col=18, min_row=2):
	role_vars[col[0].value] = [i for i in map(get_value, col[1:]) if i is not None]

role_keys = role_vars.keys()

with open(prof_fn, "w+") as profiles:
	line = "UID,"
	for key in candidate_keys:
		line += key + ","
	line = line[:-1]
	profiles.write(line)

	for uid in range(n_cand):
		line = str(uid) + ","
		for key in candidate_keys:
			line += str(random.choice(candidate_vars[key])) + ","

		profiles.write("\n" + line[:-1])


with open(proj_fn, "w+") as projects:
	line = "UID,"
	for key in role_keys:
		line += key + ","
	line = line[:-1]
	projects.write(line)

	for uid in range(n_role):
		line = str(uid) + ","
		for key in role_keys:
			line += str(random.choice(role_vars[key])) + ","

		projects.write("\n" + line[:-1])