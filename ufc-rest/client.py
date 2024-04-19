import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

import search
from models.event import Event


'''
This class is a wrapper for the UFC API, providing methods to retrieve event data, search for events, etc. Supports SOCKS proxies, custom headers, and request timeouts.
args:
    proxies: dict - A dictionary of SOCKS proxies to use for requests. E.g. {"http": "socks5://fakeproxyip:1234", "https": "socks5://fakeproxyip:1234"} (default is None)
    headers: dict - A dictionary of custom headers to use for requests. E.g. {"User-Agent": "Mozilla/5.0"}  (default is None)
    timeout: int - The request timeout in seconds. (default is 4)
    retry: int|tuple - The number of retries to attempt on failed requests Can also be a tuple of integers to specify connect and read timeouts seperately. (default is 1)
'''
class APIClient:
    def __init__(self, proxies: dict = None, headers: dict = None, timeout: int = 4, retry: int|tuple = 1):
        self.base_url = "https://d29dxerjsp82wz.cloudfront.net/api/v3"
        self.proxies = proxies
                
        self.session = requests.Session()
        
        self.headers = headers
        self.timeout = timeout
        self.retry = retry

        if self.retry > 0:
            self.retries = Retry(total=self.retry, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])        #TODO: fine-tune retries
            self.session.mount('https://', HTTPAdapter(max_retries=self.retries))
        
    '''
    Returns the event data for the specified event ID from the UFC API.
    '''
    def get_event(self, id: int):
        url = f"{self.base_url}/event/live/{id}.json"
        data = requests.get(url, proxies=self.proxies, headers=self.headers, timeout=self.timeout).json()
        return Event.from_json(data)

    '''
    Search the UFC website directly for the specified query. Query must be a string of the name of the event you would like to search for, matching the official event title (Wikipedia)
    Returns the event id of the matching event, or None if no event was found. Currently only supports Fight nights and PPV events.
    E.g. search_event("UFC 303: McGregor vs Chandler") or search_event("UFC Fight Night: Font vs Aldo")
    '''
    def search_event(self, query: str):
        url = search.compile_event_url(query)
        return search.extract_fmid(url)

if __name__ == "__main__":
    client = APIClient()
    id = client.search_event("UFC 269: Oliveira vs Poirier")
    print(id)