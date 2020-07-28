from datetime import datetime
import json
import turicreate as tc



### HELPER FUNCTIONS ###

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



### MAIN FUNCTIONS ###

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
			  "location_filter": <LOCATION_BOOL>
			}'

			- If a filter is not being applied, then the list for the filter will be empty (except
			  the skills filter, which is a bool)
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

	Returns:
		JSON string in the format
			'{"user": <USER_UID>,
			  "projects": [0, 14, 135, 647],
			  "0": {
					"start_date": "<DATE>",
					"end_date": "<DATE>",
					"client": "<CLIENT>",
					"name": "<NAME>",
					"skills": ["<SKILL_1>", "<SKILL_2>", ...],
					"location": "<LOCATION>",
					"loc_requirement": <LOC_REQ>
			  }
			}'

			- DATE (str): in the format '2020-01-31'
			- LOC_REQ (str): 'Yes' if there is a local requirement, 'No' otherwise

	'''
	# Data variables
	candidates = tc.SFrame.read_csv('./Data Creation/Data/candidate_data.csv')
	projects = tc.SFrame.read_csv('./Data Creation/Data/project_data.csv')

	model_name = 'recommendations.model1'
	ratings = tc.SFrame.read_csv('./Data Creation/Data/model_data1.csv')


	# Parse the JSON string and extract required information
	request = json.loads(json_string)
	user_uid = int(request['user'])
	service = str(request['service'])

	# Track any additional filters that were passed into the function
	segment_filter = request['segment_filter']
	skills_filter = request['skills_filter']
	level_filter = request['level_filter']
	location_filter = request['location_filter']

	# TODO: assert that filters are all correct types

	# Load the ML model and user object from turicreate
	model = tc.load_model(model_name)
	user = candidates[candidates['Candidate UID'] == int(user_uid)].unique()

	# Filter results by service
	items = projects

	# # TODO: Add column for service spec in projects data
	# items = items[items['Service'] == service]

	# TODO: Filter by start dates that occur after the user becomes free

	# Deal with binary filters (skills and location)
	if skills_filter:
		items = items[items.apply(lambda x: contains_skills(user, x))]
		# By default, apply no filter

	if location_filter:
		items = items[items.apply(lambda x: location_match(user, x))]
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

	# Deal with level filter
	if len(level_filter) > 0:
		lesser = min(level_filter)
		greater = max(level_filter)
		items = items[items.apply(lambda x: in_range(lesser, greater, x))]
	else:
		# By default, filter by the user's current level as greater and two higher as lesser
		user_level = int(user['Level'][0])
		items = items[items.apply(lambda x: in_range(user_level - 2, user_level, x))]

	recs = model.recommend([user_uid], items=items['Project UID'])

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
					'skills': str(rec['Required Skills'][0]).split('/')[:-1], \
					'location': rec['Location'][0], \
					'loc_requirement': rec['Local Requirement'][0]}

		projects_list.append(project_uid)
		response[key] = contents

	response['projects'] = projects_list

	return response

# For testing
if __name__ == '__main__':
	json_string = '{"user": 0,' + \
			  '"service": "Technology",' + \
			  '"segment_filter": ["Security", "Engineering"],' + \
			  '"skills_filter": true,' + \
			  '"level_filter": [],' + \
			  '"location_filter": true' + \
			'}'
	print(preferences_for_user(json_string))

