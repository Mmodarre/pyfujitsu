from api import Api as api

class splitAC:
    def __init__(self,dsn,api,properties=None):
        self._dsn = dsn
        self._api = api # Setting the API object
        
        ## Calling the api class _get_device_properties to get devices properties
        properties = self._api._get_device_properties(self._dsn)
        
        ## self.properties: For now this variable is not used but lots of device properties which are not implemented
        ## this variable can be used to expose those properties and implement them.
        self.properties = properties 
        #print(type(properties))
        self.device_name = properties
        self.af_vertical_swing = properties
        self.af_vertical_direction = properties
        self.af_horizontal_swing = properties 
        self.af_horizontal_direction = properties 
        self.economy_mode = properties 
        self.fan_speed = properties
        self.powerful_mode = properties 
        self.min_heat = properties 
        self.outdoor_low_noise = properties
        self.operation_mode = properties

    ## Method for getting new properties
    ## // Todo: Add the refreshing values by API call to this method
    def refresh_properties(self):
        properties = self._api._get_device_properties(self._dsn)
        self.properties = properties
        self.device_name = properties
        self.adjust_temprature = properties
        self.af_vertical_swing = properties
        self.af_vertical_direction = properties
        self.af_horizontal_swing = properties 
        self.af_horizontal_direction = properties 
        self.economy_mode = properties 
        self.fan_speed = properties
        self.powerful_mode = properties 
        self.min_heat = properties 
        self.outdoor_low_noise = properties
        self.operation_mode = properties
    
    ## todo get the last operation mode to turn it one to that using the property endpoint and "GET" method
    def TurnOn(self):
        self.operation_mode = 6

    def changeTemprature(self,newTemperature):
        self.adjust_temperature = newTemperature

    def changeOperationMode(self,operationMode):
        if not isinstance(operationMode, int):
            operationMode = self._operation_mode_translate(operationMode)
            #print(operationMode)
        self.operation_mode = operationMode

    

    @property
    def dsn(self): return self._dsn
    
    def _get_prop_from_json(self,propertyName,properties):
        for property in properties:
            if property['property']['name'] == propertyName:
                return {'value':property['property']['value'],'key':property['property']['key']}

    

    @property
    def operation_mode(self): return self._operation_mode

    @property
    def operation_mode_desc(self): return self._operation_mode_translate(self.operation_mode['value'])

    @operation_mode.setter
    def operation_mode(self,properties):
        if isinstance(properties,(list, tuple)):
            self._operation_mode = self._get_prop_from_json('operation_mode',properties)
        elif isinstance(properties,int):
            print(self._api._set_device_property(self.operation_mode['key'],properties))
            self._operation_mode['value'] =  properties
        else:
            raise Exception('Wrong usage of the method!!')

    @property
    def adjust_temperature(self): return self._adjust_temperature

    @adjust_temperature.setter
    def adjust_temperature(self,properties):
        self._adjust_temperature = self._get_prop_from_json('adjust_temperature',properties)


    @property
    def outdoor_low_noise(self): return self._outdoor_low_noise

    @outdoor_low_noise.setter
    def outdoor_low_noise(self,properties):
        self._outdoor_low_noise = self._get_prop_from_json('outdoor_low_noise',properties)


    @property
    def powerful_mode(self): return self._powerful_mode

    @powerful_mode.setter
    def powerful_mode(self,properties):
        self._powerful_mode = self._get_prop_from_json('powerful_mode',properties)

    @property
    def fan_speed(self): return self._fan_speed

    @fan_speed.setter
    def fan_speed(self,properties):
        self._fan_speed = self._get_prop_from_json('fan_speed',properties)

    
    @property
    def economy_mode(self): return self._economy_mode

    @economy_mode.setter
    def economy_mode(self,properties):
        self._economy_mode = self._get_prop_from_json('economy_mode',properties)

    @property
    def af_horizontal_direction(self): return self._af_horizontal_direction

    @af_horizontal_direction.setter
    def af_horizontal_direction(self,properties):
        self._af_horizontal_direction = self._get_prop_from_json('af_horizontal_direction',properties)

    @property
    def af_horizontal_swing(self): return self._af_horizontal_swing

    @af_horizontal_swing.setter
    def af_horizontal_swing(self,properties):
        self._af_horizontal_swing = self._get_prop_from_json('af_horizontal_swing',properties)
    
    @property
    def af_vertical_direction(self): return self._af_vertical_direction

    @af_vertical_direction.setter
    def af_vertical_direction(self,properties):
        self._af_vertical_direction = self._get_prop_from_json('af_vertical_direction',properties)
    
    @property
    def device_name(self): return self._device_name

    @device_name.setter
    def device_name(self,properties):
        self._device_name = self._get_prop_from_json('device_name',properties)

    @property
    def af_vertical_swing(self): return self._af_vertical_swing

    @af_vertical_swing.setter
    def af_vertical_swing(self,properties):
        self._af_vertical_swing = self._get_prop_from_json('af_vertical_swing',properties)

    ##Translate the operation mode to descriptive values and reverse
    def _operation_mode_translate(self,operation_mode):
        DICT_OPERATION_MODE = {
            "OFF": 0,
            "AUTO" : 2,
            "COOL" : 3,
            "DRY" : 4,
            "FAN" : 5,
            "HEAT" : 6,
            0 : "OFF",
            2 : "AUTO",
            3 : "COOL",
            4 : "DRY",
            5 : "FAN",
            6 : "HEAT"
        }
        return DICT_OPERATION_MODE[operation_mode]
         
      
print(living.device_name['value'])
print(living.operation_mode_desc)
living.changeOperationMode('OFF')
print(living.operation_mode_desc)