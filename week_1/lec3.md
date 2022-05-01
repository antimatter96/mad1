# L1.3: Client-Server and Peer-to-Peer Architecture
---

Architectures

- How devices are connected to each other

- User AND system we need to connect to


---

Cleint Server

Server
-> Stores data
-> Provides data on demand
-> May perform computations


Cleint
- End users
- Will request data
- Interatctions


Network
- Connects client to server
- Data pipe [no alterations]
- Can be local


-> Explicit servers
-> Explicit users

Local systems
- both client system on same machine
- conceptually still a network

Machine client
- Need not have user interaction
- Eg Software Updates


Eg Email, WhatsApp, Web Browsing

Variants
-> Single queue
-> Multiple queue
-> Load balancing frontends

----

Peer To Peer

Data flowing both ways

No distinction b/w client/server

All peers are considered equivalent [some peers may be more equal eg high bandwith]

Error Tolerance
- Masters/Introducers
- Election/ re selection of masters
- No central

Shared Information

eg BitTorrent, IPFS

-----

Which among the following is/are true about a distributed network?

- ❌ Each system must act as both a client and a server.
- ❌ A system failure will bring entire network to a hault.
- ✅ In general, it can suffer from the failure of a certain number of nodes.
- ❌ It becomes more stable if the number of nodes increases.
