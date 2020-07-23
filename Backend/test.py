import sys
import turicreate as tc

candidates = tc.SFrame.read_csv('Data Creation/Data/candidate_data.csv')
projects = tc.SFrame.read_csv('Data Creation/Data/project_data.csv')

# Pretty print a user object's relevant information (candidates)
def user_string(user):
	result = 'USER %d: ' % user['Candidate UID'][0]

	attr = ['Talent Segment', 'Level', 'Skills', 'Local Office', 'Local Preference']
	for a in attr:
		result += ' ' + str(user[a][0])

	return result

# Pretty print an item object's relevant information (projects)
def item_string(item):
	result = '    ITEM %d:\t' % item['Project UID'][0]

	attr = ['Project Name', 'Level', 'Required Skills', 'Location', 'Local Requirement']
	for a in attr:
		result += ' ' + str(item[a][0])

	return result

# Print recommendations for the first 10 users
def print_test(*argv):
	# Load model
	model_name, ratings = None, None

	if '1' in argv[0]:
		model_name = 'recommendations.model1'
		ratings = tc.SFrame.read_csv('Data Creation/Data/model_data1.csv')
	elif '2' in argv[0]:
		model_name = 'recommendations.model2'
		ratings = tc.SFrame.read_csv('Data Creation/Data/model_data2.csv')
	else:
		print("Please specify which model (1 or 2)")
		return
	
	model = tc.load_model(model_name)
	training_data, validation_data = tc.recommender.util.random_split_by_user(ratings, 'Candidate UID', 'Project UID', max_num_users=200)

	# Make recommendations
	user_uids = [validation_data['Candidate UID'][i*5000] for i in range(10)]
	for u in user_uids:
		user = candidates[candidates['Candidate UID'] == u].unique()
		
		# Filter results by argument
		if len(argv[0]) != 0:
			items = projects['Project UID']
			if 'segment' in argv[0]:
				segment = str(user['Talent Segment'][0]) + ' Project'
				items = items[projects['Project Name'] == segment]
			else:
				# TODO: add other filters here
				pass
				
			recs = model.recommend(users=[str(u)], items=items)

		# Unfiltered results
		else:
			recs = model.recommend(users=[str(u)])

		print('\n', user_string(user))
		for rec in recs:
			item = projects[projects['Project UID'] == rec['Project UID']]
			print(item_string(item))

if __name__ == '__main__':
	print_test(sys.argv[1:])