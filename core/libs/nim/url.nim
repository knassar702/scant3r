import uri, strformat


type Parser = object

proc printUri(self:Parser, url: string) =
  let res = parseUri(url)
  if res.scheme != "":
    echo &"\t  Scheme: {res.scheme}"
  if res.hostname != "":
    echo &"\tHostname: {res.hostname}"
  if res.username != "":
    echo &"\tUsername: {res.username}"
  if res.password != "":
    echo &"\tPassword: {res.password}"
  if res.path != "":
    echo &"\t    Path: {res.path}"
  if res.query != "":
    echo &"\t   Query: {res.query}"
  if res.port != "":
    echo &"\t    Port: {res.port}"


# const test = Parser()
# test.printUri("http://knassar702.github.io/?test=1")
