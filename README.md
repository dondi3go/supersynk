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

## Application side

The content of the value in the key/value pairs should avoid any collision with the JSON syntax.

* One way to do it is conversion to/from byte64

* Another way is to use this kind of syntax :
```
pos=0 0 0;rot=3.5 9.0 8.4 6.0;shp=rect(1);col=#457900
```

## TODO

* [] Add a DTO for python clients, can ease tests

* [ ] reduce size of keywords

* [ ] In object Channel :
    * Store a timestamp for each host update
        * pass timestamp as a parameter in update() ? : 'update(s, timestamp)'
    * add 'channel.set_host_timestamp(host_key)'
    * add 'channel.is_host_disconnected(host_key, timeout)'
    * add 'channel.remove_disconnected_hosts(timeout)'

* [ ] Add object Channels :
    * channels.update(channel_key:str, s:str)
    * channels.clean_up(timeout : )
        * timeout is the amount of time to consider a host as disconnected
        * clean_up nodes inside channel (remove_disconnected_hosts)
        * clean_up empty channels (containg no host)

* [ ] In the clients, consider using base64 to encode data in node_val
    * Create a synk_node_DTO where val is automaticaly converted

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