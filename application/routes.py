import sys

from flask import Flask, render_template, url_for, flash, redirect, jsonify, request
from application import app

from application.Backend import run


filter_list = []
saved_project_list=[]
@app.route('/')
@app.route('/home',methods=['GET','POST'])
def home():
    json_string = '{"user": 0,' + \
              '"service": "Technology",' + \
              '"segment_filter": [],' + \
              '"skills_filter": true,' + \
              '"level_filter": [],' + \
              '"location_filter": false' + \
            '}'

    # response = run.preferences_for_user(json_string)
    #test responses
    response = {'user': 0, '1683': {'start_date': '2020-07-01', 'end_date': '2020-07-15', 'client': 'B', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'NYC', 'loc_requirement': 'No'}, '4286': {'start_date': '2020-12-01', 'end_date': '2020-12-15', 'client': 'F', 'name': 'Strategy Project', 'skills': ['Excel'], 'location': 'Chicago', 'loc_requirement': 'No'}, '1368': {'start_date': '2020-10-01', 'end_date': '2020-12-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Excel'], 'location': 'Chicago', 'loc_requirement': 'No'}, '2266': {'start_date': '2020-12-01', 'end_date': '2020-12-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Critical thinking', 'Critical thinking', 'Critical thinking'], 'location': 'Boston', 'loc_requirement': 'No'}, '2044': {'start_date': '2020-07-01', 'end_date': '2020-07-15', 'client': 'B', 'name': 'Strategy Project', 'skills': ['Excel', 'Excel', 'Excel'], 'location': 'NYC', 'loc_requirement': 'No'}, '4464': {'start_date': '2020-06-01', 'end_date': '2020-11-15', 'client': 'A', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'DC', 'loc_requirement': 'Yes'}, '53': {'start_date': '2020-06-01', 'end_date': '2020-09-15', 'client': 'A', 'name': 'Strategy Project', 'skills': ['Excel', 'Excel'], 'location': 'Denver', 'loc_requirement': 'Yes'}, '4038': {'start_date': '2020-06-01', 'end_date': '2020-12-15', 'client': 'H', 'name': 'Strategy Project', 'skills': ['Critical thinking', 'Excel', 'Excel'], 'location': 'Chicago', 'loc_requirement': 'Yes'}, '42': {'start_date': '2020-11-01', 'end_date': '2020-11-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'NYC', 'loc_requirement': 'No'}, '3253': {'start_date': '2020-06-01', 'end_date': '2020-07-15', 'client': 'C', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'Chicago', 'loc_requirement': 'No'}, 'projects': [1683, 4286, 1368, 2266, 2044, 4464, 53, 4038, 42, 3253]}
    #test responses
    ids = []
    start_date = []
    end_date = []
    client = []
    name = []
    skills = []
    location = []
    loc_requirement = []

    for project in response['projects']:
        ids.append(str(project))
        start_date.append(response[str(project)]['start_date'])
        end_date.append(response[str(project)]['end_date'])
        client.append(response[str(project)]['client'])
        name.append(response[str(project)]['name'])
        skills.append(response[str(project)]['skills'])
        location.append(response[str(project)]['location'])
        loc_requirement.append(response[str(project)]['loc_requirement'])

    return render_template("home.html", ids = ids, skills = skills, len = len(name), client = client, start_date = start_date, end_date = end_date,name = name, loc_requirement = loc_requirement, location = location)


@app.route('/saved_projects', methods=['GET','POST'])
def saved_info():
    response = request.get_json()
    id_number = response["id"]
    if (id_number != 'N/A'):
       saved_project_list.append(id_number)
    print(saved_project_list)


    #input: saved_project_list (list of all the id of projects saved in front-end)
    #output: response, all projects that correspond to the ids

    #test responses
    response = {'user': 0, '1683': {'start_date': '2020-07-01', 'end_date': '2020-07-15', 'client': 'B', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'NYC', 'loc_requirement': 'No'}, '4286': {'start_date': '2020-12-01', 'end_date': '2020-12-15', 'client': 'F', 'name': 'Strategy Project', 'skills': ['Excel'], 'location': 'Chicago', 'loc_requirement': 'No'}, '1368': {'start_date': '2020-10-01', 'end_date': '2020-12-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Excel'], 'location': 'Chicago', 'loc_requirement': 'No'}, '2266': {'start_date': '2020-12-01', 'end_date': '2020-12-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Critical thinking', 'Critical thinking', 'Critical thinking'], 'location': 'Boston', 'loc_requirement': 'No'}, '2044': {'start_date': '2020-07-01', 'end_date': '2020-07-15', 'client': 'B', 'name': 'Strategy Project', 'skills': ['Excel', 'Excel', 'Excel'], 'location': 'NYC', 'loc_requirement': 'No'}, '4464': {'start_date': '2020-06-01', 'end_date': '2020-11-15', 'client': 'A', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'DC', 'loc_requirement': 'Yes'}, '53': {'start_date': '2020-06-01', 'end_date': '2020-09-15', 'client': 'A', 'name': 'Strategy Project', 'skills': ['Excel', 'Excel'], 'location': 'Denver', 'loc_requirement': 'Yes'}, '4038': {'start_date': '2020-06-01', 'end_date': '2020-12-15', 'client': 'H', 'name': 'Strategy Project', 'skills': ['Critical thinking', 'Excel', 'Excel'], 'location': 'Chicago', 'loc_requirement': 'Yes'}, '42': {'start_date': '2020-11-01', 'end_date': '2020-11-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'NYC', 'loc_requirement': 'No'}, '3253': {'start_date': '2020-06-01', 'end_date': '2020-07-15', 'client': 'C', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'Chicago', 'loc_requirement': 'No'}, 'projects': [1683, 4286, 1368, 2266, 2044, 4464, 53, 4038, 42, 3253]}
    #test responses

    ids = []
    start_date = []
    end_date = []
    client = []
    name = []
    skills = []
    location = []
    loc_requirement = []

    for project in response['projects']:
        ids.append(str(project))
        start_date.append(response[str(project)]['start_date'])
        end_date.append(response[str(project)]['end_date'])
        client.append(response[str(project)]['client'])
        name.append(response[str(project)]['name'])
        skills.append(response[str(project)]['skills'])
        location.append(response[str(project)]['location'])
        loc_requirement.append(response[str(project)]['loc_requirement'])

    #test responses
    name[1] = "saved result 1"
    name[0] = "saved result 2"
    #test responses

    return render_template("saved.html",ids = ids, skills = skills, len = len(name), client = client, start_date = start_date, end_date = end_date,name = name, loc_requirement = loc_requirement, location = location, )





@app.route('/project_info', methods=['GET','POST'])
def project_info():

    response = request.get_json()
    categories = response["categorytab"]
    checked = response["checked"]
    if categories in filter_list:
        filter_list.remove(categories)
    else:
        filter_list.append(categories)


    #input: filter_list (list of categories checked in front-end)
    #output: response, all projects that correspond to the categories
    print(filter_list)
    
    #page refresh, filter must refresh as well: need a solution

    
    #test responses
    response = {'user': 0, '1683': {'start_date': '2020-07-01', 'end_date': '2020-07-15', 'client': 'B', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'NYC', 'loc_requirement': 'No'}, '4286': {'start_date': '2020-12-01', 'end_date': '2020-12-15', 'client': 'F', 'name': 'Strategy Project', 'skills': ['Excel'], 'location': 'Chicago', 'loc_requirement': 'No'}, '1368': {'start_date': '2020-10-01', 'end_date': '2020-12-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Excel'], 'location': 'Chicago', 'loc_requirement': 'No'}, '2266': {'start_date': '2020-12-01', 'end_date': '2020-12-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Critical thinking', 'Critical thinking', 'Critical thinking'], 'location': 'Boston', 'loc_requirement': 'No'}, '2044': {'start_date': '2020-07-01', 'end_date': '2020-07-15', 'client': 'B', 'name': 'Strategy Project', 'skills': ['Excel', 'Excel', 'Excel'], 'location': 'NYC', 'loc_requirement': 'No'}, '4464': {'start_date': '2020-06-01', 'end_date': '2020-11-15', 'client': 'A', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'DC', 'loc_requirement': 'Yes'}, '53': {'start_date': '2020-06-01', 'end_date': '2020-09-15', 'client': 'A', 'name': 'Strategy Project', 'skills': ['Excel', 'Excel'], 'location': 'Denver', 'loc_requirement': 'Yes'}, '4038': {'start_date': '2020-06-01', 'end_date': '2020-12-15', 'client': 'H', 'name': 'Strategy Project', 'skills': ['Critical thinking', 'Excel', 'Excel'], 'location': 'Chicago', 'loc_requirement': 'Yes'}, '42': {'start_date': '2020-11-01', 'end_date': '2020-11-15', 'client': 'G', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'NYC', 'loc_requirement': 'No'}, '3253': {'start_date': '2020-06-01', 'end_date': '2020-07-15', 'client': 'C', 'name': 'Strategy Project', 'skills': ['Critical thinking'], 'location': 'Chicago', 'loc_requirement': 'No'}, 'projects': [1683, 4286, 1368, 2266, 2044, 4464, 53, 4038, 42, 3253]}
    #test responses


    ids = []
    start_date = []
    end_date = []
    client = []
    name = []
    skills = []
    location = []
    loc_requirement = []

    for project in response['projects']:
        ids.append(str(project))
        start_date.append(response[str(project)]['start_date'])
        end_date.append(response[str(project)]['end_date'])
        client.append(response[str(project)]['client'])
        name.append(response[str(project)]['name'])
        skills.append(response[str(project)]['skills'])
        location.append(response[str(project)]['location'])
        loc_requirement.append(response[str(project)]['loc_requirement'])

    #test responses
    name[1] = "filter_result1"
    name[0] = "filter result 2"
    #test responses





    return render_template("request.html",ids = ids, skills = skills, len = len(name), client = client, start_date = start_date, end_date = end_date,name = name, loc_requirement = loc_requirement, location = location, )
