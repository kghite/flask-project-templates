"""
MongoDB tool set
"""


import yaml
from pymongo import MongoClient


class MongoInterface:


	"""
	Set up database connection
	"""


	def __init__(self, mongo_uri, database):
		self.client = MongoClient(mongo_uri)
		self.db = self.client[database]


	"""
	Check if a refcode exists in the user collection
	"""


	def verify_code(self, refcode):
		return False if not self.db.users.find( {"code": refcode} ) else True


"""
Mongo connection debug
"""


if __name__ == '__main__':
	# Load config
	with open('config.yaml', 'r') as ymlfile:
		config = yaml.load(ymlfile)
	mongo_uri = config['mongo']['connection_string']

	# Connect to database
	mi = MongoInterface(mongo_uri)
	collections = mi.client['nonviral'].list_collection_names()
	for col_num, col in enumerate(collections):
			print(col, '--', col_num)