'''

Gets information from any specified web API and returns
a dictionary of information.

Class used in 'OpenWeather.py' and 'LastFM.py'

'''

# Mukarram A.
# WebAPI.py


from abc import ABC, abstractmethod
import urllib, json
from urllib import request, error


class WebAPI(ABC):
  '''
  Class for obtaining information from any web API
  
  '''
  def _download_url(self, url: str) -> dict:
    '''
    Args:
      url: string of API url

    Returns:
      dictionary of information from the API

    '''
    response = urllib.request.urlopen(url)
    json_results = response.read()
    r_obj = json.loads(json_results)
    return r_obj


  def set_apikey(self, apikey:str) -> None:
    '''
    Args:
      apikey: string of API key used to access API.
      Stores apikey as class variable

    Returns:
      None
      
    '''
    self._apikey = apikey

  @abstractmethod
  def load_data(self):
    pass

  @abstractmethod
  def transclude(self, message:str) -> str:
    pass


