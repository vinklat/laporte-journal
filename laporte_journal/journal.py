# -*- coding: utf-8 -*-
# pylint: disable=C0103
'''creates journaling client of Socket.IO laporte server'''

import logging
from prometheus_client import start_http_server
from laporte.client import LaporteClient
from laporte_journal.argparser import get_pars

# create logger
logger = logging.getLogger(__name__)

# get parameters from command line arguments
pars = get_pars()

# set logger
logging.basicConfig(
    format='%(asctime)-15s %(levelname)s %(module)s: %(message)s',
    level=pars.log_level)
if pars.log_level == logging.DEBUG:
    logging.getLogger('socketio').setLevel(logging.DEBUG)
    logging.getLogger('engineio').setLevel(logging.DEBUG)
else:
    logging.getLogger('socketio').setLevel(logging.WARNING)
    logging.getLogger('engineio').setLevel(logging.WARNING)

values = {}


def init_handler(nodes):
    '''
    Function launched after connect/reconnect.

    Args:
        nodes (Dict[str: Dict[str: Dict[str: Any]]]):
            dicts of node_ids with dict of sensor_ids with dicts of changed metrics
    '''
    for node_id, sensors in nodes.items():
        for sensor_id, metrics in sensors.items():
            for metric, value in metrics.items():
                if metric == 'value':
                    key = node_id + '.' + sensor_id
                    values[key] = value
                    logger.debug("initial value: %s = %s", key, value)


def update_handler(node_id, sensors):
    '''
    Function launched upon an update response.

    Args:
        node_id (str):
            a node with changed metrics
        sensors (Dict[str: Dict[str: Any]]):
            dict of sensor_ids with dicts of changed metrics
    '''

    for sensor_id, metrics in sensors.items():
        for metric, value in metrics.items():
            if metric == 'value':
                key = node_id + '.' + sensor_id
                prev_value = values[key]
                logger.info("%s: %s --> %s", key, prev_value, value)
                values[key] = value


laporte = LaporteClient(pars.sio_addr, pars.sio_port, events=True)
laporte.ns_events.init_handler = init_handler
laporte.ns_events.update_handler = update_handler


def main():
    '''start main loops'''

    # start up the server to expose promnetheus metrics.
    start_http_server(pars.port)

    # start Socket.IO loop
    laporte.loop()
