from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'pa55word1'
DB_NAME = 'learningBrix'

DATABASE = MongoClient()[DB_NAME]
POSTS_COLLECTION = DATABASE.posts
USERS_COLLECTION = DATABASE.Users
SETTINGS_COLLECTION = DATABASE.settings

DEBUG = True