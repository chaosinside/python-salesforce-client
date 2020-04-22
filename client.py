import requests, json

class SalesforceClient:
	# static variables
	API_ENDPOINT = "/services/data/v46.0/"

	# constructor
	def __init__(self, login_endpoint, username, password, token, client_id, client_secret):
		# instance variables
		self.login_endpoint = login_endpoint
		self.username = username
		self.password = password
		self.token = token
		self.client_id = client_id
		self.client_secret = client_secret

	# login to Salesforce
	def login(self):
		payload = {
			"grant_type": "password",
			"client_id": self.client_id,
			"client_secret": self.client_secret,
			"username": self.username,
			"password": self.password + self.token
		} 
		headers = { "Content-Type": "application/x-www-form-urlencoded" }
		response = requests.post(self.login_endpoint, headers=headers, data=payload)
		self.access_token = json.loads(response.text)["access_token"]
		self.instance_url = json.loads(response.text)["instance_url"]
		return response

	def get_headers(self):
		return {
			"Content-Type": "application/json; charset=UTF-8",
			"Accept": "application/json",
			"Authorization": "Bearer "+ self.access_token
		}

	# query data using SOQL
	def query(self, query):
		url = self.instance_url + self.API_ENDPOINT +"query/?q="+ query
		response = requests.get(url, headers=self.get_headers())
		return response

	# create record
	def record_create(self, object_name, payload):
		url = self.instance_url + self.API_ENDPOINT +"sobjects/"+ object_name +"/"
		response = requests.post(url, headers=self.get_headers(), data=json.dumps(payload))
		return response

	# create list of records
	# sObject type attribute required in each object: {"attributes": {"type" : "Account"}, "Name": "example.com"}
	def record_create_list(self, objects, all_or_none=False):
		payload = { "allOrNone": all_or_none, "records": objects }
		url = self.instance_url + self.API_ENDPOINT +"composite/sobjects"
		response = requests.post(url, headers=self.get_headers(), data=json.dumps(payload))
		return response

	# delete record
	def record_delete(self, object_name, object_id):
		url = self.instance_url + self.API_ENDPOINT +"sobjects/"+ object_name +"/"+ object_id
		response = requests.delete(url, headers=self.get_headers())
		return response

	# delete list of records
	def record_delete_list(self, object_ids):
		url = self.instance_url + self.API_ENDPOINT +"composite/sobjects?ids="+ ",".join(object_ids)
		response = requests.delete(url, headers=self.get_headers())
		return response

	# delete record with external id field
	def record_delete_extid(self, object_name, extid_field_name, ext_id):
		url = self.instance_url + self.API_ENDPOINT +"sobjects/"+ object_name +"/"+ extid_field_name +"/"+ ext_id
		response = requests.delete(url, headers=self.get_headers())
		return response

	# get record with external id field
	def record_get_extid(self, object_name, extid_field_name, ext_id):
		url = self.instance_url + self.API_ENDPOINT +"sobjects/"+ object_name +"/"+ extid_field_name +"/"+ ext_id
		response = requests.get(url, headers=self.get_headers())
		return response

	# update record
	def record_update(self, object_name, object_id, payload):
		url = self.instance_url + self.API_ENDPOINT +"sobjects/"+ object_name +"/"+ object_id
		response = requests.patch(url, headers=self.get_headers(), data=json.dumps(payload))
		return response

	# upsert record with external id field
	def record_upsert_extid(self, object_name, extid_field_name, ext_id, payload):
		url = self.instance_url + self.API_ENDPOINT +"sobjects/"+ object_name +"/"+ extid_field_name +"/"+ ext_id
		response = requests.patch(url, headers=self.get_headers(), data=json.dumps(payload))
		return response

	# create job
	def job_create(self, payload):
		url = self.instance_url + self.API_ENDPOINT +"jobs/ingest"
		response = requests.post(url, headers=self.get_headers(), data=json.dumps(payload))
		return response

	# upload job data
	def job_upload(self, job_id, payload, content_type):
		url = self.instance_url + self.API_ENDPOINT +"jobs/ingest/"+ job_id +"/batches/"
		headers = self.get_headers()
		headers["Content-Type"] = content_type
		response = requests.put(url, headers=headers, data=payload.encode('utf-8'))
		return response

	# update job
	def job_update(self, job_id, payload):
		url = self.instance_url + self.API_ENDPOINT +"jobs/ingest/"+ job_id
		response = requests.patch(url, headers=self.get_headers(), data=json.dumps(payload))
		return response

	# check job
	def job_check(self, job_id):
		url = self.instance_url + self.API_ENDPOINT +"jobs/ingest/"+ job_id
		response = requests.get(url, headers=self.get_headers())
		return response

	# get job failures
	def job_get_failed(self, job_id):
		url = self.instance_url + self.API_ENDPOINT +"jobs/ingest/"+ job_id +"/failedResults"
		response = requests.get(url, headers=self.get_headers())
		return response