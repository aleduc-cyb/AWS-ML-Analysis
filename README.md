# AWS-ML-Analysis
This Python script performs behavior analysis on AWS data using the Isolation Forest algorithm for anomaly detection. It allows users to fetch data from different sources and identify anomalies in the data.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries: Fetchers, pandas, scikit-learn, joblib

### Installation

1. Clone the repository to your local machine.
`git clone https://github.com/your_username/AWS-ML-Analysis.git`

2. Change into the cloned directory.
`cd AWS-ML-Analysis`

3. Install the required Python libraries using pip.
`pip install -r requirements`


### Usage

To run the AWS Behavior Analysis script, use the following command:

`python main.py [arguments]`


### Command-line Arguments

- `-f, --from_file`: Get data from a file.
- `-q, --from_qradar`: Get data from QRadar.
- `-a, --from_aws`: Get data from AWS S3.
- `-tm, --train_model`: Force retraining of the model. Otherwise, use .joblib files in Out/Model.
- `-cf, --calculate_features`: Force recalculation of the features. Otherwise, use the file specified in the config file under featuresdatafile in Out/Data.
- `-df, --data_filename`: Name of the file to get data from (default is specified in config file under databackupfile in In/Data).
- `-ff, --features_filename`: Name of the file to get features from (default is specified in config file under featuresdatafile in Out/Data).

