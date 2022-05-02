# L1.8: What is a Protocol?

---

### Protocol

Both sides agree on how to talk

Server expects requests

- Nature of request
- Nature of client
- Types of result the client can deal with

Client expects response

- Ask server for something
- Convey what you can accept
- Read result and process

### HTTP

Text Based

Requests specified as GET, POST, PUT etc

- Headers can be used to convey acceptable respoe tpyes, languages, encoding etc
- Which host to connect to [if multiple hosts on single server]

Response Headers

- Convey message type, data
- Cache info
- Status codes

### Use Cases

GET : simple requests, search queries

POST : more complex form data, large text blocks, file uploads

PUT/DELETE :

- Rarely used in web1
- Mostly in web2.0
- Basis of most APIs -> REST, CRUD

---

###

```bash
python3 -m http.server
```

// take module http, run function server
// using http/1.0

// Gives content-type -> how to interpret this response
// Content length
// Last modiefid -> if not chnaged : no need to redraw page

- Serve files from local folder
- Understands basic http requests
- Gives more detailed headers and response

GET '/'
-> serve index.html if present
// convention

GET '/filename'
-> returns the file
-> picks apt content-type

---

**Which of the following statements is/are correct?**

- ✅ GET method is generally used to request a resource from the server.
- ✅ In GET method, data is visible in url.
- ❌ In POST method, data is visible in url.
- ✅ POST method is generally used to submit forms.

**Which among the following methods is used by the HTTP protocol to transfer data between a browser and a server?**

- ✅ Both GET and POST
