'''

Uses LastFM API to retrieve top 
artist based on current top artists.

Imported into 'a4_refactor.py'

'''


# Mukarram A.
# LastFM.py

#apikey = d649e0ad3b577d939d2dcf585c27ea2c

import urllib, json
from WebAPI import WebAPI
from urllib import request, error


class LastFM(WebAPI):
    '''
    Inherits from parent class "WebAPI"

    Abstract method for load_data() and transclude()
    
    '''

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.

        Collects API data from LastFM for Top Artist and stores it as a class variable "self.topartist"

        '''

        response = None
        r_obj = None

        try:
            r_obj = self._download_url(f'http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={self._apikey}&format=json')

            self.topartist = r_obj['artists']['artist'][0]['name']

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

        Transcluded message includes API data from LastFM for Top Artist

        '''
        self.load_data()
        message = message.replace('@lastfm', self.topartist)

        return message
