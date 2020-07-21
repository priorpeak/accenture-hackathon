from datetime import datetime
import pandas as pd
import random

random.seed(datetime.now())

candidates_df = pd.read_csv("candidate_data.csv", header=0)
projects_df = pd.read_csv("project_data.csv", header=0)

def calc_match(candidate, project):
	probabilistic = {"Talent": False, "Skills": False, "Location": False, "Level": False}

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
	elif unmatched_skills == 1:
		skills_match = random.random() < 0.8
	elif unmatched_skills == 2:
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

	return talent_match and skills_match and location_match and level_match, probabilistic

with open("labeled_data.csv", "w+") as ld:
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


