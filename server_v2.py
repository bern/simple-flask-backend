from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import argparse
import sys

parser = argparse.ArgumentParser()

#-addr ADDRESS -u USERNAME -p PASSWORD
parser.add_argument("-addr", "--address", help="Database address", default="")
parser.add_argument("-db", "--database", help="Database name", default="")
parser.add_argument("-u", "--username", help="User name", default="")
parser.add_argument("-p", "--password", help="Password", default="")

args = parser.parse_args()

if (args.address == ""):
    sys.exit("missing db address")
elif (args.database == ""):
    sys.exit("missing db name")
elif (args.username == ""):
    sys.exit("missing db username")
elif (args.password == ""):
    sys.exit("missing db password")

dburi = "mongodb://" + args.username + ":" + args.password + "@" + args.address

# Create our Flask app
app = Flask(__name__)

# Add MONGO_DBNAME and MONGO_URI to our app config
app.config['MONGO_DBNAME'] = args.database
app.config['MONGO_URI'] = dburi

# Feed app into PyMongo() to generate a db connection
mongo = PyMongo(app)

@app.route('/students', methods=['GET'])
def get_all_students():
  roster = mongo.db['class-roster']
  # Example of request.args.get()
  output = []
  for student in roster.find():
    print student
    output.append({'_id': str(student['_id']), 'name' : student['name'], 'gator_one' : student['gator_one']})
  return jsonify({'result' : output})

@app.route('/students', methods=['POST'])
def add_student():
  roster = mongo.db['class-roster']
  name = request.json['name']
  gator_one = request.json['gator_one']
  db_id = roster.insert({'name': name, 'gator_one': gator_one})
  student = roster.find_one({'_id': db_id})
  output = {'_id': str(student['_id']), 'name': student['name'], 'gator_one': student['gator_one']}
  return jsonify({'result': output})

# Use type hints to define custom URLs
@app.route('/students/<string:id>', methods=['DELETE'])
def delete_student(id):
  roster = mongo.db['class-roster']
  roster.delete_one({'_id': ObjectId(id)})
  return "success"

# This has to be last because definition order matters in Python
if __name__ == '__main__':
    app.run(debug=True)
