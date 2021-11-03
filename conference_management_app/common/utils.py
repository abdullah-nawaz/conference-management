from dateutil.parser import parse

def parse_timestamp(time_stamp):
    """
    Parse string to timestamp
    """
    if isinstance(time_stamp, str):
        return parse(time_stamp)
    else:
        return time_stamp
