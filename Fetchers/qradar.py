import search.qradar_search as qradar
import json
import config
import os

global_logger = config.global_logger
config_object = config.config_object

# Getting data from QRadar directly via API
# If needed specify store_to_file as true to export the logs to a text file to be reused
def get_data(query_file, store_to_file=False, filename=config_object['FILES']['databackupfile']):
    global_logger.info('Querying QRadar')
    try:
        results = qradar.get_all(query_file)
    except Exception as e:
        global_logger.error("Not possible to complete QRadar query")
        global_logger.error(str(e))
        return None
    
    if store_to_file:
        store_data_to_file(os.path.join('In', 'Data', filename), results['events'])
    
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