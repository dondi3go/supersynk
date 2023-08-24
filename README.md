# Supersynk

Supersynk is a toy project for synchronisation of distributed data via HTTP

## Why supersynk ?

Sypersynk was originaly created to synchronize VR users sharing a common VR 
environment. The project started during the 2020 lockdown as a way to meet 
VR aware friends having VR helmets with them and considering video meeting as,
well, not as fun as VR.

The first version of this project was considered (by me) having some embarrasing 
limitions :
* the server was dependant on application-level data
* there was only one channel
* the name of the project was not fun enough

The idea is to make something as simple as possible with as few HTTP requests 
as possible.

HTTP is obviously not the most efficient approach to solve this problem but HTTP 
libraries are available in almost every programming language, so writing
a client for *supersynk* should be easy. Furthermore, HTTP tooling is strong.

VR specific syntax has disappeared from the original idea (it has been relocated 
to application level), making this server now usable in other contexts.

## How does it work ?

Each client sends its data to the server, and get the data of other clients in return.

All data on the server are stored in memory, no database is involved in the process.

The server can host different channels.

Clients connected to the same channel "see" each others.

Clients belonging to different channels do not interact with each others.

## How to use it ?

The API is made of two endpoints, one for the clients who share data with the other 
clients of the channel, and another one for the pure observer clients of the channel.

In each use case, clients can share/get data using one and only one HTTP request.

The payload of request and response are not fully defined here, on purpose, they 
should be *json* objects containing at least the property "client_id". Any other 
properties in the *json* objects should be defined and handled by client applications.

### Endpoint for a participant in the channel

**POST** [ip]:[port]/api/channels/[channel_key]

with a request body like :
```
{"client_id":"ada" ... }
```
response body could be :
```
[{"client_id":"joe" ...}]
```

### Endpoint for an observer of the channel

**GET** [ip]:[port]/api/channels/[channel_key]

response body could be :
```
[{"client_id":"ada" ... }, {"client_id":"joe" ... }]
```

## Running the server

```
python supersync_server.py
```

## Testing the server

Sending data to 'test' channel
```
curl -X POST http://127.0.0.1:9999/api/channels/test -H "Content-Type:application/json" -d {\"client_id\":\"ada\"}
curl -X POST http://127.0.0.1:9999/api/channels/test -H "Content-Type:application/json" -d {\"client_id\":\"joe\"}
```

Getting data from 'test' channel
```
curl http://127.0.0.1:9999/api/channels/test
```

Or checking this url in a web browser
```
http://127.0.0.1:9999/api/channels/test
```

## Unfinished work

* Empty channels are not removed (no consequences)
* High frequency polling is not handled (done on another project, but)
* No security at all
    * no API keys (done on other project, but)
    * no test on https (done on other project, but)
    * any client can impersonate any other client 

