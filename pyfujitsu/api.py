import logging
import requests
import time
import os
import json

HEADER_CONTENT_TYPE = "Content-Type"
HEADER_VALUE_CONTENT_TYPE = "application/json"
HEADER_AUTHORIZATION = "Authorization"
SIGNIN_BODY = "{\r\n    \"user\": {\r\n        \"email\": \"%s\",\r\n        \"application\": {\r\n            \"app_id\": \"CJIOSP-id\",\r\n            \"app_secret\": \"CJIOSP-Vb8MQL_lFiYQ7DKjN0eCFXznKZE\"\r\n        },\r\n        \"password\": \"%s\"\r\n    }\r\n}"
API_BASE_URL = "https://ads-field.aylanetworks.com/apiv1/"
API_GET_ACCESS_TOKEN_URL = "https://user-field.aylanetworks.com/users/sign_in.json"

API_GET_DEVICES_URL =  API_BASE_URL + "devices.json"
API_GET_PROPERTIES_URL = API_BASE_URL + "/dsns/{DSN}/properties.json"
API_SET_PROPERTIES_URL = API_BASE_URL + "/properties/{property}/datapoints.json"
ACCESS_TOKEN_FILE = 'token.txt'

_LOGGER = logging.getLogger(__name__)

def _api_headers(access_token=None):
    headers = {
        HEADER_CONTENT_TYPE: HEADER_VALUE_CONTENT_TYPE
    }

    if access_token:
        headers[HEADER_AUTHORIZATION] = 'auth_token ' + access_token

    return headers

class Api:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        #self._authenticate()
        self._ACCESS_TOKEN_FILE = 'token.txt'
    
    def _get_devices(self,access_token=None):
      if not self._check_token_validity(access_token):
          ## Token invalid requesting authentication
          access_token = self._authenticate()
          

      response = self._call_api("get",API_GET_DEVICES_URL,access_token=access_token)
      return response.json()
      
    def _get_device_properties(self,dsn):
        access_token = self._read_token()
        if not self._check_token_validity(access_token):
            access_token = self._authenticate()

        response = self._call_api("get",API_GET_PROPERTIES_URL.format(DSN=dsn),access_token=access_token)
        return response.json()

    def _set_device_property(self,propertyCode,value):
        access_token = self._read_token()
        if not self._check_token_validity(access_token):
            access_token = self._authenticate()

        response = self._call_api("post",API_SET_PROPERTIES_URL.format(property=propertyCode),propertyValue=value,access_token=access_token)

        return response
    
    def _get_device_property(self,propertyCode):
        access_token = self._read_token()
        if not self._check_token_validity(access_token):
            access_token = self._authenticate()

        response = self._call_api("get",API_SET_PROPERTIES_URL.format(property=propertyCode),access_token=access_token)
        ## Pay Attention the response is a HTTP request response object 
        #  and by doing .json you would get a List
        return response


    def _check_token_validity(self,access_token=None):
        if not access_token:
            return False
        
        try:
            self._call_api("get",API_GET_DEVICES_URL,access_token=access_token)
        except:
            return False
        
        return True


    def _authenticate(self):
        
        response = self._call_api("POST",
         API_GET_ACCESS_TOKEN_URL,
         json=SIGNIN_BODY % (self.username,self.password),
         headers= _api_headers())

        response.json()['time'] = int(time.time())

        access_token = response.json()['access_token']
    
        #refresh_token = response.json()['refresh_token']
        #expires_in = response.json()['expires_in']


        f = open(ACCESS_TOKEN_FILE, "w")
        f.write(response.text) 

        
        return access_token
    
    def _read_token(self,access_token_file=None):
        if not access_token_file:
            access_token_file = self._ACCESS_TOKEN_FILE
        if (os.path.exists(access_token_file) and os.stat(access_token_file).st_size != 0):
            f = open(access_token_file, "r")
            access_token_file_content = f.read()

            #now = int(time.time())

            access_token = json.loads(access_token_file_content)['access_token']
            #refresh_token = access_token_file_content.json()['refresh_token']
            #expires_in = access_token_file_content.json()['expires_in']
            #auth_time = int(access_token_file_content.json()['time'])
            return access_token
        else:
            return self._authenticate()


    
    def _call_api(self, method, url, access_token=None, **kwargs):
        payload = ''
                
        
        if "propertyValue" in kwargs:
            propertyValue = kwargs.get("propertyValue")
            kwargs["json"] = '{\"datapoint\": {\"value\": '+ str(propertyValue) +' } }'
        payload = kwargs.get("json")

        if "headers" not in kwargs:
            if access_token:
                kwargs["headers"] = _api_headers(access_token=access_token)
            else:
                kwargs["headers"] = _api_headers()
        
        if method.lower() == 'post':
            if not payload:
              raise Exception('Post method needs a request body!')

        
        response = requests.request(method, url, data=kwargs.get("json"),headers=kwargs.get("headers"))
        response.raise_for_status()
        return response