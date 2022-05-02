# L1.7: Simple Web Server

---

```bash
while true; do
  echo -e "HTTP/1.1 200 OK \n\n$(date)" | nc -l localhost 1500;
done
```

Responding with HTTP/1.2
Send 'HTTP/1.1 '
Send Status Code '200 OK'
Send '\n\n' => Seperate header and data
Send 'Date'

netcat listen on localhost 1500
-> will ask OS to open port 1500 and listen
-> whenever a request comes to 1500
-> given to netcat
-> netcat will pass whatever comes from echo and send it to whoever asks


*time will be when port was opened [time of last request*

```bash
# Netcat output

GET / HTTP/1.1
Host: localhost:1500
User-Agent: curl/7.64.1
Accept: */*

```

----

Listenn on fixed port

On incoming request -> run some code and return a result
- Standard headers to be sent as part of result
- Output can be text or other format - MIME []


---

Typical Request

```log
GET / HTTP/1.1
Host: localhost:1500
User-Agent: curl/7.64.1
Accept: */*
```

Only 1st line is Mandatory
In case of HTTP/1.1 we need to specify host -> can be possible that mulitple hosts on same machine
User agent -> optional but good
Accept -> '*/*' I can accept everythinh 

Response

```log
*   Trying ::1...
* TCP_NODELAY set
* Connected to localhost (::1) port 1500 (#0)
> GET / HTTP/1.1
> Host: localhost:1500
> User-Agent: curl/7.64.1
> Accept: */*
> 
< HTTP/1.1 200 OK 
* no chunk, no close, no size. Assume close to signal end
< 
Mon  2 May 2022 07:20:07 IST
* Closing connection 0
```

* -> debug logs
'> -> Request data [BLANK line at the end is important -> tell server we are done]
'GET' '/' => Root

< -> Response
'\n\n' -> End of headers, start of data


----


Which of the following is/are loopback address(es)?

127.0.0.1 [127.0.0.0/8]
::1 [Only one actually ::1/128 => ]


0.0.0.0 in IPv6
::
::0


Which statement is correct regarding CGI?

- ❌ It is related to transfer of data from client to server.

It is an interface specification that enables web servers to execute an application program.

It is an abbreviation for common gateway interface.

All of the above


MIME : Multipurpose Internet Mail Extensions
