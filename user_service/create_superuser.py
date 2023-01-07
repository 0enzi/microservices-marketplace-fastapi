import argparse
from pymongo import MongoClient
from dotenv import dotenv_values
from api.v1.users.auth import get_password_hash
import datetime
config = dotenv_values(".env")

parser = argparse.ArgumentParser()
parser.add_argument("--email", required=True)
parser.add_argument("--password", required=True)
args = parser.parse_args()

# Connect to MongoDB
mongodb = MongoClient(config["MONGODB_URI"], tls=True, tlsAllowInvalidCertificates=True)
db = mongodb[config["DB_NAME"]]


existing_admin = db.users.find_one({"email": args.email})
if existing_admin is not None:
    raise ValueError("A user with this email already exists")


# Parse and autofill remaining fields before saving to db
user_obj = {
    "account_info": {
        "account_type": "ADMIN",
        "permissions": ["ALL"]


    },
    "email": args.email,

    "username": args.email.split("@")[0],
    "password": get_password_hash(args.password),
    "created_at": datetime.datetime.now().timestamp(),
    "account_type_id": "ADMIN",
    "is_super_admin": True,
    "status": True,
    "email_verified": True,
    "phone_verified": True,
    "following_categories": []

}



# Insert the new user into the database and Cache using redis
new_superuser = db.users.insert_one(user_obj)




# Create the superuser
# client.admin.command("createUser", args.email, pwd=args.password, roles=[{"role": "root", "db": "admin"}])

print("Superuser created successfully!")