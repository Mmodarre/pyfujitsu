from pyfujitsu.api import Api as api

class splitAC:
    def __init__(self,dsn,api):
        self._dsn = dsn
        self._api = api # Setting the API object
        
        ## Calling the api class _get_device_properties to get devices properties
        self._properties = self._api._get_device_properties(self._dsn)
        
        ## self.properties: For now this variable is not used but lots of device properties which are not implemented
        ## this variable can be used to expose those properties and implement them.
        self.device_name = self._properties 
        self.af_vertical_swing = self._properties 
        self.af_vertical_direction = self._properties 
        self.af_horizontal_swing = self._properties  
        self.af_horizontal_direction = self._properties  
        self.economy_mode = self._properties  
        self.fan_speed = self._properties 
        self.powerful_mode = self._properties  
        self.min_heat = self._properties  
        self.outdoor_low_noise = self._properties 
        self.operation_mode = self._properties 
        self.adjust_temperature = self._properties 

    ## Method for getting new(refreshing) properties
    def refresh_properties(self):
        self._properties  = self._api._get_device_properties(self._dsn)
        self.device_name = self._properties 
        self.adjust_temperature = self._properties 
        self.af_vertical_swing = self._properties 
        self.af_vertical_direction = self._properties 
        self.af_horizontal_swing = self._properties  
        self.af_horizontal_direction = self._properties  
        self.economy_mode = self._properties  
        self.fan_speed = self._properties 
        self.powerful_mode = self._properties  
        self.min_heat = self._properties  
        self.outdoor_low_noise = self._properties 
        self.operation_mode = self._properties 
    
    ## todo get the last operation mode to turn it one to that using the property endpoint and "GET" method
    def TurnOn(self):
        self.operation_mode = 6

    def changeTemperature(self,newTemperature):
        ## set temperature for degree C
        if not isinstance(newTemperature,int) and not isinstance(newTemperature,float):
            raise Exception('Wrong usage of method')
        ## Fixing temps if not given as multiplies of 10 less than 180
        if newTemperature < 180:
            newTemperature = newTemperature * 10
        if (newTemperature > 180 and newTemperature < 320):
            self.adjust_temperature = newTemperature
        else:
            raise Exception('out of range temperature!!')

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
            self._api._set_device_property(self.operation_mode['key'],properties)
            self.refresh_properties()
        else:
            raise Exception('Wrong usage of the method!!')

    @property ##property to get temperature in degree C
    def adjust_temperature_degree(self): return round((self._adjust_temperature['value'] /10),1)

    @property ## property returns temperature dict in 10 times of degree C
    def adjust_temperature(self): return self._adjust_temperature

    @adjust_temperature.setter
    def adjust_temperature(self,properties):
        if isinstance(properties,(list, tuple)):
            self._adjust_temperature = self._get_prop_from_json('adjust_temperature',properties)
        elif isinstance(properties,int) or isinstance(properties,float):
            self._api._set_device_property(self.adjust_temperature['key'],properties)
            self.refresh_properties()
        else:
            raise Exception('Wrong usage of the method!!')


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
         

