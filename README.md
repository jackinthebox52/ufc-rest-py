<h3 align="center">UFC-REST-PY</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/jackinthebox52/ufc-rest-py)](https://github.com/jackinthebox52/ufc-rest-py/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/jackinthebox52/ufc-rest-py)](https://github.com/jackinthebox52/ufc-rest-py/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> A REST api wrapper for the undocumented UFC.com event api, written in python.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Prerequisites](#prerequisites)
- [Installing](#installing)
- [Usage](#usage)
- [Built Using](#built_using)

## 🧐 About <a name = "about"></a>

This api client currently supports the singular endpoint that I am aware of (api/v3/events/live/eventid.json), which returns JSON containing event-specific data (Date, Location, Title,  Bouts/Fighters, Per-Bout Timestamps etc.) The data is deserialized and returned as a custom Python object. No 3rd-party libraries are used for deserialization. This project is a bit overkill, enjoy.

### Prerequisites

Python version 3.6+
Python requests library and requests[socks]

### Installing

A step by step series of examples that tell you how to get a development env running.

(Optional) Create a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install from PyPi

```bash
pip install ufc-rest
```

OR, clone the repository and install from source

```bash
git clone https://github.com/jackinthebox52/ufc-rest-py
cd ufc-rest-py
pip install .
```

## 🎈 Usage <a name="usage"></a>

An basic example of how to use the client.

```python
from ufc_rest import APIClient

client = APIClient()    # Initialize a client

event = client.get_event(1081) # Get the live event data for event id 1081 (Oliveira vs. Gaethje)

print(event.title) # Print the event title

for f in event.fights: # Print the fighters in each bout
    print(f)
    print(f'The #{f.FightOrder} (reverse order), is between {f.fighters[0].name.first} and {f.fighters[0].name.first}')
```

TODO: Add advanced usage examples

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.python.com/)
- [Requests](https://github.com/psf/requests) (With socks support)

