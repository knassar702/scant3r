import nimpy

# this a simple NIM script , you can use nim inside scant3r to make your script faster


proc main(url: string): string {.exportpy.} =
  return url
