# Monitoring agent
This monitring agent is developed to pull PROGRAN API to get enodeb service
statistics and publish them to kafka databus. It is a server application based
on Flask framework. It can be enabled and disabled with http request.
This work can also be modified to be a generic monitoring agent framework.

## Start Agent
start monitoring agent on port 5004
```sh
python3 monitoring_agent.py
```
## Start Monitoring
t: frequency to pull service api to get service running stats
target: kafka address where the stats will be published
```sh
curl -i -H "Content-Type: application/json" -X POST -d '{"t":1,"target":"127.0.0.1:9092"}' -L http://localhost:5004/monitoring/agent/enodeb/start
```
## Stop Monitoring
```sh
curl http://localhost:5004/monitoring/agent/enodeb/stop
```
