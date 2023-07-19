import pandas as pd
import json
import base64
import data_fetcher
import ipaddress

#df = pd.read_json('data_backup.json')
#df = df

def format_data():
    data = data_fetcher.get_data_from_file()
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

def format_data_simple():
    data = data_fetcher.get_data_from_file(filename='data_backup_simple.json')
    excluded_users = users_exclusion_list()

    formatted_data = {}
    
    for log in data:
        principalId = log['PrincipalId']
        count = log['Count']

        if not principalId:
            continue
        
        # Exclude some users
        username = principalId.split(':')
        if len(username) > 1:
            userid = username[1]
            if username[1] in excluded_users:
                continue
        else:
            userid = username[0]

        if not (principalId in formatted_data):
            formatted_data[principalId] = {}

        formatted_data[principalId]['username'] = userid

        if log['Error Code']:
            if not 'errorCode' in formatted_data[principalId]:
                formatted_data[principalId]['errorCode'] = 0
            formatted_data[principalId]['errorCode'] += count

        if is_valid_ip_address(log['sourceIP']):
            network_address = ".".join(log['sourceIP'].split(".")[:2]) + ".0.0/16"
            if not network_address in formatted_data[principalId]:
                formatted_data[principalId][network_address] = 0
            formatted_data[principalId][network_address] += count

        if not log['EventSource'] in formatted_data[principalId]:
            formatted_data[principalId][log['EventSource']] = 0
        formatted_data[principalId][log['EventSource']] += count

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
    with open('exclusions.txt') as f:
        lines = f.read().splitlines()
    return lines

def main():
    #data = format_data()
    data = format_data_simple()
    df = create_dataframe(data)
    df = df.fillna(0)
    return df

if __name__ == "__main__":
    main()