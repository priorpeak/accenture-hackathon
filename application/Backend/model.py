import sys
import turicreate as tc

candidates = tc.SFrame.read_csv('./Data Creation/Data/candidate_data.csv')
projects = tc.SFrame.read_csv('./Data Creation/Data/project_data.csv')

def get_talent_segment(user):
	return str(user['Talent Segment'][0])

def make_model(*argv):
	model_name, ratings = None, None

	if '1' in argv[0]:
		model_name = 'recommendations.model1'
		ratings = tc.SFrame.read_csv('./Data Creation/Data/model_data1.csv')
	elif '2' in argv[0]:
		model_name = 'recommendations.model2'
		ratings = tc.SFrame.read_csv('./Data Creation/Data/model_data2.csv')
	elif '3' in argv[0]:
		model_name = 'recommendations.model3'
		ratings = tc.SFrame.read_csv('./Data Creation/Data/model_data2.csv')		
	else:
		print("Please specify which model (1, 2, 3)")
		quit()
	
	training_data, validation_data = tc.recommender.util.random_split_by_user(ratings, 'Candidate UID', 'Project UID', max_num_users=200)
	model = tc.ranking_factorization_recommender.create(training_data, \
												user_id='Candidate UID', \
												item_id='Project UID', \
												target='Rating', \
												user_data=candidates)
	model.save(model_name)

if __name__ == '__main__':
	make_model(sys.argv[1:])