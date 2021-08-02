import nimpy,uri

type Parser = object

proc printUri(self:Parser, url: string): string {.exportpy.} =
  let res = "YES", parseUri(url).hostname
  return res

# const test = Parser()
# test.printUri("http://knassar702.github.io/?test=1")
