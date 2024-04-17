import requests
from models.event import Event

def main():
    from pympler import asizeof
    url = "https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/1080.json"
    data = response = requests.get(url).json()
    event_obj = Event.from_json(data)

if __name__ == "__main__":
    main()