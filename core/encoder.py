import urllib.parse
def urlencoder(payload):
	return urllib.parse.quote(payload,safe='')