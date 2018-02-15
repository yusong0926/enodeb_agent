#from flask import request, Request, jsonify
#from flask import Flask
#from flask import make_response
import logging
import logging.handlers
import logging.config

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('enodeb_stats')
logger.setLevel(logging.DEBUG)

"""
def get_enodebs(data):
    try:
        #r = requests.get(url = URL)
        enodebs = [e['eNBId'] for e in data["EnodeBArray"]]
        return enodebs
    except Exception:
        logger.warning("Couldn't get Enodeb information")
        return None 
"""

def get_enodeb_stats(data, enodeb, p_specs):
    #r = requests.get(url = URL+'/'+enodeb)
    #data = r.json()
    logger.debug(data)
    logger.debug(enodeb)
    logger.debug(p_specs)
    try:
        stats = []
        for p in data['EnodeBStatsArray']:
            logger.debug(p)
            for s in p['StatsArray']:
                sd = {}
                sd['enodeb'] = enodeb
                sd['profile'] = p['Profile']
                sd['dlallocrbrate'] = p_specs[p['Profile']]['dlallocrbrate']
                sd['ulallocrbrate'] = p_specs[p['Profile']]['ulallocrbrate']
                sd['time'] = s['Time']/1000
                sd['dlbitrate'] = s['DlBitrate']
                sd['ulbitrate'] = s['UlBitrate']
                stats.append(sd)
        return stats 
    except Exception:
        logger.warning("Couldn't get Enodeb stats")
        return [] 

def get_profile_specs(data):
    #r = requests.get(url = URL + '/'+'profile')
    #data = r.json()
    p_specs = {}
    logger.debug(data)
    try:
        for p in data['ProfileArray']:
            logger.debug(type(p))
            logger.debug(p)
            dlallocrbrate = p.get('DlAllocRBRate')
            ulallocrbrate = p.get('UlAllocRBRate')
            p_name = p.get('Name')
            specs = {}
            specs['dlallocrbrate'] = dlallocrbrate;
            specs['ulallocrbrate'] = ulallocrbrate;
            p_specs[p_name] = specs
        return p_specs
    except Exception:
        logger.warning("Couldn't get Enodeb Profile specs")
        return {}

