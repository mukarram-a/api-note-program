'''

Uses OpenWeather API to retrieve weather
data based on zipcode input.

Imported into 'a4_refactor.py'

'''


# Mukarram A.
# OpenWeather.py

#apikey = d5c9b6d9426a12f20035ddbe1069f003

import urllib, json
from WebAPI import WebAPI
from urllib import request, error

class OpenWeather(WebAPI):
    '''
    Inherits from parent class "WebAPI"
    Abstract method for load_data() and transclude()

    '''

    def __init__(self, zipcode = 97086, ccode = 'US'):
        '''
        Creates class variables for zipcode and country code. Default values are set.

        '''
        self._zipc = zipcode
        self._countryc = ccode

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.

        Collects API data from OpenWeather for weather data/conditions and stores them as class variables.
        Default values are set to '[Unable to process data]'
    
        '''
        response = None
        r_obj = None
        self.temperature = '[Unable to process data]'
        self.high_temperature = '[Unable to process data]'
        self.low_temperature = '[Unable to process data]'
        self.longitude = '[Unable to process data]'
        self.latitude = '[Unable to process data]'
        self.description = '[Unable to process data]'
        self.humidity = '[Unable to process data]'
        self.city = '[Unable to process data]'
        self.sunset = '[Unable to process data]'

        try:
            r_obj = self._download_url(f'http://api.openweathermap.org/data/2.5/weather?zip={self._zipc},{self._countryc}&appid={self._apikey}')
            status = r_obj['cod']
    
            if status == 200:

                self.temperature = r_obj['main']['temp']
                self.high_temperature = r_obj['main']['temp_max']
                self.low_temperature = r_obj['main']['temp_min']
                self.longitude = r_obj['coord']['lon']
                self.latitude = r_obj['coord']['lat']
                self.description = r_obj['weather'][0]['description']
                self.humidity = r_obj['main']['humidity']
                self.city = r_obj['name']
                self.sunset = r_obj['sys']['sunset']
                
            else:
                print('An error occured when trying to recieve data from the API. Try again.')
    
        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print('Status code: {}'.format(e.code))
            print()

        except urllib.error.URLError:
            raise Exception('Failed attempt. Not connected to the internet.')

        except KeyError:
            raise Exception('Invalid data formatting from the remote API (Key Errror). Resuming...')

        except TypeError:
            raise Exception('Invalid data formatting from the remote API (Type Error). Resuming...')
        
        finally:
            if response != None:
                response.close()

    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude
            
        :returns: The transcluded message
        Transcluded message includes API data from OpenWeather for "description"

        '''
        self.load_data()
        message = message.replace('@weather', self.description)

        return message
        