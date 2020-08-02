from datetime import datetime
import json
import pickle
import sys
import time
import turicreate as tc

candidates = tc.SFrame.read_csv('./application/Backend/Data Creation/Data/candidate_data_new.csv')
projects = tc.SFrame.read_csv('./application/Backend/Data Creation/Data/project_data_new.csv')

model_name = './application/Backend/recommendations.model'
ratings = tc.SFrame.read_csv('./application/Backend/Data Creation/Data/model_data_new.csv')

db_fn = './application/Backend/savedProjects'

json_string = '{"user": 0,' + \
              '"service": "",' + \
              '"segment_filter": [],' + \
              '"skills_filter": true,' + \
              '"level_filter": [],' + \
              '"location_filter": false' + \
            '}'

### HELPER FUNCTIONS ###

def date_match(user, item):
	'''
	Determines if a user becomes free before the start date of the item
	'''

	date_free = datetime.fromisoformat(str(user['Coming Available'][0]))
	start_date = datetime.fromisoformat(str(item['Start Date']))

	return date_free < start_date

def contains_skills(user, item):
	'''
	Determines if a user has all the required skills of an item
	'''
	user_skills = set(str(user['Skills'][0]).split('/')[:-1])
	item_skills = set(str(item['Required Skills']).split('/')[:-1])

	if item_skills.issubset(user_skills):
		return True
	
	return False

def location_match(user, item):
	'''
	Determines whether candidate and project preferences are compliant/matching
	'''
	return user['Local Office'][0] == item['Location'][0] or \
		   user['Local Preference'][0] == 'No' and item['Local Requirement'][0] == 'No'

def in_range(lesser, greater, item):
	'''
	Determines whether a project falls within a specified level range
	'''
	item_level = int(item['Level'][0][0]) # If the level range is 4-5, takes 4

	return lesser <= item_level + 1 and greater >= item_level

def make_db():
	'''
	Make the pickled database.
	'''
	global db_fn

	db = dict()
	for i in range(1001):
		db[str(i)] = set()
	dbfile = open(db_fn, 'wb')

	pickle.dump(db, dbfile)
	dbfile.close()

def format_user(user):
	'''
	Format string for terminal printing.
	'''
	uid = str(user['Candidate UID'][0])
	coming_avail = str(user['Coming Available'][0]).split(' ')[0]
	level = str(user['Level'][0])
	office = str(user['Local Office'][0])
	loc_pref = str(user['Local Preference'][0])
	service = str(user['Service'][0])
	skills = list(set(str(user['Skills'][0]).split('/')[:-1]))
	segment = str(user['Talent Segment'][0])

	result = "USER\tSERVICE\t\tTALENT SEG\tLEVEL\tCOMING AVAIL\tOFFICE\tLOCAL PREF\tSKILLS\n"
	result += "%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s" \
				% (uid, service, segment, level, coming_avail, office, loc_pref, skills)

	return result

def format_preferences(prefs):
	'''
	Format preferences dict for terminal printing
	'''
	result = "RANK\tPROJ\tSERVICE\t\tNAME\t\t\tLEVEL\tCLIENT\tSTART DATE\tEND DATE\tLOCATION\tLOC REQ\tSKILLS\n"
	rank = 1

	for project_uid in prefs['projects']:
		uid = str(project_uid)
		service = str(prefs[uid]['service'])[:12]
		name = str(prefs[uid]['name'])
		level = str(prefs[uid]['level'])
		client = str(prefs[uid]['client'])
		start = str(prefs[uid]['start_date'])
		end = str(prefs[uid]['end_date'])
		location = str(prefs[uid]['location'])
		loc_req = str(prefs[uid]['loc_requirement'])
		skills = str(prefs[uid]['skills'])
		result += "%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s\t%s\n" \
					% (rank, uid, service, name, level, client, start, end, location, loc_req, skills)
		rank += 1

	return result[:-1]



### MAIN FUNCTIONS ###

def store_preferences(json_string):
	'''
	Store preferences to load into routes.py
	'''
	preference_file = open('./application/Backend/preferences', 'wb+')
	preferences = preferences_for_user(json_string)

	pickle.dump(preferences, preference_file)
	preference_file.close()

