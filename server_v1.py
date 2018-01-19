# Create a new MongoDB Deployment on MongoLabs
# Host it on AWS's free tier, nice (Half a gig of storage)
# Set your region to us-east-1 since we're on the east coast
    # And also not in Ireland
# Name it something like swamphacks-db

# Great, let's create a new user for our database so we can admin it
# Users tab, create new user
    # Make it secure, and definitely NOT admin admin

# Now we're going to create a collection inside this database
# We will be reading from and writing to this
# Let's call it class-roster

import argparse
from pymongo import MongoClient
import sys

parser = argparse.ArgumentParser()

#-addr ADDRESS -db DATABASE -u USERNAME -p PASSWORD
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

client = MongoClient(dburi)
db = client['swamphacks-db']
collection = db['class-roster']

print collection
print collection.insert({"a": "b"})
print collection.find({"a": "b"}).count()