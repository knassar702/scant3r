# Scant3r - Coded by Khaled Nassar @knassar702
import urllib.parse
def urlencoder(payload):
	return urllib.parse.quote(payload,safe='')
