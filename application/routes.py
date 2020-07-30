from flask import render_template, url_for, flash, redirect, jsonify, request
from application import app


@app.route('/')
@app.route('/home',methods=['GET','POST'])
def home():

    title_list = ["title1", "title2", "title3","title4","title5"]
    start_date = "2020-08-01"
    end_date = "2020-12-31"
    client = "Facebook"
    name = "This Project Title"
    skills = ["C", "Java"]
    location = "San Fransisco"
    loc_requirement = "yes"
    info = [("start_date",start_date),("end_date",end_date)]
    print (info)
    return render_template("home.html", len = len(title_list), title_list = title_list, start_date = start_date, end_date = end_date,name = name)

@app.route('/project_info', methods=['GET','POST'])
def project_info():
    response = request.get_json()
    id_number = response["categorytab"]
    title_list = ["filter1", "filter2", "filter3","filter4","filter5"]
    start_date = "2020-08-01"
    end_date = "2020-12-31"
    client = "Facebook"
    name = "This Project Title"
    skills = ["C", "Java"]
    location = "San Fransisco"
    loc_requirement = "yes"
    info = [{'user': 0, '1683': {'start_date': '2020-07-01', 'end_date': '2020-07-15', 'client': 'B', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'NYC', 'loc_requirement': 'No'}, '4286': {'start_date': '2020-12-01', 'end_date': '2020-12-15', 'client': 'F', 'name': 'Strategy Project', 'skills': ['Excel'], 'location': 'Chicago', 'loc_requirement': 'No'}, '1368': {'start_date': '2020-10-01', 'end_date': '2020-12-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Excel'], 'location': 'Chicago', 'loc_requirement': 'No'}, '2266': {'start_date': '2020-12-01', 'end_date': '2020-12-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Critical thinking', 'Critical thinking', 'Critical thinking'], 'location': 'Boston', 'loc_requirement': 'No'}, '2044': {'start_date': '2020-07-01', 'end_date': '2020-07-15', 'client': 'B', 'name': 'Strategy Project', 'skills': ['Excel', 'Excel', 'Excel'], 'location': 'NYC', 'loc_requirement': 'No'}, '4464': {'start_date': '2020-06-01', 'end_date': '2020-11-15', 'client': 'A', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'DC', 'loc_requirement': 'Yes'}, '53': {'start_date': '2020-06-01', 'end_date': '2020-09-15', 'client': 'A', 'name': 'Strategy Project', 'skills': ['Excel', 'Excel'], 'location': 'Denver', 'loc_requirement': 'Yes'}, '4038': {'start_date': '2020-06-01', 'end_date': '2020-12-15', 'client': 'H', 'name': 'Strategy Project', 'skills': ['Critical thinking', 'Excel', 'Excel'], 'location': 'Chicago', 'loc_requirement': 'Yes'}, '42': {'start_date': '2020-11-01', 'end_date': '2020-11-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'NYC', 'loc_requirement': 'No'}, '3253': {'start_date': '2020-06-01', 'end_date': '2020-07-15', 'client': 'C', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'Chicago', 'loc_requirement': 'No'}, 'projects': [1683, 4286, 1368, 2266, 2044, 4464, 53, 4038, 42, 3253]}]
    return render_template("request.html", tab = id_number, len = len(title_list), title_list = title_list, info = info)

