import requests

url = "https://user-field.aylanetworks.com/users/sign_in.json"

payload = "{\r\n    \"user\": {\r\n        \"email\": \"luckposht@gmail.com\",\r\n        \"application\": {\r\n            \"app_id\": \"CJIOSP-id\",\r\n            \"app_secret\": \"CJIOSP-Vb8MQL_lFiYQ7DKjN0eCFXznKZE\"\r\n        },\r\n        \"password\": \"sanjab1234\"\r\n    }\r\n}"
headers = {
    'content-type': "application/json"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
