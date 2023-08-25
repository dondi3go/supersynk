# supersynk

Punk synchronisation for cyberspace : the server

## Why supersynk ?

*supersynk* was originaly created to synchronize VR users sharing a common VR 
environment. The project started during the 2020 lockdown as a way to meet 
VR aware friends (having VR helmets at home) considering video meeting as,
well, not as fun as VR.

The first version of this project was considered (by me) having some embarrasing 
limitions :
* the server was dependant on application-level data
* there was only one channel
* the name of the project was not fun enough

The idea was and is still to make something as simple as possible with as few HTTP requests 
as possible.

HTTP is obviously not the most efficient approach to solve this problem but HTTP 
libraries are available in almost every programming language, so writing
a client for *supersynk* should be quite easy. Furthermore, HTTP tooling is strong.

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

**POST** http://[ip]:[port]/api/channels/[channel_key]

with a request body like :
```
{"client_id":"ada" ... }
```
response body could be :
```
[{"client_id":"joe" ...}]
```

### Endpoint for an observer of the channel

**GET** http://[ip]:[port]/api/channels/[channel_key]

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
Warning : the disconnection timespan is quite low, you have to be fast between your *curl* command and a 
refresh of your favorite web browser.  

## Unfinished work

* Empty channels are not removed (no consequences)
* No security at all :
    * no API key (done on other project, but)
    * no test on https (done on other project, but)
    * any client can impersonate any other client
 
## The awfull truth about HTTP 

HTTP is everywhere, HTTP is easy, HTTP brings connectivity to the everyone, it looks
like the obvious *go to* solution to every problem. 

But something strange starts to occur as soon as you poll your server at a periods
that are closer and closer to the process time of your requests. If you use HTTP
for animation, as this project aims to do, you begin to notice small glitches. Some
vibrations appears, all the more than many clients are connected, or your network is
overloaded, or your server is fighting with its own resources.

The truth *everybody knows* is : nothing can garanty that HTTP responses are receives in the
same order requests were emitted. What are the consequences when using HTTP to perform 3D 
animations ? A client can receive, from time to time, older positions of an object, breaking 
the fluidity of its movement.

What can be done ? You can questions your choices in life, like *why HTTP, I knew it 
would have limitations ?* or you can prefer quick and not that beautyfull fixes over 
heavy rethinking, because you are punk. Well, in fact disorder is punk, but I would prefer
my animations to be nice and this project not to suffer from too many embarassing issues.

What can be done fast about this disorder ? This is what I did. As the latence can occur
on the way between the client and the server, or on the way back, between the server and
the client, I decided to discard all the requests arriving **late** on the server, or
the responses arriving **late** on the client. To do that, I used the HTTP request and 
HTTP response headers to store the emission time, only took into account the messages in 
an increasing time order, and forget the others.

Why using headers and not the payload of the requests ? Because the payload is for more 
for application logic, and the HTTP disorder issue is more a protocol issue (HTTP, I like 
you anyway). 

What do I mean by *forget the others* ? When a message arrives **late** on the server, its 
content is ignored (I already have a more up-to-date content stored on this server) and 
an empty reponse is sent (code 204). When a message arrives **late** on the client, it does 
not lead to any update.

So far, so good, but something has been written about making *something as simple as 
possible* ? Where is the simplicity, if the client has to handle special headers ? Well,
once again, my answer is : this is a punk personnal project. I only solve the problems I
choose to solve, and I don't even pretend they are chosen with great care.
