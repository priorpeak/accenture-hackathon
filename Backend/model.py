import turicreate as tc

candidates = tc.SFrame.read_csv("Data Creation/Data/candidate_data.csv")
projects = tc.SFrame.read_csv("Data Creation/Data/project_data.csv")
ratings = tc.SFrame.read_csv("Data Creation/Data/model_data.csv")

training_data, validation_data = tc.recommender.util.random_split_by_user(ratings, 'Candidate UID', 'Project UID', max_num_users=200)
model = tc.factorization_recommender.create(training_data, user_id='Candidate UID', item_id='Project UID', target='Rating')

# user = validation_data['Candidate UID'][5001]
users = [validation_data['Candidate UID'][i*5000] for i in range(10)]
model.recommend(users=users).print_rows(num_rows=100)