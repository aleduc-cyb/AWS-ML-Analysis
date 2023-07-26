import json
import config
import os

global_logger = config.global_logger
config_object = config.config_object

# Getting data from a file
def get_data(filename=config_object['FILES']['databackupfile']):
    global_logger.info('Getting data from file')
    try:
        file = open(os.path.join('In', 'Data', filename), mode='r')
        file_content = file.read()
        file.close()
        file_data = json.loads(file_content)
        return file_data
    except Exception as e:
        global_logger.error("Not possible to get data from file")
        global_logger.error(str(e))
        return None