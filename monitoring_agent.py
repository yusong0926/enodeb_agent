#!/usr/bin/python
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

enodeb_demo = "20"
onos_url = "0.0.0.0"
enodebs_url = "http://"+onos_url+"api/enodeb"
enodeb_stats_url = "http://"+onos_url+"/api/stats/enodeb"
profile_url = "http://"+onos_url+"api/profile"
t = 10

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('enodeb_agent')
logger.setLevel(logging.DEBUG)

def shutdown_hook(kafka_producer):
    """
    a shutdown hook to be called before the shutdown
    :param kafka_consumer: instance of a kafka consumer
    :return: None
    """
    logger.info('Shutdown kafka producer')
    kafka_producer.close()


@app.route('/')
def index():
    logger.info('monitoring agent')
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
            logger.info("polling time needs to be integer")
            return "polling time need to be integer"

        logger.info("target:%s",target)
        logger.info("polling interval t:%s", t)
        #url = urlparse(target)
        kafka_broker = target
        logger.debug(kafka_broker)
        #producer = KafkaProducer(bootstrap_servers = kafka_broker) 
        atexit.register(shutdown_hook, producer)
        start_publish = True
        periodic_publish()

        logger.info("Enodeb monitoring is enabled")
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
            #producer.send(topic=produce_topic, key=str(e['enodeb']).encode('utf-8'), value=msg.encode('utf-8'))
            logging.debug('Publishing Enodeb event: %s', msg)
    except Exception as e:
            return e.__str__()

def periodic_publish():
    global start_publish
    if not start_publish:
        return
    logging.debug('start periodic publish...')
    try:
        #r1 = requests.get(url = profile_URL)
        #r1_json = r1.json()
        r1_json = {
      "ProfileArray" : [
        {
        "Name" : "Profile-1"  ,     
        "DlSchedType"   : "RR",   
        "DlAllocRBRate" : 70,     
        "UlSchedType"   : "RR",        
        "UlAllocRBRate" : 70  , 
        "Start" : "15/05/2015 9:00",    
        "End" :"15/05/2015 18:00" , 
        "AdmControl" : 0 ,               
        "CellIndividualOffset":0
         },
        {
        "Name" : "Profile-2"  ,     
        "DlSchedType"   : "RR",   
        "DlAllocRBRate" : 70,     
        "UlSchedType"   : "RR",        
        "UlAllocRBRate" : 70  , 
        "Start" : "15/05/2015 9:00",    
        "End" :"15/05/2015 18:00" , 
        "AdmControl" : 0 ,               
        "CellIndividualOffset":0
         }]}
        p_specs = stats.get_profile_specs(r1_json)
        if len(p_specs):
            #r2 = requests.get(url = enodebs_URL)
            #r2_json = r2.json()
            #enodebs = stats.get_enodebs(r2_json)
            enodebs = [enodeb_demo]
            for enodeb in enodebs:
                #r3 = requests.get(url = enodeb_stats_url+'/'+enodeb+'/'+'1')
                logging.debug('calling %s to get enodeb stats', enodeb_stats_url)
                #r3_json = r3.json()
                r3_json = {
                   "EnodeBStatsArray" :[
                   {
                    "Profile"  : "Profile-1",
                    "StatsArray" :[
                      {
                        "Time"      :   time.time(),
                        "DlBitrate" :   randint(0,40), 
                        "UlBitrate" :   randint(0,40)
                      }
                     ]
                    },
                   {
                     "Profile"  : "Profile-2",
                     "StatsArray" :[
                     {
                       "Time"      :   time.time(),
                       "DlBitrate" :   randint(0,40), 
                       "UlBitrate" :   randint(0,40)
                     }
                     ]
                    }
                   ]
                }
                enodeb_stats = stats.get_enodeb_stats(r3_json, enodeb, p_specs)
                logger.debug("enodeb stats:%s", str(enodeb_stats))
                if len(enodeb_stats):
                    publish_stats(enodeb_stats)

        threading.Timer(t, periodic_publish).start()
    except Exception as e:
         return e.__str__()


if __name__ == "__main__":
    logging.config.fileConfig('monitoring_agent.conf',
            disable_existing_loggers=True)
    logging.info ("Service monitoring is listening on port 5004")
    app.run(host="0.0.0.0",port=5004,debug=False)
