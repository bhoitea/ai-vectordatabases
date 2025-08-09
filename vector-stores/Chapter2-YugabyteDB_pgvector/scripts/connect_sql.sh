#!/bin/bash
# Change the -h hostname with the correct hostname
docker exec -it yugabyte bin/ysqlsh -h 68d2a87797ad -U yugabyte -d yugabyte
