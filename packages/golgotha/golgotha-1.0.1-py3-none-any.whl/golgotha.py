#!/usr/bin/env python3

import sys
import re
import regex

def eprint(*args, **kwargs):
  print(f"{current_infile_name}:{line_index}:", *args, file=sys.stderr, **kwargs)

debug = False #False #True #these values here for easy copying

def dprint(*args, **kwargs):
  if debug:
    eprint(*args, **kwargs)

def parenthor(left, right, name=r"recursor\1"):
  l = re.escape(left)
  r = re.escape(right)
  p = "%s[^%s%s]*(?&%s)?[^%s%s]*%s" % (l, l, r, name, l, r, r)
  dprint("paren now!", p)
  return p

def golgothate(infile, outfile) -> None:
  global line_index
  line_index = 1 #type: ignore[name-defined] # https://github.com/python/mypy/issues/5732
  source_string = ""
  operator_rules = []
  for line in infile:
    line_index += 1 #type: ignore[name-defined] # https://github.com/python/mypy/issues/5732
    if line[0] == '🔣':
      #reading comprehension warning: this code contains regex operations on text that will be used for regex operations later. So, be wary of that.
      dprint("operator rule line encountered")
      rule = line[1:].strip('\n').split('🔜')
      dprint(rule)
      if len(rule) == 2:
        #Now, we are going to turn rule[0] from a regular string into a valid regex that does what we want
        rule[0] = re.escape(rule[0]) # first, we escape any literal characters from the string that would otherwise be interpreted as special regex characters, because we haven't put any special regex characters in yet.
        dprint(rule[0])
        rule[0] = regex.sub(
          r"(\d+)",
          r"(?P<frontspace\1>[^\\S\\r\\n]*)"+ #note that we have to \ the \S because otherwise regex tries to interpret it here, leading to a bad escape error.
          r"(?P<arg\1>\\w+"+r"|(?P<recursor\1>"+parenthor("(",")")+"|"+parenthor("[","]") + "|" + parenthor("{","}")+r"))"+
          r"(?P<rearspace\1>[^\\S\\r\\n]*)",
          rule[0]
        )
        #Now, we massage the string to be the regex we want.
        dprint(rule[0])
        rule[1] = re.sub(r"(\d+)", r"\\g<frontspace\1>\\g<arg\1>\\g<rearspace\1>", rule[1]) #rhs of rule uses proper subs, using \g form for maximum disambiguation
        dprint(rule)
        operator_rules.append(rule)
      else:
        eprint("Invalid rule (no 🔜 token?), which I will ignore:", line)
    else:
      source_string += line
  for rule in operator_rules:
    source_string = regex.sub(rule[0], rule[1], source_string)
  outfile.write(bytes(source_string, encoding='utf-8'))

def main():
  global current_infile_name
  if not sys.stdin.isatty(): #this means something is being piped to stdin
    current_infile_name = 'Standard In'
    with open(1, "wb") as outfile: #write to stdout in binary mode to avoid the usual python \n→\r\n replacement.
      golgothate(sys.stdin, outfile)
  else:
    if len(sys.argv) <= 1:
      print("USAGE: golgotha names_of_files_to_tranform... (or use stdin, which will then go to stdout)", file=sys.stderr)
      exit(2)
  for filename in sys.argv[1:]:
    current_infile_name = filename
    with open("golgotha."+filename, "wb") as outfile:
      with open(filename, "r", encoding='utf-8') as infile:
        golgothate(infile, outfile)

if __name__ == "__main__":
  main()
