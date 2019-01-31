import requests

try:
    requests.get('https://www.latlong.net', proxies={"http":"http://110.52.235.119:9999"})
except:
    print('connect failed')
else:
    print('success')