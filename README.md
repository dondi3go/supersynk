# Supersynk

Supersynk is punk synchronisation of distributed data

## Why supersynk ?

Sypersynk was originaly created to synchronize VR users sharing a common VR environment.

The idea is to make something as simple as possible with as few HTTP requests as possible.
HTTP is obviously not the most efficient approach for this problem. 
The solution works yet, is simple, and VR specific usage has disappered in the meantime 
(has been displaced to application level), making it usable in other contexts.

## How does it work ?

Each client sends its data to the server, and get the data of other clients in return.
The data of a client is a dictionary of key/value pairs.
All data are in-memory stored, there is no database involved in the process.

## How to use it ?

The API is made of 2 endpoints, one for the clients who share data with the other participants of the channel, and one for  the pure observers of the channel.

### Endpoint for a participant in the channel

**POST** [ip]:[port]/synk/[channel_key]

request is :
```
{"c"="ada", "d"=[{"k"="head", "v"="UYTFUYTDI"}]}
```
response is :
```
[{"c"="joe", "d"=[{"k"="head", "v"="OIHIBEZAWREZ"}]}]
```

### Endpoint for an observer of the channel

**GET** [ip]:[port]/synk/[channel_key]

response is :
```
[{"c"="ada", "d"=[{"k"="head", "v"="UYTFUYTDI"}]}, {"c"="joe", "d"=[{"k"="head", "v"="OIHIBEZAWREZ"}]}]
```

## Running the server

```
python supersync_server.py
```

## Testing the server

```
curl 127.0.0.1:9999/api/channels
```

```
curl 127.0.0.1:9999/api/channels/tests
```

## Application side

The content of the "v" field should avoid collisions with the JSON syntax.

* One way to do it is to use conversion to/from byte64

* Another way is to use this kind of syntax :
```
"pos=0 0 0;rot=3.5 9.0 8.4 6.0;shp=rect(1);col=#457900"
```

## TODO

* [ ] Add a DTO for python clients, can ease tests

* [x] reduce size of keywords

* [ ] Refactoring ...
  * 'host' ? 
      * not the user (a user can have several application contributing to the scene)
      * not the device (for teh same reason)
      * agent ? (5 letters)
      * client
  * 'key' or 'id' ?
      * api_key mean it locks somethings
      * but "key/value" association is obvious

  * compacity : hk= nk= nv=

  "c"="hh", "d"=[{"k"=1, "v"=2}]