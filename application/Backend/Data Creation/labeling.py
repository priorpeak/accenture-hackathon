from datetime import datetime
import pandas as pd
import random

random.seed(datetime.now())

candidates_df = pd.read_csv("Data/candidate_data_new.csv", header=0)
projects_df = pd.read_csv("Data/project_data_new.csv", header=0)

# Determine if a project is a good match for a candidate (returns True, False)
def calc_match(candidate, project):
	probabilistic = {"Talent": False, "Skills": False, "Location": False, "Level": False}

	# SERVICE
	service = candidate.get("Service") == project.get("Service")

	# TALENT SEGMENT
	talent_match = candidate.get("Talent Segment") in project.get("Project Name")

	# SKILLS
	skills_match = False
	cand_skills = set(candidate.get("Skills").split("/"))
	proj_skills = project.get("Required Skills").split("/")
	unmatched_skills = len(proj_skills)

	for skill in proj_skills:
		if skill in cand_skills:
			unmatched_skills -= 1

	if unmatched_skills == 0:
		skills_match = True
	elif unmatched_skills / len(proj_skills) < 0.34:
		skills_match = random.random() < 0.5
	else:
		skills_match = random.random() < 0.1

	if unmatched_skills != 0 and skills_match:
		probabilistic["Skills"] = True

	# LOCATION
	location_match = candidate.get("Local Office") == project.get("Location") or \
					 candidate.get("Local Preference") == "No" and project.get("Local Requirement") == "No"
	if not location_match:
		if project.get("Local Requirement") == "Yes":
			location_match = random.random() < 0.05
		else:
			location_match = random.random() < 0.5

		if location_match:
			probabilistic["Location"] = True

	# LEVEL
	level_match = False
	cand_level = int(candidate.get("Level"))
	proj_level = int(project.get("Level")[-1])
	if proj_level >= cand_level:
		level_match = True
	elif abs(proj_level - cand_level) <= 2:
		level_match = random.random() < 0.25
		probabilistic["Level"] = True

	return service and talent_match and skills_match and location_match and level_match, probabilistic

# Create csv file where rows are candidates and columns are projects (0 = no match, 1 = match)
with open("Data/labeled_data_new.csv", "w+") as ld:
	for c in candidates_df.iterrows():
		cand = c[1]
		elems = []

		for p in projects_df.iterrows():
			proj = p[1]

			match, probabilistic = calc_match(cand, proj)
			if match:
				elems.append("1")
			else:
				elems.append("0")

		line = ",".join(elems)
		ld.write("\n" + line)
		print(c[0])


