# L1.9: Performance of a Website

---

Latency
- How much time does it take to get the response for a given response

~ Speed of light in wire : 2e8

5ms for 1000km

if serever 2000km away
- one way request : 10ms
- round trip : 20ms [assuming instantaious response]

Max 50 request / second per client if done serially [wait for response from previous]

---

Resonse Size

Headers + Actual Data

- Assume 1 KB

- Network 100 Mbps [of server]
- 10 MBytes /s

=> 10,000 requests / second []

---

Google.com

Ideal ~ 144k

Handles 60,000 requests / second

-> 80 Gbps

-> Need to scale out
-> Multipe data centers

---

YouTube

- one python process - 6MB
- multiple parallel request -> mulktiple processes
- say streaming -> 2 Million viewers
- 12 TB RAM

-> Need to scale out
-> Multipe servers / data centers

---

Google

- Index 100s of billions of pages
- Cross refernce pagerank
- Total index size estimate : 100,000,000 => 100 petabytes

- Storage 
- Retrieval

---

What does RTT stand for in the context of network requests and data transfer?

- Round Trip Time

What should be the minimum bandwidth of a data center that can handle 6,250 requests per second of 200 kilobytes each?

-> 6250 * 200 KBps
-> * 8 kbps
-> /(1000 * 1000) Gbps
