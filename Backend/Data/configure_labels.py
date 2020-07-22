with open("labeled_data.csv", "r") as ld:
	with open("model_data.csv", "w+") as md:
		header = "Candidate UID, Project UID, Rating"
		md.write(header)
		cand_uid = 0
		for l in ld.readlines():
			ratings = l.split(",")
			proj_uid = 0
			for rating in ratings:
				line = str(cand_uid) + "," + str(proj_uid) + "," + rating
				md.write("\n" + line)
				proj_uid += 1
			cand_uid += 1

			

