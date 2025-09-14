# Car Price Prediction
A program to predict car prices from 1990 to 2017 with data mining

## Features
- Implementing the program with data mining
- Having a user interface with tkinter
- Ability to add and delete cars
- Receiving imported car files
- Ability to upload multiple files
- Simultaneously predicting the uploaded file and imported cars
- Saving results as a csv file

## Prerequisites
Minimum requirement of Python 3 and above
Requirement to install tkinter, scikit-learn, pandas, numpy, matplotlib libraries
Requirement to install the xgboost library if running the data mining process

- Installing libraries:

pip install scikit-learn
pip install pandas
pip install numpy
pip install matplotlib
pip install tkinter
pip install xgboost


## How to run
python front.py

## Structure Project
car_F_and_P
- pycache\
- Images\                                       # Folder for project images
- ├── car_main.png                                # Main page image
- ├── delete_main.png                             # Delete page image
- ├── desert-white-5120x2880-21880.jpg            # Downloaded main image
- ├── desert-white-5120x2880-21880.png            # Product import page image
- ├── mclaren-speedtail-3840x2160-23016.jpg       # Downloaded main image
- ├── predict_main.png                            # Prediction page image
- └── up_main.png                                 # Upload page image
- Backend_ml.py                                 # Project working codes and their functions
- Car F and P.csv                               # Main dataset for data mining implementation
- data_mining.ipynb                             # Data analysis and data step implementation Mining
- front.py                                      # Implement the frontend
- README.text                                   # Help file