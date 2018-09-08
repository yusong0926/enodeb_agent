#from flask import request, Request, jsonify
#from flask import Flask
#from flask import make_response
import logging
import logging.handlers
import logging.config

"""
logging_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logging_format)
logging = logging.getLogger('enodeb_stats')
logging.setLevel(logging.DEBUG)
"""

"""
def get_enodebs(data):
    try:
        #r = requests.get(url = URL)
        enodebs = [e['eNBId'] for e in data["EnodeBArray"]]
        return enodebs
    except Exception:
        logging.warning("Couldn't get Enodeb information")
        return None 
"""

def get_enodeb_stats(data, enodeb, p_specs):

    logging.debug("start to parse stats of enodeb %s", enodeb)
    logging.debug("raw stats: %s", data)
    logging.debug("profile specs %s", p_specs)
    try:
        stats = []
        for p in data['EnodeBStatsArray']:
            logging.debug("start to parse stats of profile %s", p.get('Profile'))
            for s in p['StatsArray']:
                sd = {}
                sd['enodeb'] = enodeb
                if (p.get('Profile') and p_specs.get(p['Profile'])):
                    sd['profile'] = p['Profile']
                    sd['dlallocrbrate'] = p_specs[p['Profile']]['dlallocrbrate']
                    sd['ulallocrbrate'] = p_specs[p['Profile']]['ulallocrbrate']
                    sd['time'] = s['Time']
                    sd['dlbitrate'] = s['DlBitrate']
                    sd['ulbitrate'] = s['UlBitrate']
                    sd['event-type'] = "ran-status"
                    stats.append(sd)
        return stats 
    except Exception:
        logging.warning("Couldn't get Enodeb stats")
        return [] 


def get_profile_specs(data):

    p_specs = {}
    logging.debug("start to parse profile specs raw %s", data)
    try:
        for p in data['ProfileArray']:
            dlallocrbrate = p.get('DlAllocRBRate')
            ulallocrbrate = p.get('UlAllocRBRate')
            p_name = p.get('Name')
            specs = {}
            specs['dlallocrbrate'] = dlallocrbrate;
            specs['ulallocrbrate'] = ulallocrbrate;
            p_specs[p_name] = specs
        return p_specs
    except Exception:
        logging.warning("Couldn't get Enodeb Profile specs")
        return {}

