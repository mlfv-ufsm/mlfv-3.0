import subprocess
import sys

def parse_dependencies(dependencies_str):
  parsedDependencies = dependencies_str.replace('"', '')
  parsedDependencies = parsedDependencies.split(',')
  return parsedDependencies

def install(dependencies):
  print(parse_dependencies(dependencies))
  # for dependency in parse_dependencies(dependencies):
  #   print (dependency)
    # subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])