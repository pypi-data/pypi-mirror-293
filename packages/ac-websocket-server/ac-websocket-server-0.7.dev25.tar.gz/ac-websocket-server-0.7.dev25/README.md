# AC-WEBSOCKETS-SERVER

The ac-websockets-server is a python based server to control a local Assetto Corsa dedicated server via a websockets connection from a remote host.

## Installation

You can install ac-websockets-server from PyPi:

```
pip install ac-websockets-server
```

The module is only supported in python3.

## How to use

## Websocket Commands

The client protocol consists of single line commands which receive a Google style JSON object response.

### shutdown
The following ACWS related commands are supported:

- `shutdown now`  shutdown the ACWS server

### server
The following server related commands are supported:

- `server drivers`  shows a summary of the active drivers on the server
- `server entries`  shows a summary of the entry_list.ini contents
- `server info`  shows a summary of the server
- `server restart`   stops and starts the AC server
- `server sessions`  shows a summary of configured sessions
- `server set session_name enable|disable`  enable or disable a session
- `server set session_name laps number_of_laps`  set number of laps for a session (only valid for RACE)
- `server set session_name time number_of_mins`  set number of mins for a session
- `server start` starts the AC server
- `server stop`  stops the AC server
- `server time number_of_minutes`  sets the number of minutes - needs server restart to take effect

Excerts from the responses to these commands are shown below.

#### server drivers

```
# server drivers
{
    "data": {
        "drivers": {
            "Mark Hannon": {
                "name": "Mark Hannon",
                "host": "192.168.1.1",
                "port": 50834,
                "car": "bmw_m3_e30",
                "guid": "9993334455599",
                "ballast": 0,
                "msg": "joining"
            },
            "Boof Head": {
                "name": "Boof Head",
                "host": "192.168.2.1",
                "port": 50834,
                "car": "bmw_m3_e30",
                "guid": "123456768",
                "ballast": 0,
                "msg": "joining"
            },
            "Crazy Guy": {
                "name": "Crazy Guy",
                "host": "192.168.3.1",
                "port": 50834,
                "car": "bmw_m3_e30",
                "guid": "7777777777777",
                "ballast": 0,
                "msg": "joining"
            }
        }
    }
}
```
#### server entries

```
# server entries
{
    "data": {
        "entries": {
            "CAR_0": {
                "car_id": "CAR_0",
                "model": "dj_skipbarber_f2000",
                "skin": "The9GAG",
                "spectator_mode": "0",
                "drivername": "",
                "team": "",
                "guid": "76561198102064903",
                "ballast": "0",
                "restrictor": "0"
            }
```
#### server sessions

```
# server sessions
{
    "Practice": {
        "type": "Practice",
        "laps": 0,
        "time": 120,
        "msg": ""
    },
    "Qualify": {
        "type": "Qualify",
        "laps": 0,
        "time": "10",
        "msg": ""
    },
    "Race": {
        "type": "Race",
        "laps": 20,
        "time": 0,
        "msg": ""
    }
}
```
#### server start
```

# server start
{
    "data": {
        "msg": "Assetto Corsa server started"
    }
}
# {
    "data": {
        "serverInfo": {
            "version": "v1.15",
            "timestamp": "2022-07-22 10:42:32.8776464 +1000 AEST m=+0.007426800",
            "track": "rt_autodrom_most",
            "cars": "[\"ks_mazda_mx5_cup\"]",
            "msg": ""
        }
    }
}
```
### grid

The following grid related commands are supported:

- `grid finish`  sets grid order based on latest race finishing order
- `grid reverse`  sets grid order based on latest race REVERSED order
- `grid order`  shows a summary of the current/updated grid order
- `grid entries`  shows a summary of the all slots for/from entry_list.ini
- `grid save` write the changes to the grid to the entry_list.ini file


Setting reverse grid and then writing the result are shown below:

```
# grid reverse
{
    "data": {
        "msg": "test/results/2020_12_20_20_58_RACE.json parse SUCCESS"
    }
}
# grid finish
{
    "data": {
        "grid": {
            "1": "Keith",
            "2": ".SNRL.shille",
            "3": "Wayne",
            "4": "Russ S",
            "5": "Mark Hannon",
            "6": "RussG",
            "7": "ab156"
        }
    }
}
# grid write
{
    "data": {
        "msg": "entry_list.ini file update SUCCESS"
    }
}
```

### lobby
The following lobby related commands are supported:

- `lobby info` shows the lobby info
- `lobby restart`   re-registers to the lobby



### tracker
The following tracker related commands are supported:

- `tracker start` starts the AC server
- `tracker stop`  stops the AC server
- `tracker restart`   stops and starts the AC server

All commands require stracker.ini to be stored in the cfg directory and stracker.exe in the server root.


