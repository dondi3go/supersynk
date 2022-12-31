# Supersynk

Supersynk is punk synchronisation of distributed data

## Why supersynk ?

Sypersynk was originaly created to synchronize VR users sharing a common VR environment.

The idea is to make something as simple as possible with as few HTTP requests as possible.
HTTP is obviously not the most efficient approach for this problem. 
The solution works yet, is simple, and VR specific syntax has disappeared 
(has been relocated to application level), making it usable in other contexts.

## How does it work ?

Each client sends its data to the server, and get the data of other clients in return.
The data of a client is a dictionary of key/value pairs.
All data are in-memory stored, there is no database involved in the process.

## How to use it ?

The API is made of 2 endpoints, one for the clients who share data with the other participants of the channel, and one for  the pure observers of the channel.

### Endpoint for a participant in the channel

**POST** [ip]:[port]/synk/[channel_key]

with a request body like :
```
{"c":"ada", "n":[{"k":"head", "v":"UYTFUYTDI"}]}
```
response body could be :
```
[{"c":"joe", "n":[{"k":"head", "v":"OIHIBEZAWREZ"}]}]
```

### Endpoint for an observer of the channel

**GET** [ip]:[port]/synk/[channel_key]

response body could be :
```
[{"c":"ada", "n":[{"k":"head", "v":"UYTFUYTDI"}]}, {"c":"joe", "n":[{"k":"head", "v":"OIHIBEZAWREZ"}]}]
```

## Running the server

```
python supersync_server.py
```

## Testing the server

```
curl -X POST 127.0.0.1:9999/api/channels/tests -H 'Content-Type: application/json' -d '{"c":"ada", "n":[{"k":"head", "v":"UYTFUYTDI"}]}' 
```

```
curl 127.0.0.1:9999/api/channels
```

```
curl 127.0.0.1:9999/api/channels/tests
```

## Application side

The content of the "v" field should avoid collisions with the JSON syntax.

* One way to do it is to use conversion to/from byte64

* Another way is to use a syntax different from json, for example :
```
"pos=0 0 0;rot=3.5 9.0 8.4 6.0;shp=rect(1);col=#457900"
```

## TODO

* [ ] Add a DTO for python clients, can ease tests

* [ ] Use json validation