import requests
import re
from datetime import datetime

'''Probe the specified URL to ensure it is reachable'''
def probe_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Failed to probe URL: {url}')
        return False
    return True

'''
Create the UFC.com event URL based on the event name and date. This is used to extract the fmid (UFC API event ID) from the website.
Note: Many older events and TUF events are not supported, this function will raise an error if a date is not provided for Fight Night events.

args:
    event_name: str - The name of the event (e.g. "UFC 269: Oliveira vs Poirier" or "UFC Fight Night: Font vs Aldo")
    event_date: str - The date of the event in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) (trailing Z is optional)
'''
def compile_event_url(event_name: str, event_date: str = None):
    ppv_match = re.search(r'(?i)ufc (\d+)', event_name)
    fn_match = re.search(r'(?i)ufc fight night', event_name)
    url = None
    if ppv_match:
        number = ppv_match.group(1)
        url = f'https://www.ufc.com/event/ufc-{number}'
    elif fn_match:
        if not event_date:
            raise ValueError('Event date required for Fight Night events')      #TODO: handle more gracefully
        date = datetime.strptime(event_date.replace('Z', ''), "%Y-%m-%dT%H:%M")
        fdate = date.strftime("%B-%d-%Y").lower()
        url = f'https://www.ufc.com/event/ufc-fight-night-{fdate}'
        
    if url and probe_url(url):                                                  #If the URL is valid, return it
        return url
    
    print(f'Failed to compile event URL for {event_name} (Many older events and TUF events are not supported)')
    raise ValueError('Invalid event name')

'''Extract the fmid (UFC API event ID) from the specified event URL at UFC.com, and return it.
args:
    event_url: str - The URL of the event page on UFC.com
returns:
    str - The fmid (UFC API event ID) for the event
'''
def extract_fmid(event_url: str) -> str:
    url_match = re.search(r'ufc.com/event/', event_url) 
    if not url_match:
        print('Invalid UFC.com event URL')
        return None
    response = requests.get(event_url)
    response.raise_for_status()

    fmid_match = re.search(r'data-fmid="(\d+)"', response.text)
    if not fmid_match:
        print('Failed to extract fmid from response')
        return None
    return fmid_match.group(1)

def test_compile_event_url():
    event_name = 'UFC 269: Oliveira vs Poirier'
    event_date = '2021-12-11T23:00Z'
    event_url = compile_event_url(event_name, event_date)
    assert event_url == 'https://www.ufc.com/event/ufc-269'
    print('PPV event test passed!\n')

    event_name = 'UFC Fight Night: Font vs Aldo'
    event_date = '2021-12-04T23:00'
    event_url = compile_event_url(event_name, event_date)
    assert event_url == 'https://www.ufc.com/event/ufc-fight-night-december-04-2021'
    print('Fight Night event test passed!')


if __name__ == "__main__":
    test_compile_event_url() 