def get_preferences():
	with open('./application/Backend/preferences', 'rb') as file:
		prefs = pickle.load(file)

		return prefs

def store_project(user_uid, project_uid):
	'''
	Stores project as "saved" under user.
	'''
	global db_fn

	dbfile = open(db_fn, 'rb')
	db = pickle.load(dbfile)
	dbfile.close()

	dbfile = open(db_fn, 'wb')
	
	user = str(user_uid)
	if user in db:
		db[user].add(int(project_uid))
	else:
		db[user] = [int(project_uid)]

	pickle.dump(db, dbfile)
	dbfile.close()

def lookup_saved(user_uid):
	'''
	Looks up all saved projects of a user.
	'''
	global db_fn

	with open(db_fn, 'rb') as dbfile:
		db = pickle.load(dbfile)

		return db[str(user_uid)]

def saved_projects_information(user_uid):
	'''
	Takes in a user UID and returns information for each saved project for that user.
	'''
	global projects

	project_uids = lookup_saved(user_uid)

	def in_uids(item):
		return item['Project UID'] in project_uids

	items = projects[projects.apply(lambda x: in_uids(x))]

	response = dict()
	projects_list = list()
	for item in items:
		project_uid = int(item['Project UID'])
		key = str(project_uid)

		rec = projects[projects['Project UID'] == project_uid].unique()

		contents = {'start_date': rec['Start Date'][0].split(' ')[0], \
					'end_date': rec['End Date'][0].split(' ')[0], \
					'client': rec['Client'][0], \
					'name': rec['Project Name'][0], \
					'skills': list(set(str(rec['Required Skills'][0]).split('/')[:-1])), \
					'location': rec['Location'][0], \
					'loc_requirement': rec['Local Requirement'][0], \
					'level': rec['Level'][0], \
					'service': rec['Service'][0]}

		projects_list.append(project_uid)
		response[key] = contents

	response['projects'] = projects_list

	return response

