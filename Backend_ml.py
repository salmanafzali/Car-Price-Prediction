import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from pathlib import Path


# Attribute Selectortegy
class AttributeSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attributes):
        self.attr_name = attributes
        
    def fit(self, df):
        return self
    
    # return values for next process in pipeline
    def transform(self, df):
        return df[self.attr_name].values

# hourse power missing value fix over year
class EnginHpFix(BaseEstimator, TransformerMixin):
    def fit(self, df):
        return self
    
    def transform(self, df):
        year_ix, hp_ix = 0, 1        # Engine HP missing value fix over year
        df = pd.DataFrame(df)
        imputer = SimpleImputer(missing_values=np.nan, strategy='median')  
        
        df_hp_imputed_upp = imputer.fit_transform(df[df[year_ix] >= 2010][[hp_ix]])
        df_hp_imputed_upp = pd.DataFrame(df_hp_imputed_upp)
        df_hp_imputed_low = imputer.fit_transform(df[df[year_ix] < 2010][[hp_ix]])
        df_hp_imputed_low = pd.DataFrame(df_hp_imputed_low)
        df_hp_imputed = pd.concat([df_hp_imputed_upp, df_hp_imputed_low], axis=0)
        df_hp_imputed.reset_index(drop=True, inplace=True)

        # set all rows in Engin HP
        df_num_upp = df[df[year_ix] >= 2010].copy()
        df_num_low = df[df[year_ix] < 2010].copy()
        df_num = pd.concat([df_num_upp, df_num_low], axis=0)
        df_num.reset_index(drop=True, inplace=True)

        # concatinate Engin Hp to numeric values
        df_num.drop(hp_ix, axis=1, inplace=True)
        df_num = pd.concat([df_num, df_hp_imputed], axis=1)
        
        return df_num.values
    
# Category value fix
class CategoryValueFix(BaseEstimator, TransformerMixin):
    def fit(self, df):
        return self
    
    def transform(self, df):
        year_ix, fuel_ix, trans_ix = 0, 1, 2     # index column number
        
        # set rows in numeric values
        df = pd.DataFrame(df)

        # save fix value
        new_transmision = []
        new_fuel = []
        
        # fix Transmission Unknown Value
        for t, y in zip(df[trans_ix], df[year_ix]):
            if t == "UNKNOWN":
                if y >= 2000:
                    new_transmision.append("AUTOMATIC")
                else:
                    new_transmision.append("MANUAL")
            else:
                new_transmision.append(t)
            
        # fix missing value in Engin Fuel Type    
        for f in df[fuel_ix]:
            if pd.isnull(f):
                new_fuel.append("regular unleaded")
            else:
                new_fuel.append(f)
                
        df_upp = df[df[year_ix] >= 2010].copy()
        df_low = df[df[year_ix] < 2010].copy()
        
        df = pd.concat([df_upp, df_low], axis=0)
        df.reset_index(drop=True, inplace=True)
        
        df.drop([year_ix, fuel_ix, trans_ix], axis=1, inplace=True)

        # add Engine Fuel Type column value fix
        df.insert(0, 0, new_fuel)

        # add Transmission column value fix
        df.insert(1, 1, new_transmision)
        
        return df.values

