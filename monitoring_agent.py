#!/usr/bin/python
import requests
from flask import request, Request, jsonify
from flask import Flask
from flask import make_response
import logging
import logging.handlers
import logging.config
import enodeb_stats as stats
import threading
import subprocess
import six
#from urllib.parse import urlparse
from kafka import KafkaProducer
import atexit
import time
from random import randint

app = Flask(__name__)

produce_topic = 'event-raw'
kafka_broker = '127.0.0.1:9092'
producer = None
start_publish = False

enodeb_demo = "302"
profile_demo = "video-slice"
onos_url = "10.128.13.3:8183"

enodebs_url = "http://"+onos_url+"/onos/progran/enodeb"
enodeb_stats_url = "http://"+onos_url+"/onos/progran/stats/enodeb"
profile_url = "http://"+onos_url+"/onos/progran/profile"
t = 2 

#enodeb_log = open("enodeb_log.txt",'w')

"""
logging_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logging_format)
logging = logging.getLogger('enodeb_agent')
logging.setLevel(logging.DEBUG)
"""

def shutdown_hook(kafka_producer):
    """
    a shutdown hook to be called before the shutdown
    :param kafka_consumer: instance of a kafka consumer
    :return: None
    """
    logging.info('Shutdown kafka producer')
    kafka_producer.close()
    #enodeb_log.close()


@app.route('/')
def index():
    logging.info('monitoring agent')
    print ("monitoring agent") 
    return "monitoring agent"

@app.route('/monitoring/agent/enodeb/start',methods=['POST'])
def service_start_monitoring_agent():
    global start_publish, t, producer
    try:
        # To do validation of user inputs for all the functions
        target = request.json['target']
        if isinstance(request.json.get('t'), int):
            t = request.json['t']
        else:
            logging.info("polling time needs to be integer")
            return "polling time need to be integer"
        logging.info("target:%s",target)
        logging.info("polling interval t:%s", t)
        #url = urlparse(target)
        kafka_broker = target
        logging.debug("kafka_broker:%s", kafka_broker)
        producer = KafkaProducer(bootstrap_servers = kafka_broker) 
        atexit.register(shutdown_hook, producer)
        start_publish = True
        periodic_publish()

        logging.info("Enodeb monitoring is enabled")
        return "Enodeb monitoring is enabled"
    except Exception as e:
            return e.__str__()

@app.route('/monitoring/agent/enodeb/stop',methods=['POST'])
def service_stop():
    global start_publish
    start_publish = False
    logging.info ("Enodeb monitoring is stopped")
    return "Enodeb monitoring is stopped"


def publish_stats(enodeb_stats):
    global producer
    try:
        for e in enodeb_stats:
            msg = 'enodeb' + ',' + str(e)   
            producer.send(topic=produce_topic, key=str(e['enodeb']).encode('utf-8'), value=msg.encode('utf-8'))
            logging.info('Publishing Enodeb event: %s', msg)
            #enodeb_log.write(str(e)+'\n')
    except Exception as e:
            return e.__str__()

def periodic_publish():
    global start_publish
    if not start_publish:
        return
    logging.debug('start periodic publish...')
    try:
        r1 = requests.get(url = profile_url)
        r1_json = r1.json()
        p_specs = stats.get_profile_specs(r1_json)
        logging.debug("profile specs:%s", str(p_specs))
        if len(p_specs):
            ###fixed enodeb id for demo 
            """
            #r2 = requests.get(url = enodebs_URL)
            #r2_json = r2.json()
            #enodebs = stats.get_enodebs(r2_json)
            """
            enodebs = [enodeb_demo]
            for enodeb in enodebs:
                r3 = requests.get(url = enodeb_stats_url+'/'+enodeb+'/'+'1')
                logging.debug('calling %s to get enodeb stats',
                        enodeb_stats_url+'/'+enodeb+'/'+'1')
                r3_json = r3.json()
                enodeb_stats = stats.get_enodeb_stats(r3_json, enodeb, p_specs)
                logging.debug("enodeb stats:%s", str(enodeb_stats))
                if len(enodeb_stats):
                    publish_stats(enodeb_stats)
        else:
            logging.warn("no profile specs found")

        threading.Timer(t, periodic_publish).start()
    except Exception as e:
         return e.__str__()


if __name__ == "__main__":
    logging.config.fileConfig('monitoring_agent.conf',
            disable_existing_loggers=False)
    logging.info ("Service monitoring is listening on port 5004")
    app.run(host="0.0.0.0",port=5004,debug=False)
