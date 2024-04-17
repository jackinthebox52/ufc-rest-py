import requests
from models.event import Event

'''
This class is a wrapper for the UFC API, providing methods to retrieve event data, search for events, etc.
'''
class APIClient:
    def __init__(self, proxies: dict = None, headers: dict = None, timeout: int = 10, retries: int = 3):
        self.base_url = "https://d29dxerjsp82wz.cloudfront.net/api/v3"
        self.proxies = proxies
        
        self.headers = headers      #TODO: implement headers
        self.timeout = timeout      #TODO: implement timeout
        self.retries = retries      #TODO: implement retries
        
    '''
    Returns the event data for the specified event ID from the UFC API.
    '''
    def get_event(self, event_id: int):
        url = f"{self.base_url}/event/live/{event_id}.json"
        data = requests.get(url, proxies=self.proxies).json()
        return Event.from_json(data)

    '''
    Search the UFC website directly for the specified query. Query must be a string of the name of the event you would like to search for, matching the official event title (Wikipedia)
    Returns the event id of the matching event, or None if no event was found. Currently only supports Fight nights and PPV events.
    E.g. search_event("UFC 303: McGregor vs Chandler") or search_event("UFC Fight Night: Font vs Aldo")
    '''
    def search_event(self, query: str):
        #Boilerplate
        return None

if __name__ == "__main__":
    client = APIClient()
    event = client.get_event(1082)
    print(event)