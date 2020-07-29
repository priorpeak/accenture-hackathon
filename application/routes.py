from flask import render_template, url_for, flash, redirect, jsonify, request
from application import app


@app.route('/')
@app.route('/home',methods=['GET','POST'])
def home():

    title_list = ["title1", "title2", "title3","title4","title5"]

    return render_template("home.html", len = len(title_list), title_list = title_list)

@app.route('/project_info', methods=['GET','POST'])
def project_info():
    response = request.get_json()
    id_number = response["categorytab"]
    
    title_list = ["1234", "qwer", "asdf","title4","title5"]
    print(request.method)
    print(id_number)
    print("hello")
    return render_template("request.html", tab = id_number, len = len(title_list), title_list = title_list)

