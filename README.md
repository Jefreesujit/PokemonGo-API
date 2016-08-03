# Pokemon Go API for Python

This was originally based on tejado's **original** demo,
[this API](https://github.com/tejado/pgoapi/tree/eb788ebbde46664013527a2e5f6c16e98d59d5e3/old-demo).
You can view this as an advanced
and cleaned up version
based on object-oriented principles.

Additions welcome.

## Current implementation
This Bot focuses on collecting pokestops and hatching eggs automatically. 
This bot is not made for catching pokemons, cuz it may lead to soft ban/hard ban of your pokemon go account.

The bot is capable of:

    * Getting your Profile details

    * Getting your Inventory details

    * Cleaning up your Inventory (non-important items)

    * Mock your Location 

    * Collect XP and Items from Pokestops

    *  Incubate Eggs Automatically

    *  Auto assign Eggs into empty Incubators


## Installation

### Step One :  Install Prerequisites

1. [Install Python 2.7+](https://wiki.python.org/moin/BeginnersGuide/Download)
2. [Install PIP](https://pip.pypa.io/en/stable/installing/)

(Latest versions of python comes along with pip)

### Step Two :  Install Pokemon_Go_API

1. Download or clone the repository.
2. Using a terminal, navigate into the cloned repository.
3. Install all requirements for the project using 

```bash
    pip install -r requirements.txt
```

### Step Three :  Run Pokemon_Go_API

To run the project using Google login:

```bash
python main.py -a "google" -u "yourusername" -p "yourpassword123"  -l "Some Location, Some City"
```

To run the project using  Pokemon Trainer Club login:

```bash
python main.py -a "ptc" -u "yourusername" -p "yourpassword123" -l "Some Location, Some City"
```

### Authentication Note

If you're authenticating with Google and have 2 factor authentication enabled for you account, you should
create an [application specific password](https://support.google.com/accounts/answer/185833?hl=en).


## Bot Example
`main.py` includes an automated Bot script made out of the API.

```

2016-07-17 16:26:59,947 - INFO - Creating Google session for someemail@gmail.com
2016-07-17 16:26:59,953 - INFO - Starting new HTTPS connection (1): android.clients.google.com
2016-07-17 16:27:00,362 - INFO - Starting new HTTPS connection (1): android.clients.google.com
2016-07-17 16:27:00,789 - INFO - Location: Your Location
2016-07-17 16:27:00,789 - INFO - Coordinates: 51.01 7.12 0.0
2016-07-17 16:27:00,793 - INFO - Starting new HTTPS connection (1): pgorelease.nianticlabs.com
2016-07-17 16:27:01,633 - INFO - creation_time: 3341800000
team: 3
avatar {
  hair: 1
  shirt: 1
  pants: 1
  hat: 1
  shoes: 1
  eyes: 1
  backpack: 1
}
max_pokemon_storage: 250
max_item_storage: 400
daily_bonus {
  next_defender_bonus_collect_timestamp_ms: 4106877052
}
currency {
  type: "STARDUST"
  quantity: 9001
}
```


## Protocol
This repo currently use [AeonLucid's Pokemon Go Protobuf protocol](https://github.com/AeonLucid/POGOProtos).
