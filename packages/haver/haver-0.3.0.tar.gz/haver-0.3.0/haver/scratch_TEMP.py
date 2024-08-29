import os
os.environ['HAVER_API_KEY'] = 'wCT48fKMOeIbVZImPzzz32Ocrk4oEFMey9Um7xPVZw0'
import requests

HEADERS = {'Content-Type': 'application/json', 
           'X-API-Key':os.getenv('HAVER_API_KEY')}
_HAVER_URL = 'https://api.haverview.com'
database = 'EUDATA'


requests.get(
            f"{_HAVER_URL}/v4/database/{database}/series?&format=short&per_page=1000",
            headers=HEADERS).json()

database='EUDATA'
series='N997CE'
API_URL = f'{_HAVER_URL}/v4/database/{database}/series/{series}'

requests.get(API_URL, headers=HEADERS).json()



# NOT WORKING

requests.get(f"{_HAVER_URL}/v4/recessions/", headers=HEADERS)#.json()
requests.get(f"{_HAVER_URL}/v4/docs",
                      headers=HEADERS).json()['data']


query='defined'
requests.get(f"{_HAVER_URL}/v4/search?query={query}",headers=HEADERS)#.json()


requests.get(f"{_HAVER_URL}/v4/database", headers=HEADERS).json()