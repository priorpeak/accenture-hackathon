import turicreate as tc

candidates = tc.SFrame.read_csv("Data/candidate_data.csv")
projects = tc.SFrame.read_csv("Data/project_data.csv")
ratings = tc.SFrame.read_csv("Data/model_data.csv")

training_data, validation_data = tc.recommender.util.random_split_by_user(ratings, 'Candidate UID', 'Project UID', max_num_users=200)
model = tc.factorization_recommender.create(training_data, user_id='Candidate UID', item_id='Project UID', target='Rating')

print(model.recommend(users=validation_data['Candidate UID'][:10]))
# print(model.evaluate(validation_data))