def preferences_for_user(json_string):
	'''
	Takes in a request for a user's preferences (specified by user UID) and returns a JSON string
	with recommended projects' UIDs and details. A maximum of 10 recommended projects are returned
	at a time.

	Args:
		json_string (str): The details of the request in the format
			'{"user": <USER_UID>,
			  "service": "<SERVICE>",
			  "segment_filter": ["<SEGMENT_1>", "<SEGMENT_2>", ...],
			  "skills_filter": <SKILLS_BOOL>,
			  "level_filter": [<LOW_LVL>, <HIGH_LVL>],
			  "location_filter": <LOCATION_BOOL>,
			  "n": <NUM_RECS>
			}'

			- If a filter is not being applied, then the list for the filter will be empty (except
			  the skills and location filters, which are bool values)
			- Default filters when a filter is not specified are recorded in the function body below

			- USER_UID (int): from range [0,999]
			- SERVICE (str): one of {"Technology", "Strategy", "Interactive", "Operations"}
			- SEGMENT (str): one of {"Account Leadership", "Business", "Design", "Engineering",
			  "Finance", "Human Resources", "IT Operations", "Legal", "Security", "Strategy"}
			- SKILLS_BOOL (bool): true if looking for perfect skills match, false otherwise
			- LOW_LVL / HIGH_LVL (int): from range [1, 11]
				* LOW_LVL = HIGH_LVL if you only want to filter for one level
				* No spec for LOW_LVL < HIGH_LVL or LOW_LVL > HIGH_LVL; will be handled in function
			- LOCATION_BOOL (bool): true if looking for compliant locations, false otherwise
			- NUM_RECS (int): number of recommendations wanted (if not specified, set to 10)

	Returns:
		JSON string in the format
			'{"user": <USER_UID>,
			  "projects": [0, 14, 135, 647, ...],
			  "0": {
					"start_date": "<DATE>",
					"end_date": "<DATE>",
					"client": "<CLIENT>",
					"name": "<NAME>",
					"skills": ["<SKILL_1>", "<SKILL_2>", ...],
					"location": "<LOCATION>",
					"loc_requirement": <LOC_REQ>,
					"level": "<LEVEL_RANGE>",
					"service": "<SERVICE>"
			  },
			  "14": {
					 ...,
			  },
			  ...
			}'

			- DATE (str): in the format '2020-01-31'
			- LOC_REQ (str): 'Yes' if there is a local requirement, 'No' otherwise

	'''
	# Data variables
	global candidates, projects, model_name, ratings

	# Parse the JSON string and extract required information
	request = json.loads(json_string)
	user_uid = int(request['user'])
	service = str(request['service'])
	if 'n' in request:
		n = int(request['n'])
	else:
		n = 10 # Default to making 10 new recommendations

	# Track any additional filters that were passed into the function
	segment_filter = request['segment_filter']
	skills_filter = request['skills_filter']
	level_filter = request['level_filter']
	location_filter = request['location_filter']

	# TODO: assert that filters are all correct types

	# Load the ML model and user object from turicreate
	model = tc.load_model(model_name)
	user = candidates[candidates['Candidate UID'] == int(user_uid)].unique()

	items = projects

	# Filter results by service
	if service != '':
		items = items[items['Service'] == service]
	# print("**", len(items))

	# Filter by start dates that occur after the user becomes free
	items = items[items.apply(lambda x: date_match(user, x))]
	# print("***", len(items))

	# Deal with binary filters (skills and location)
	if skills_filter:
		items = items[items.apply(lambda x: contains_skills(user, x))]
		# print("****", len(items))
		# By default, apply no filter

	if location_filter:
		items = items[items.apply(lambda x: location_match(user, x))]
		# print("*****", len(items))
		# By default, apply no filter

	# Deal with talent segment filter
	if len(segment_filter) > 0:
		for seg in segment_filter:
			project_name = seg + ' Project'
			items = items[items['Project Name'] == project_name]
	else:
		# By default, filter by the user's talent segment
		project_name = str(user['Talent Segment'][0]) + ' Project'
		items = items[items['Project Name'] == project_name]
	# print("******", len(items))

	# Deal with level filter
	if len(level_filter) > 0:
		lesser = min(level_filter)
		greater = max(level_filter)
		items = items[items.apply(lambda x: in_range(lesser, greater, x))]
	else:
		# By default, filter by the user's current level as greater and two higher as lesser
		user_level = int(user['Level'][0])
		items = items[items.apply(lambda x: in_range(user_level - 2, user_level, x))]
	# print("*******", len(items))

	recs = model.recommend([user_uid], items=items['Project UID'], exclude_known = False, k=n)

	# Format response
	response = {'user': user_uid}
	projects_list = list()
	for r in recs:
		project_uid = int(r['Project UID'])
		key = str(project_uid)

		rec = projects[projects['Project UID'] == project_uid].unique()
		contents = {'start_date': rec['Start Date'][0].split(' ')[0], \
					'end_date': rec['End Date'][0].split(' ')[0], \
					'client': rec['Client'][0], \
					'name': rec['Project Name'][0], \
					'skills': list(set(str(rec['Required Skills'][0]).split('/')[:-1])), \
					'location': rec['Location'][0], \
					'loc_requirement': rec['Local Requirement'][0], \
					'level': rec['Level'][0], \
					'service': rec['Service'][0]}

		projects_list.append(project_uid)
		response[key] = contents

	response['projects'] = projects_list

	return response

# For recording
if __name__ == '__main__':
	# args = sys.argv[1:]

	# user_uid = int(args[0])
	# skills_filter = str(args[1])

	# user = candidates[candidates['Candidate UID'] == int(user_uid)].unique()
	# user_service = user['Service'][0]

	# json_string = '{"user": %d,' % user_uid + \
	# 		  '"service": "%s",' % user_service + \
	# 		  '"segment_filter": [],' + \
	# 		  '"skills_filter": %s,' % skills_filter + \
	# 		  '"level_filter": [],' + \
	# 		  '"location_filter": false' + \
	# 		'}'

	# time.sleep(2)
	# print()
	# print("------------------------------------------------------")
	# print("------------------------------------------------------")
	# print("Serving recommendations for User with UID %d" % user_uid)
	# print("------------------------------------------------------")
	# print("------------------------------------------------------")

	# time.sleep(2)
	# print(format_user(user))

	# print("------------------------------------------------------")
	# print("------------------------------------------------------")
	
	# prefs = preferences_for_user(json_string)
	# print(format_preferences(prefs))
	# print("------------------------------------------------------")
	# print("------------------------------------------------------")

	make_db()

