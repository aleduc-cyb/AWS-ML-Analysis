import pandas as pd
import json
import base64
import ipaddress
import os
import config

config_object = config.config_object

def format_data(data):
    excluded_users = users_exclusion_list()

    formatted_data = {}
    for log in data:
        # Parse the log
        parsed_log = parse_log(log)
        
        # If there is a problem during decoding, go to next
        if not parsed_log:
            continue

        # If there is no identifiable user, go to next
        if not ('principalId' in parsed_log['userIdentity']):
            continue

        # Get the username
        principalId = parsed_log['userIdentity']['principalId']

        # Exclude some users
        username = principalId.split(':')
        if len(username) > 1:
            if username[1] in excluded_users:
                continue

        # Create new dict for user
        if not principalId in formatted_data:
            formatted_data[principalId] = {}

        # Get the errors
        if 'errorCode' in parsed_log:
            if not 'errorCode' in formatted_data[principalId]:
                formatted_data[principalId]['errorCode']  = 0
            formatted_data[principalId]['errorCode'] += 1

        # Get all the different sources
        if not parsed_log['eventSource'] in formatted_data[principalId]:
            formatted_data[principalId][parsed_log['eventSource']] = 0
        formatted_data[principalId][parsed_log['eventSource']] += 1

        # If no sourceIPAddress, then no addition
        if not ('sourceIPAddress' in parsed_log):
            continue
        
        # Get the data for the IP addresses
        if is_valid_ip_address(parsed_log['sourceIPAddress']):
            if not 'IP' in formatted_data[principalId]:
                network_address = ".".join(parsed_log['sourceIPAddress'].split(".")[:2]) + ".0.0/16"
                if not network_address in formatted_data[principalId]:
                    formatted_data[principalId][network_address] = 0
                formatted_data[principalId][network_address] += 1
    
    return formatted_data

def create_dataframe(data):
    df = pd.DataFrame.from_dict(data, orient='index')
    return df

def parse_log(log):
    try:
        json_string = base64.b64decode(log['Payload']).decode('utf-8')
        return json.loads(json_string)
    except:
        return None

def is_valid_ip_address(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False

def users_exclusion_list():
    with open(os.path.join('In', 'Data', config_object['FILES']['exclusionsfile'])) as f:
        lines = f.read().splitlines()
    return lines

def get_features_from_file():
    df = pd.read_csv(os.path.join('Out', 'Data', config_object['FILES']['featuresdatafile']), index_col=0)
    return df

def main(data=None, from_file=False, features_file=config_object['FILES']['featuresdatafile']):
    if from_file:
        df = get_features_from_file()
    else: 
        formatted_data = format_data(data)
        df = create_dataframe(formatted_data)
        df = df.fillna(0)
        df.to_csv(os.path.join('Out', 'Data', features_file))
    return df