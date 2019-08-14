from .api import Api as api

#version 0.9.2.7

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
        self.min_heat = self._properties  ## TODO Missing device setting method
        self.outdoor_low_noise = self._properties  ## TODO Missing device setting method
        self.operation_mode = self._properties 
        self.adjust_temperature = self._properties 

    ## Method for getting new (refreshing) properties values
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
    
    ## To Turn on the device get the last operation mode using property history method
    ## Find the last not 'OFF'/'0' O.M. 
    ## Turn on by setting O.M. to the last O.M
    def turnOn(self):
        datapoints = self._get_device_property_history(self.operation_mode['key'])
        ## Get the latest setting before turn off
        for datapoint in reversed(datapoints):
            if(datapoint['datapoint']['value'] != 0):
                last_operation_mode = int(datapoint['datapoint']['value'])
                break
        
        self.operation_mode = last_operation_mode
        self.refresh_properties()
    
    def turnOff(self):
        self.operation_mode = 0
        self.refresh_properties()

    ## Economy mode setting
    def economy_mode_on(self):
        self.economy_mode = 1

    def economy_mode_off(self):
        self.economy_mode = 0

    ## Powerfull mode setting
    def powerfull_mode_on(self):
        self.powerful_mode = 1

    def powerfull_mode_off(self):
        self.powerful_mode = 0

    ## Fan speed setting
    ## Quiet Low Medium High Auto
    def changeFanSpeed(self, speed):
        print(speed)
        if speed.upper() == 'QUIET':
            self.fan_speed_quiet()
            return None
        if speed.upper() == 'LOW':
            self.fan_speed_low()
            return None
        if speed.upper() == 'MEDIUM':
            self.fan_speed_medium()
            return None
        if speed.upper() == 'HIGH':
            self.fan_speed_high()
            return None
        if speed.upper() == 'AUTO':
            self.fan_speed_auto()
            return None

    def fan_speed_quiet(self):
            self.fan_speed = 0
    def fan_speed_low(self):
            self.fan_speed = 1
    def fan_speed_medium(self):
            self.fan_speed = 2
    def fan_speed_high(self):
            self.fan_speed = 3
    def fan_speed_auto(self):
            self.fan_speed = 4
    
    def get_fan_speed_desc(self):
        FAN_SPEED_DICT = {
            0 : 'Quiet',
            1 : 'Low',
            2 : 'Medium',
            3 : 'High',
            4 : 'Auto'
        }
        return FAN_SPEED_DICT[self.fan_speed['value']]
    
    ## Fan Swing mode
    ## 0: 'Horizontal',1: 'Down', 2: 'Unknown', 3: 'Swing' 
    def changeSwingMode(self, mode):
        print(mode)
        if mode.upper() == 'HORIZONTAL':
            self.af_vertical_direction = 0
            return None
        if mode.upper() == 'DOWN':
            self.af_vertical_direction = 1
            return None
        if mode.upper() == 'UNKNOWN':
            self.af_vertical_direction = 2
            return None
        if mode.upper() == 'SWING':
            self.af_vertical_direction = 3
            return None
    
    def get_swing_mode_desc(self):
        SWING_LIST_DICT = {
            0: 'Horizontal',
            1: 'Down', 
            2: 'Unknown', 
            3: 'Swing' 
        }
        try:
            return SWING_LIST_DICT[self.af_vertical_direction['value']]
        except TypeError:
            return SWING_LIST_DICT[2]
        

    ## Direction Settings
            ## Vertical
    def vertical_swing_on(self):
        self.af_vertical_swing = 1

    def vertical_swing_off(self):
        self.af_vertical_swing = 0
    
    def vertical_direction(self,newDirection):
        if not isinstance(newDirection,int):
            raise Exception('Wrong usage of method')
        if newDirection > 0 and newDirection < 8:
            self.af_vertical_direction = newDirection
        else:
            raise Exception('Direction out of range 1 - 7!')
            
            ## Horizontal
    def horizontal_swing_on(self):
        self.af_vertical_swing = 1

    def horizontal_swing_off(self):
        self.af_vertical_swing = 0

    def horizontal_direction(self,newDirection):
        if not isinstance(newDirection,int):
            raise Exception('Wrong usage of method')
        if newDirection > 0 and newDirection < 8:
            self.af_horizontal_direction = newDirection
        else:
            raise Exception('Direction out of range 1 - 7!')
    
    
    
    ## Temperature setting
    def changeTemperature(self,newTemperature):
        ## set temperature for degree C
        if not isinstance(newTemperature,int) and not isinstance(newTemperature,float):
            raise Exception('Wrong usage of method')
        ## Fixing temps if not given as multiplies of 10 less than 180
        if newTemperature < 180:
            newTemperature = newTemperature * 10
        if (newTemperature >= 180 and newTemperature <= 320):
            self.adjust_temperature = newTemperature
        else:
            raise Exception('out of range temperature!!')

    ## Operation Mode setting
    def changeOperationMode(self,operationMode):
        if not isinstance(operationMode, int):
            operationMode = self._operation_mode_translate(operationMode)
        self.operation_mode = operationMode

    
    ## Class properties:
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
        if isinstance(properties,(list, tuple)):
            self._outdoor_low_noise = self._get_prop_from_json('outdoor_low_noise',properties)
        elif isinstance(properties,int):
            self._api._set_device_property(self.outdoor_low_noise['key'],properties)
            self.refresh_properties()
        else:
            raise Exception('Wrong usage of the method!!')


    @property
    def powerful_mode(self): return self._powerful_mode

    @powerful_mode.setter
    def powerful_mode(self,properties):
        if isinstance(properties,(list, tuple)):
            self._powerful_mode = self._get_prop_from_json('powerful_mode',properties)
        elif isinstance(properties,int):
            self._api._set_device_property(self.powerful_mode['key'],properties)
            self.refresh_properties()
        else:
            raise Exception('Wrong usage of the method!!')

    @property
    def fan_speed(self): return self._fan_speed

    @fan_speed.setter
    def fan_speed(self,properties):
        if isinstance(properties,(list, tuple)):
            self._fan_speed = self._get_prop_from_json('fan_speed',properties)
        elif isinstance(properties,int):
            self._api._set_device_property(self.fan_speed['key'],properties)
            self.refresh_properties()
        else:
            raise Exception('Wrong usage of the method!!')
            
    
    @property
    def economy_mode(self): return self._economy_mode

    @economy_mode.setter
    def economy_mode(self,properties):
        if isinstance(properties,(list, tuple)):
            self._economy_mode = self._get_prop_from_json('economy_mode',properties)
        elif isinstance(properties,int):
            self._api._set_device_property(self.economy_mode['key'],properties)
            self.refresh_properties()
        else:
            raise Exception('Wrong usage of the method!!')


    @property
    def af_horizontal_direction(self): return self._af_horizontal_direction

    @af_horizontal_direction.setter
    def af_horizontal_direction(self,properties):
        
        if isinstance(properties,(list, tuple)):
            self._af_horizontal_direction = self._get_prop_from_json('af_horizontal_direction',properties)
        elif isinstance(properties,int):
            self._api._set_device_property(self.af_horizontal_direction['key'],properties)
            self.horizontal_swing_off() ##If direction set then swing will be turned OFF
            self.refresh_properties()
        else:
            raise Exception('Wrong usage of the method or direction out of range!!')
    

    @property
    def af_horizontal_swing(self): return self._af_horizontal_swing

    @af_horizontal_swing.setter
    def af_horizontal_swing(self,properties):
        if isinstance(properties,(list, tuple)):
            self._af_horizontal_swing = self._get_prop_from_json('af_horizontal_swing',properties)
        elif isinstance(properties,int):
            self._api._set_device_property(self.af_horizontal_swing['key'],properties)
            self.refresh_properties()
        else:
            raise Exception('Wrong usage of the method!!')
         

    @property
    def af_vertical_direction(self): return self._af_vertical_direction

    @af_vertical_direction.setter
    def af_vertical_direction(self,properties):
        if isinstance(properties,(list, tuple)):
            self._af_vertical_direction = self._get_prop_from_json('af_vertical_move_step1',properties)
        elif isinstance(properties,int):
            self._api._set_device_property(self.af_vertical_direction['key'],properties)
            #self.vertical_swing_off() ##If direction set then swing will be turned OFF
            self.refresh_properties()
        else:
            raise Exception('Wrong usage of the method or direction out of range!!')
    
    @property
    def af_vertical_swing(self): return self._af_vertical_swing

    @af_vertical_swing.setter
    def af_vertical_swing(self,properties):
        if isinstance(properties,(list, tuple)):
            self._af_vertical_swing = self._get_prop_from_json('af_vertical_swing',properties)
        elif isinstance(properties,int):
            self._api._set_device_property(self.af_vertical_swing['key'],properties)
            self.refresh_properties()
        else:
            raise Exception('Wrong usage of the method!!')

    @property
    def device_name(self): return self._device_name

    @device_name.setter
    def device_name(self,properties):
        self._device_name = self._get_prop_from_json('device_name',properties)
        
    ## Get a property history
    def _get_device_property_history(self,propertyCode):
        propertyHistory = self._api._get_device_property(propertyCode)
        propertyHistory = propertyHistory.json()

        return propertyHistory

    ##Translate the operation mode to descriptive values and reverse
    def _operation_mode_translate(self,operation_mode):
        DICT_OPERATION_MODE = {
            "off": 0,
            "auto" : 2,
            "cool" : 3,
            "dry" : 4,
            "fan_only" : 5,
            "heat" : 6,
            0 : "off",
            2 : "auto",
            3 : "cool",
            4 : "dry",
            5 : "fan_only",
            6 : "heat"
        }
        return DICT_OPERATION_MODE[operation_mode]
