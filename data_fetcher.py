import search.qradar_search as qradar
import json
import config
import os

global_logger = config.global_logger
config_object = config.config_object

# Getting data from QRadar directly via API
# If needed specify store_to_file as true to export the logs to a text file to be reused
def get_data_from_qradar(query_file, store_to_file=False, filename="data_backup.json"):
    global_logger.info('Querying QRadar')
    try:
        results = qradar.get_all(query_file)
    except Exception as e:
        global_logger.error("Not possible to complete QRadar query")
        global_logger.error(str(e))
        return None
    
    if store_to_file:
        store_data_to_file(filename, results['events'])

    return results

# Getting data from a file
def get_data_from_file(filename="data_backup.json"):
    global_logger.info('Getting data from file')
    try:
        file = open(filename, mode='r')
        file_content = file.read()
        file.close()
        file_data = json.loads(file_content)
        return file_data
    except Exception as e:
        global_logger.error("Not possible to get data from file")
        global_logger.error(str(e))
        return None

# Function to store data to file
def store_data_to_file(filename, data_to_store, append_mode=False):
    try:
        if append_mode:
            with open(filename, "a") as outfile:
                json.dump(data_to_store, outfile)
                outfile.write('\n')
        else:
            global_logger.info('Storing data to file')
            with open(filename, "w") as outfile:
                json.dump(data_to_store, outfile)
    except Exception as e:
        global_logger.error("Not possible to store to text file")
        global_logger.error(str(e))

# Deleting temporary file
def remove_file(filename):
    global_logger.info('Removing file')
    if os.path.exists(os.path.join('Queries', filename)):
        os.remove(os.path.join('Queries', filename))
    else:
        global_logger.warning("Not possible to remove file")
