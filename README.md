# Supersynk

Supersynk is punk synchronisation of distributed data

## Why supersynk ?

Sypersynk was originaly created to synchronize VR users sharing a common VR environment.

The idea was to make something as simple as possible with as few HTTP requests as possible.

HTTP is obviously not the most efficient approach to this problem, but http libraries are available in almost every programming language and the HTTP tooling is strong. 

Far from being perfect, this HTTP solution works and is simple. 

VR specific syntax has disappeared from the original idea (it has been relocated 
to application level), making this server usable in other contexts.

## How does it work ?

Each client sends its data to the server, and get the data of other clients in return.

All data are stored in-memory,no database is involved in the process.

Clients connected to the same channel "see" each others. Clients belonging to
different channels do not interact with each others.

The server can host different channels.

## How to use it ?

The API is made of 2 endpoints, one for the clients who share data with the other 
clients of the channel, and another one for the pure observer clients of the channel.

In each use case, clients can share/get data using one and only one HTTP request.

### Endpoint for a participant in the channel

**POST** [ip]:[port]/api/channels/[channel_key]

with a request body like :
```
{"client_id":"ada"}
```
response body could be :
```
[{"client_id":"joe"}]
```

### Endpoint for an observer of the channel

**GET** [ip]:[port]/api/channels/[channel_key]

response body could be :
```
[{"client_id":"ada"}, {"client_id":"joe"}]
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

