# Create a csv file of candidate-project ratings in the format necessary for the model
with open("Data/labeled_data_new.csv", "r") as ld:
	with open("Data/model_data_new.csv", "w+") as md:
		header = "Candidate UID, Project UID, Rating"
		md.write(header)
		cand_uid = 0
		for l in ld.readlines():
			ratings = l.split(",")
			proj_uid = 0
			for rating in ratings:
				new_rating = "1" if rating == "0" else "5"
				line = str(cand_uid) + "," + str(proj_uid) + "," + new_rating
				md.write("\n" + line)
				proj_uid += 1
			cand_uid += 1