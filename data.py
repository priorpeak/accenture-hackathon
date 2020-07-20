import random
from datetime import datetime
from openpyxl import load_workbook

random.seed(datetime.now())

# Set number of profiles and projects to generate for randomized dataset
n_prof = 10
n_proj = 50

# Input filenames to pull random data from
vars_fn = "filename_here"
prof_fn = "profile_data.csv"
proj_fn = "project_data.csv"

# Load sample data workbook
wb = load_workbook(filename = 'C:\Users\alexander.j.prior\OneDrive - Accenture\Desktop\Hackathon\accenture-hackathon\dataset.xlsx')
ws = wb['Sheet1']

# Randomly populate profile attributes from profile_data.csv
with open(prof_fn, "w+") as profiles:
	for uid in range(n_prof):
		line = ""
		profiles.write(line + "\n")

# Randomly populate project attributes from project_data.csv
with open(proj_fn, "w+") as projects:
	for uid in range(n_proj):
		line = ""
		projects.write(line + "\n")