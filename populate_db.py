#!/usr/bin/python

from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def main():
    
    
    
    # Connect to the DB
    collection = MongoClient()["learningBrix"]["Users"]

    # Ask for data to store
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    fname= input("Enter your first name: ")
    lname = input("Enter your last name: ")
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Insert the user in the DB
    try:
        collection.insert({"email": email, "password": pass_hash, "fname":fname, "lname":lname})
        print ("User created.")
    except DuplicateKeyError:
        print ("User already present in DB.")


if __name__ == '__main__':
    main()