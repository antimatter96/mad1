# L1.5: Introduction to the Web

---

Generic -> works across operating systems, hardware arch

---

## History

Telephone Networks

- Circuit Switched - A and B are connected directly, via a set of wires. Physical
- These wires are tied up during the call

Packet Switch Network

- Lines connecting exchanges are bundled into one wire -> need to pack more info per second
- Wires occupied only when the data to be send
- Data instead of voice
- Netrual to type of data [bits]

ARPANet

- Node to node network [can relay through nodes as well]

Protocol

- How to format packets, place them on the wire, headers, checksums
- Each network had its own protocol :/

=> How to enable different networks to talk to each other / communicate

Inter Network Protocol

- Higher level protocol to enable diff network protocol to communicate
- Take actual data, add headers, checksums

IP : Internet Protocol

- Defines header, packet types, interpretation
- Can be carried over different underlying networks
- Only how packets are created
- Tranmission is left to underlying network arch

TCP : Transimission Control Protocol

- Establish reliable communication -> retry, error control
- Set up a somewhat closed route -> set up a circuit switch upon a packed switch network
- Reliabilty
- Autonmatically scale and adjust to network limits [speed etc]

---

Need to know address of the machine : IP address
32 bit
[0-255].[0-255].[0-255].[0-255]

Domain Names:

- Use names instead of IP addresses
- Easy to remember

- Herieachy structre
- root, subdomains

- translate domain to ip address
- can chnage ip address without any need to inform users

HyperText

- Text documents to be served
- Formatting hints inside document to "link" to other documents -> bold, heading, hyperlink [corresponds to another file]

conneccted documdenrs make the web

=> World Wide Web

---

Orignal

- Static pages
- Coplicted exexcutable interfaces
- Limited styling
- browser compatibikity

Web 2.0

- Dynamic pages -> genrate on ythe fly
- HTTP > As a transport mechanism , binary data, serialuzed data
- client side computation and rendering
- Platform agnostic operating system

Servers now computate and generate, not just serve files

---

Which of the following protocols gives priority to the reliability of data delivered?

- ✅ TCP
- IP
- ARP
- DHCP

Which among the following options is correct about the World Wide Web?

- It is a network of networks.
- ✅ It is system of interconnected resources over the internet.
- It is a set of rules that computers use to communicate over the internet.

Which among the following options is correct regarding the Internet?

✅ It is a network of networks.

Which of the following statements is/are true about TCP and UDP?

- UDP is a connection oriented protocol.
- UDP is more reliable than TCP.
- Both UDP and TCP provide acknowledgement after receiving the data.
- ✅ UDP can result in loss of data

Which of the following is a session establishment protocol between a client and a server?

- ARP
- ✅ TCP/IP
- DHCP
- UDP

Choose the correct statement(s) regarding internet protocol from the following.

- ✅ It bridges different network protocols.
- ✅ It defines a standardized header for all the network protocols.
- It requires a predefined specific network as it cannot be carried over by its underlying network.
- It establishes a reliable communication.

Which of the following statements regarding telephone networks is/are correct?

- ✅In a circuit switched network, there is a set of physical wires that connect point A to point B and back from point B to point A forming a closed loop.
- ✅In circuit switched networks, if a set of wires is engaged in a certain connection, the same set of wires cannot be used by anyone else for transmitting data.
- ✅In a packet switched network, a single set of wires can carry information between the two exchanges.
- ❌The information in a packet switched network is carried even when the data is not being sent.


Which of the following was not a limitation of the original web?

Static pages

Limited styling

Limited connectivity

Complicated executable interfaces
