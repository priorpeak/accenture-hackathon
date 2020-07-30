from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'ji32k7au4a832'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../Team4_sensor.db'
#dbflask = SQLAlchemy(app)




from application import routes
