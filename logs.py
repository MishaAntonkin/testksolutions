import json
from datetime import datetime


def write_log(result, payload, msg_error=None):
    """
    write log about all payments or errors in json format
    :param result:
    :param payload: all payments parameters
    :param msg_error:
    :return: must write log in logs.txt file
    """
    with open('logs.txt', "a+") as f:
        log_info = {"time": datetime.now().strftime('%Y-%m-%d %H-%M-%S'), 'result': result, "payload": payload}
        if msg_error is not None:
            log_info['msg_error'] = msg_error
        f.write(json.dumps(log_info))