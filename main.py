import Fetchers as fetchers
import config
import features_extractor as fe
import ml_model as ml
import argparse

global_logger = config.global_logger
config_object = config.config_object

def main():
    # Check for inputs
    args = parse_args()
    args_count = input_checks(args)

    # Perform calculation
    data = get_data(args)
    df = get_features(args, data, args_count)
    anomalies = get_anomalies(args, df)

    return anomalies

def parse_args():
    # Parse the input arguments
    parser = argparse.ArgumentParser(description='Analyze behaviors in AWS')

    # Where to get data from
    parser.add_argument('-f', '--from_file', action='store_true', help='Get data from file')
    parser.add_argument('-q', '--from_qradar', action='store_true', help='Get data from QRadar')
    parser.add_argument('-a', '--from_aws', action='store_true', help='Get data from AWS S3')

    # Specific configuration
    parser.add_argument('-tm', '--train_model', action='store_true', help='Force to retrain the model / Otherwise using .joblib files in Out/Model')
    parser.add_argument('-cf', '--calculate_features', action='store_true', help='Force to recalculate the features / Otherwise using file specified in config file under featuresdatafile in Out/Data')

    # All necessary inputs
    parser.add_argument('-df', '--data_filename', type=str, help='Name of the file to get data from / Default is specified in config file under databackupfile / Folder is In/Data')
    parser.add_argument('-ff', '--features_filename', type=str, help='Name of the file to get features from / Default is specified in config file under featuresdatafile / Folder is Out/Data')

    return parser.parse_args()

def input_checks(args):
    args_count = sum([args.from_file, args.from_qradar, args.from_aws])
    # Checking that data is fetched from one source max
    if args_count > 1:
        print("Please specify only one between -f, -q, -a")
        exit()
    # Checking that data is fetched from one source at least
    elif args_count == 0:
        print("No specific import specified - getting data from already calculated features")

    # Data filename specified but not from_file
    if (args.data_filename) and not (args.from_file):
        print("Data filename is specified but not --from_file flag. Ignoring Data filename")

    # Query data specified but features_file also specified
    if args_count>=1 and (args.features_filename):
        print("Features file specified while getting data from source - unnecessary processing will take place")
        user_input = input("Continue? Y/N")
        if user_input!="Y":
            print("Aborting")
            exit()
        else:
            print("Proceeding")
    
    return args_count

def get_data(args):
    # Get data according to args
    if args.from_file:
        if args.data_filename:
            filename = args.data_filename
        else:
            filename = config_object['FILES']['databackupfile']
        return fetchers.file.get_data(filename)
    elif args.from_aws:
        return fetchers.aws.get_data()
    elif args.from_qradar:
        query_file = config_object['QRADARPARAM']['queryfile']
        return fetchers.qradar.get_data(query_file, True)
    return None

def get_features(args, data, args_count):
    # Get features according to args
    if args.calculate_features or args_count > 0:
        df = fe.main(data=data)
    else:
        if args.data_filename:
            filename = args.features_filename
        else:
            filename = config_object['FILES']['featuresdatafile']
        df = fe.main(from_file=True, features_file=filename)
    return df

def get_anomalies(args, df):
    # Calculate anomalies according to args
    if args.train_model:
        anomalies = ml.main(df, True)
    else:
        anomalies = ml.main(df, False)
    return anomalies

if __name__ == "__main__":
    main()