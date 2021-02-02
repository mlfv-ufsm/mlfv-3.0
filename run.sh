#!/bin/bash

docker-compose up -d

for i in 1 2 3 4 5; do
  python test/test_lenet.py
  echo "Finished $i"
  docker-compose restart
done;

docker-compose down