class DataMining(TransformerMixin, BaseEstimator):
    __base_cars = None
    __model = None
    __base_value = None
    
    # for set y rows on other columns
    def y_set(self, df):
        df_y_upp = df[df["Year"] >= 2010].copy()
        df_y_low = df[df["Year"] < 2010].copy()

        df_y = pd.concat([df_y_upp, df_y_low], axis=0)
        df_y.reset_index(drop=True, inplace=True)
        return df_y["MSRP"]
    
    # preproccessing operation
    def preprocessing(self, df):
        attr_num = ["Year", "Engine HP", "Engine Cylinders", "Number of Doors", "highway MPG", "city mpg", "Popularity"]
        attr_cat = ["Year", "Engine Fuel Type", "Transmission Type", "Driven_Wheels", "Vehicle Size", "Vehicle Style"]

        # number preprocess
        num_pipeline = Pipeline([
            ("Attribute-selector", AttributeSelector(attributes=attr_num)),
            ("EnginHp-fix", EnginHpFix()),
            ("Simple-Imputer", SimpleImputer(missing_values=np.nan, strategy='median')),
            ("Standard-scaler", StandardScaler())
        ])

        # category preprocess
        cat_pipeline = Pipeline([
            ("Attribute-selector", AttributeSelector(attributes=attr_cat)),
            ("value_fix", CategoryValueFix()),
            ("Ordinal-Encoder", OrdinalEncoder(handle_unknown='error')),
            ("Standard-scaler", StandardScaler())
        ])

        final_pipeline = FeatureUnion(transformer_list=[
            ("number_operation", num_pipeline),
            ("category_operation", cat_pipeline)
        ])
        
        df_prepared = final_pipeline.fit_transform(df)
        df_prepared = pd.DataFrame(df_prepared)
        
        return df_prepared
    
    def fit(self, df):
        cars = pd.read_csv('D:/Code File/Project/Car_F_and_P/Car F and P.csv')
        self.__base_cars = cars
        train, te = train_test_split(cars, train_size=0.8, random_state=2)
        
        # preproccessing firs data and new data 
        cars_prepared = self.preprocessing(train)
        
        # set y first data for learn michin
        cars_y = self.y_set(train)
        
        # learn model
        rand_forest = RandomForestRegressor(n_estimators=200)
        rand_forest.fit(cars_prepared, cars_y)
        
        self.__model = rand_forest     # save model for use in transform
        
        return self
        
    # use new data frame and result
    def transform(self, df):
        # Both for small data and for accurate prediction
        base = self.__base_cars
        base["find"] = False
        df["find"] = True
        
        df = pd.concat([base, df], axis=0)
        
        # set base value in price predict
        value_upp = df[df["Year"] >= 2010].copy()
        value_low = df[df["Year"] < 2010].copy()

        df_set = pd.concat([value_upp, value_low], axis=0)
        df_set.reset_index(drop=True, inplace=True)
        find_ix = df_set[df_set["find"] == True].index
        
        # save value 
        df_set.drop(["find", "MSRP"], axis=1, inplace=True)
        self.__base_value = df_set.loc[find_ix]
        self.__base_value.reset_index(drop=True, inplace=True)

        df_x = self.preprocessing(df)
        df_x = df_x.loc[find_ix]
        
        model = self.__model
        
        # predict price
        df_y = model.predict(df_x)
        df_y = pd.DataFrame(df_y, columns=["Price"])
        
        # final data frame
        df_predicted = pd.concat([self.__base_value, df_y], axis=1)
        
        return df_predicted

