import sys
import subprocess

def parse_dependencies(dependencies_str):
  return dependencies_str.replace('"', '').split(',')

def install(dependencies):
  for dependency in parse_dependencies(dependencies):
    try:
      __import__(dependency)
    except ImportError:
      subprocess.call('pip install ' + dependency, shell=True)
      __import__(dependency)
