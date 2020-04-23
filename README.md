# Python Salesforce Client

A python client for the Salesforce API.

### Getting Started

	pip install SalesforceClient

### Usage
SalesforceClient must be initialized with a login_endpoint, username, password, token, client_id, and client_secret. Once intialized, you can use any of the provided functions to return a requests response object.

### Example
```python
from SalesforceClient import SalesforceClient

login_endpoint = "https://login.salesforce.com/services/oauth2/token"
username = "my_username"
password = "my_password"
token = "my_security_token"
client_id = "my_client_id"
client_secret = "my_client_secret"

client = SalesforceClient(login_endpoint, username, password, token, client_id, client_secret)
response = client.login()
if response.status_code == 200:
	print("Login Success:", response.text)
	query_response = client.query("select Id, Name from User")
	print("Users:", query_response.text)
else:
	print("Salesforce login failed:", response.text)
```
