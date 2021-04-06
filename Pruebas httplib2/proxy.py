import urllib.request


print(urllib.request.getproxies())
proxies = urllib.request.getproxies()
print(proxies.get('http'))
