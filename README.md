# Supersynk

Supersynk is punk synchronisation

## What is supersynk ?

Originaly created to synchronize VR users sharing the same VR environment.
The idea is to make something as simple as possible with HTTP requests.
HTTP is not the best approach for this problem yet this solution works.

## Naming conventions

The combination of host_key and node_key is unique on the channel

## How to use it ?

Supersync is synchronization server for distributed data
Consists in a polling to one endpoint : 
    * to upload local changes (request)
    * and download changes from other users (response)

API is

* POST 1.2.3.4:8090/syncserver/channel_key/
  request is :
  response is :
  This endpoint is for a participant in the scene

* GET 1.2.3.4:8090/syncserver/channel_key/
  response is :
  This endpoint is for an observer of the scene

Note : this API is not REST !

Get a state of the scene via the API
Convert it to events in the scene
Update your 3D environement

## Application side

node_val could contain any string data

pos:"0 0 0", rot:"3.5 9.0 8.4 6.0", shp:"rect(1)", col:"#457900"

## TODO

* [ ] Not same JSON structure in request and in response ... problem ?

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
  * 'key' or 'id' ?
      * api_key mean it locks somethings
      * but "key/value" association is obvious

  * compacity : hk= nk= nv=