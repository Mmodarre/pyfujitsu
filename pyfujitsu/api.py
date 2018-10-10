import logging

import requests

HEADER_CONTENT_TYPE = "Content-Type"
HEADER_AUTHORIZATION = "Authorization"


HEADER_VALUE_CONTENT_TYPE = "application/json"
HEADER_VALUE_AUTHORIZATION = None 

API_BASE_URL = "https://ads-field.aylanetworks.com/apiv1/"
API_GET_ACCESS_TOKEN_URL = "https://user-field.aylanetworks.com/users/sign_in.json"

API_GET_DEVICES_URL =  API_BASE_URL + "devices.json"
API_GET_PROPERTIES_URL = API_BASE_URL + "/dsns/{DSN}/properties.json"
API_SET_PROPERTIES_URL = API_BASE_URL + "/properties/{property}/datapoints.json"

OPERATION_MODE = {
    "OFF": 0,
    "AUTO" : 2,
    "COOL" : 3,
    "DRY" : 4,
    "FAN" : 5,
    "HEAT" : 6
}

OPERATION_MODE_REVERSE = {
    0 : "OFF",
    2 : "AUTO",
    3 : "COOL",
    4 : "DRY",
    5 : "FAN",
    6 : "HEAT"
}


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
    
    def _get_devices(self,access_token):
      
      if not self._check_token_validity(access_token):
          self._authenticate()

      response = self._call_api("get",API_GET_DEVICES_URL,access_token=access_token)
      
      devices = response.json()
      SplitACs = []
      for device in devices:
          SplitACs.append(SplitAC(device['device']['dsn']))
      return[SplitACs]


    def _get_device_properties(self,access_token,dsn):
        if not self._check_token_validity(access_token):
            self._authenticate()

        response = self._call_api("get",API_GET_PROPERTIES_URL.format(dsn=dsn),access_token=access_token)

        return SplitAC(dsn,response.json())

    def _set_device_property(self,access_token,propertyCode,value):
        if not self._check_token_validity(access_token):
            self._authenticate()

        response = self._call_api("post",API_SET_PROPERTIES_URL.format(property=propertyCode),access_token=access_token)

        return SplitAC(dsn,response.json())

    def _check_token_validity(self,access_token):
        response = self._call_api("get",API_GET_DEVICES_URL,access_token=access_token)
        if response.status_code == 401:
            return False
        else:
            return True

    def _authenticate(self):
        # try to authenticate if not worked raise error
        # if worked put it in the header
        # use self.username , self.password
        return False
    
    
    def _call_api(self, method, url, access_token=None, **kwargs):
        payload = ''
        propertyValue = kwargs.get("params")
        if propertyValue:
            payload = '{\"datapoint\": {\"value\": '+ str(propertyValue) +' } }'


        if "headers" not in kwargs:
            kwargs["headers"] = _api_headers(access_token=access_token)

        if method == 'post':
            if not payload:
              raise Exception('Post method needs a request body!')


        _LOGGER.debug("About to call %s with header=%s and payload=%s", url,
                      kwargs["headers"], payload)

        response = requests.request(method, url, **kwargs)

        _LOGGER.debug("Received API response: %s, %s", response.status_code,
                      response.content)

        response.raise_for_status()
        return response