# Data Base Operations
class DataBase():
    # dictionary for input values and convert to data frame
    __insert_df = {"Id": [], "Make": [], "Model": [], "Year": [], "Engine Fuel Type": [], "Engine HP": [], "Engine Cylinders": [], 
                   "Transmission Type": [], "Driven_Wheels": [], "Number of Doors": [], "Market Category": [],
                   "Vehicle Size": [], "Vehicle Style": [], "highway MPG": [], "city mpg": [], "Popularity": []}
    
    # variabel for upload data frame
    __upload_df = False
    
    __number = 0   # For more uploads
    
    __id = 1404001   # for and manual id
    
    rec_number = 1    # for name number to receive file
    
    # Merging imported data and creating a dataframe
    def insert(self, specific):
        # number inputs
        try:
            year, hp, cylinders, doors = int(specific[2].get()), float(specific[4].get()), float(specific[5].get()), float(specific[8].get())
            highway, city, popularity = int(specific[12].get()), int(specific[13].get()), int(specific[14].get())
        except ValueError:
            return "Number Unsuccessful"
        
        # Permission to not enter a value
        market = specific[9].get()
        if not market:
            market = np.nan

        # string input
        make, model, fuel, transission, wheel = specific[0].get(), specific[1].get(), specific[3].get(), specific[6].get(), specific[7].get()
        size, style = specific[10].get(), specific[11].get()

        if not make or not model:
            return "String Unsuccessful"
        
        # add value in insert df
        values = [self.__id, make, model, year, fuel, hp, cylinders, transission, wheel, doors, market, size, style, highway, city, popularity]
        
        for d, v in zip(self.__insert_df, values):
            self.__insert_df[d].append(v)
            
        car_id = self.__id
        
        self.__id += 1
        
        print(self.__insert_df)
        
        return f"Successful {car_id}"
    
    # insert value receive file to document system
    def receive(self):
        document_path = Path.home() / "Documents"
        file_path = document_path / f"Receive File {self.rec_number}.csv"   # save address
        
        if self.__insert_df["Id"]:                  # check insert value
            insert_df = pd.DataFrame(self.__insert_df)
            insert_df.to_csv(file_path, index=False)
            self.rec_number += 1
            return "Successful"
        else:
            return "Unsuccessful"
        
    def remove(self, id):
        try:
            id_car = int(id.get())
        except ValueError:
            return "ValueError"
        
        if self.__insert_df["Id"]:
            insert_df = pd.DataFrame(self.__insert_df)
            find = False
            number = 0
            for i in insert_df["Id"]:
                if i == id_car:
                    insert_df.drop(labels=number, inplace=True)
                    insert_df.reset_index(inplace=True, drop=True)
                    insert_dict = insert_df.to_dict()
                    self.__insert_df = insert_dict
                    find = True
                else:
                    number += 1
            
            if find:
                return "Successful"
            else:
                return "Not Found"
        
        else:
            return "Unsuccessful"
        
        
    # upload file function
    def upload(self, address):   
        # create df
        df = pd.read_csv(address, sep=',')
        main_columns = ['Make', 'Model', 'Year', 'Engine Fuel Type', 'Engine HP','Engine Cylinders', 'Transmission Type',
                'Driven_Wheels', 'Number of Doors', 'Market Category', 'Vehicle Size', 'Vehicle Style','highway MPG', 'city mpg', 'Popularity']
        
        data_columns = list(df.columns)
        
        if data_columns == main_columns:
            if self.__number == 0:
                self.__upload_df = df
                self.__number += 1
            else:
                self.__upload_df = pd.concat([self.__upload_df, df], axis=0)
            
            return "Successful"

        else:
            return "Unsuccessful"
        
        
    # for connect to the data mining and predict price
    def prediction(self, name):
        dm = DataMining()
        file_name = name.get()
        
        if not file_name:
            return "Not Name"
    
        if self.__number > 0 and self.__insert_df["Id"]:
            insert_df = pd.DataFrame(self.__insert_df)
            insert_df.drop("Id", axis=1, inplace=True)
            
            upload_df = self.__upload_df
            
            df = pd.concat([insert_df, upload_df], axis=0)
            
            predict_df = dm.fit_transform(df)
            
            document_path = Path.home() / "Documents"
            file_path = document_path / f"{file_name}.csv"
            predict_df.to_csv(file_path, index=False)
            
            return "Successful"
        
        elif self.__number > 0:
            upload_df = self.__upload_df
            predict_df = dm.fit_transform(upload_df)
            document_path = Path.home() / "Documents"
            file_path = document_path / f"{file_name}.csv"
            predict_df.to_csv(file_path, index=False)
            
            return "Successful"
        
        elif self.__insert_df["Id"]:
            insert_df = self.__insert_df
            insert_df = pd.DataFrame(insert_df)
            insert_df.drop("Id", axis=1, inplace=True)
            predict_df = dm.fit_transform(insert_df)
            document_path = Path.home() / "Documents"
            file_path = document_path / f"{file_name}.csv"
            predict_df.to_csv(file_path, index=False)
            return "Successful"
        
        else:
            return "Unsuccessful"
        
        
#================================Connect Data Base==============================
def upload_connect(address):
    result = db.upload(address)
    return result

def insert_connect(*Specifications):
    result = db.insert(Specifications)
    return result
              
def receive_connect():
    result = db.receive()
    return result

def remove_connect(id):
    result = db.remove(id=id)
    return result

def predict_connect(name):
    result = db.prediction(name)
    return result
    
    
db = DataBase()