import data_fetcher
import config

global_logger = config.global_logger
config_object = config.config_object

def main():
    query_file = config_object['QRADARPARAM']['queryfile']
    data = data_fetcher.get_data_from_qradar(query_file, True)
    #data = data_fetcher.get_data_from_file()
    data = data

def main_simple():
    query_file = config_object['QRADARPARAM']['queryfilesimple']
    data = data_fetcher.get_data_from_qradar(query_file, True, filename='data_backup_simple.json')
    data = data

if __name__ == "__main__":
    #main()
    main_simple()