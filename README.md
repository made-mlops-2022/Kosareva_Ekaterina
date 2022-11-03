# Kosareva_Ekaterina

# File structure:

	| congif
	|  ├──config1.yaml
	|  ├──config2.yaml
	| data
	|  ├──data_test.csv
	|  ├──data_train.csv
	|  ├──generate_synthetic.py
	|  ├──synthetic_data.csv
	| logs
	|  ├──test_log.log
	|  ├──train_log.log
	| models
	|  ├──predictions.csv
	|  ├──rfc_model.sav
	| notebooks
	|  ├──EDA+model.ipynb
	| predict.py
	| testy_train.py
	| train.py

# Setup
## Envs
  - Linux
  - Python>=3.6
  - Istall python packages

	git clone -------
	cd -------
	pip install -r requirements.txt
       
# Train

	1) Train with configuration file:

	python3 train.py --config config/config1.yaml

	[options]
	train_data: data/data_train.csv
	target: condition
	save_path: models/rfc_model.sav
	n_estimators: 100
	max_depth: 3
	random_state: 42

	2) Train with params:

	python3 train.py --train-data "directory with data" --n-estimators N --max-depth D --random-state RS --target "target name" --save-path "model name"

	By default:
  	--train-data: data/train_data.csv
  	--n-estimators: 50
  	--max-depth: 7
  	--random-state: 0
  	--target: 'condition'
 		--save-path: models/rfc_model.sav 

# Predict

	python3 predict.py --test-data "path to file with data" --model-path "path to trained model"  --save-results "path to file for predictions"

	By default:
  		--test-data: data/data_test.csv
   		--model-path: models/rfc_model.sav
   		--save-results: models/predictions.csv

# Logging
Example of log file for training:
    
    2022-11-03 07:17:23,323 DEBUG Training is starting...
    2022-11-03 07:17:23,328 INFO Data loaded...
    2022-11-03 07:17:23,328 INFO The number of training samples = 300
    2022-11-03 07:17:23,328 INFO Model initialization ...
    2022-11-03 07:17:23,328 DEBUG Model training is started....
    2022-11-03 07:17:23,328 INFO Model RandomForest params: data = data/synthetic_data.csv, n_estimators = 10, max_depth = 5, random_state = 42
    2022-11-03 07:17:23,346 DEBUG Model trained successfuly with accuracy 0.86
    2022-11-03 07:17:23,347 INFO Model was saved

Example of log file for prediction:

    2022-11-03 07:23:03,691 DEBUG Load test data...
    2022-11-03 07:23:03,697 INFO The number of testing samples = 60
    2022-11-03 07:23:03,697 INFO Test data loaded
    2022-11-03 07:23:03,697 DEBUG Load model...
    2022-11-03 07:23:04,189 INFO Model successfully loaded...
    2022-11-03 07:23:04,190 DEBUG Prediction is started...
    2022-11-03 07:23:04,195 INFO Results saved to models/predictions.csv
