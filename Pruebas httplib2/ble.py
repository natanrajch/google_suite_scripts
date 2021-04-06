import httplib2
http = httplib2.Http(proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP_NO_TUNNEL,"mtvtmg01",8080) )
resp, content = http.request("http://google.com", "GET")
print(Resp)
