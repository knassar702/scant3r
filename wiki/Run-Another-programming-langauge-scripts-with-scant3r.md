for sure scant3r works on modules written in python, but you run your tools/scripts with scant3r

for example this my golang script

```golang
package main

import (
    "fmt"
    "os"
)

func main() {

    argsWithProg := os.Args
    fmt.Println(argsWithProg)
}
```

* Create a folder for your script 

* write `run.yaml` file and add what the command of your module

```yaml
# SCPATH = modules/MODULE_NAME/

exec: echo {url} | go run $SCPATH/main.go -t {timeout} -d {domain}
```

```
├── test_go
│   └── main.go
|   └── run.yaml 
```

* run your script

```
knassar702@OurPc:~/myprojects/scant3r(master⚡) » echo 'https://php.net' | ./scant3r.py -m test_go

   ____              __  ____
  / __/______ ____  / /_|_  /____
 _\ \/ __/ _ `/ _ \/ __//_ </ __/
/___/\__/\_,_/_//_/\__/____/_/

[!] Coded by: Khaled Nassar @knassar702
[!] Version: 0.7#Beta

[test_go] >>> |
  output: [/tmp/go-build2110072685/b001/exe/main https://php.net -d php.net -t 10]

```
