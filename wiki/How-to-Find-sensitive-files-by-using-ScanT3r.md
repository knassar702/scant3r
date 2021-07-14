if you want to find intersting endpoints , you can use `paths` module for that

## Configure:
* path : `scant3r/modules/paths/payloads.yaml`

if your match value type == string that's mean find the match in response body , if match value type == integer that's mean match on response status
```yaml
# /PATH : MATCH
# match type: string > match in response body
# match type: int > match status code

"/phpinfo.php": "PHP Version"
"/PI.php": "PHP Version"
'/+CSCOT+/translation-table?type=mst&textdomain=/%2bCSCOE%2b/portal_inc.lua&default-language&lang=../': dofile("
'/pluto/portal': '<title>Pluto Portal</title>'

```

```bash
$ cat subdomains.txt | python3 scant3r.py -m paths -w 100 -R

   ____              __  ____
  / __/______ ____  / /_|_  /____
 _\ \/ __/ _ `/ _ \/ __//_ </ __/
/___/\__/\_,_/_//_/\__/____/_/


[!] Coded by : Khaled Nassar @knassar702
[!] Version : 0.7#Beta
    	

[+] Found :> http://████████/+CSCOT+/translation-table?type=mst&textdomain=/%2bCSCOE%2b/portal_inc.lua&default-language&lang=../
```