#!/usr/bin/python
#File name: model.py
#Author: Luke Morrow
#Date Created: 7/16/2018
#Python Version: 3.6
import sys, os
import include.stack as stack
import collections

class Model(object):
  def __init__(self):
    self.fileCounts = collections.Counter()
    self.files = collections.defaultdict(list)

  def findDupes(self, dir):
    self.walk(dir)
    dupes = [self.files[i] for i in self.fileCounts if self.fileCounts[i] > 1]
    self.files.clear() #reset file counts
    self.fileCounts.clear()
    print("The", len(dupes), "duplicate files are")
    return dupes

  def walk(self, dir):
    stk = stack.stack()
    stk.push(dir)
    while not stk.empty():
      directory = stk.top()
      stk.pop()
      files = os.listdir(directory)
      for thisFile in files:
        name = os.path.join(directory, thisFile)
        if os.path.isdir(name):
          stk.push( name )
        else:
          self.files[thisFile].append(name)
          self.fileCounts[thisFile] += 1

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("usage:", sys.argv[0], "<dir>")
    sys.exit(1)
  if not os.path.isdir(sys.argv[1]):
    print(sys.argv[1], "isn't a directory")
    sys.exit(1)

  walker = Model()
  walker.findDupes(sys.argv[1])
