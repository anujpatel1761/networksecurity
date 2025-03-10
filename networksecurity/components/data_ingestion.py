import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataIngestionConfig
import os
import sys
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


MONGO_DB_URL= os.getenv("MONGO_DB_URL")

print("MongoDB URL inside data_ingestion.py:", MONGO_DB_URL)  # Debugging output

if not MONGO_DB_URL:
    raise Exception("MongoDB connection string is missing. Check .env file.")





class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        """
        Read data from mongodb
        """
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException
        
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(str(e), sys)















# class DataIngestion:

#     def __init__ (self,data_ingestion_config:DataIngestionConfig):
#         try:
#             self.data_ingestion_config=data_ingestion_config
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
             
#     def export_collection_as_dataframe(self):
#         """
#         Read Data from mongodb
#         """
#         try:
#             database_name   =self.data_ingestion_config.database_name
#             collection_name = self.data_ingestion_config.collection_name
#             self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
#             collection = self.mongo_client[database_name][collection_name]
#             cursor = collection.find({}, {"_id": 0})  # ✅ Correct for pymongo 3.6# ✅ Use 'projection' for pymongo 3.6
#             df = pd.DataFrame(list(cursor))

#             if "_id" in df.columns.to_list():
#                 df=df.drop(columns=["_id"],axis=1)
            
#             df.replace({"na":np.nan},inplace=True)
#             return df
#         except Exception as e:
#             raise NetworkSecurityException("MongoDB query failed", sys)

#     def export_data_into_feature_store(self,dataframe: pd.DataFrame):
#         try:
#             feature_store_file_path=self.data_ingestion_config.feature_store_file_path
#             #creating folder
#             dir_path = os.path.dirname(feature_store_file_path)
#             os.makedirs(dir_path,exist_ok=True)
#             dataframe.to_csv(feature_store_file_path,index=False,header=True)
#             return dataframe
            
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)

#     def split_data_as_train_test(self,dataframe: pd.DataFrame):
#         try:
#             train_set, test_set = train_test_split(
#                 dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
#             )
#             logging.info("Performed train test split on the dataframe")

#             logging.info(
#                 "Exited split_data_as_train_test method of Data_Ingestion class"
#             )
            
#             dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
#             os.makedirs(dir_path, exist_ok=True)
            
#             logging.info(f"Exporting train and test file path.")
            
#             train_set.to_csv(
#                 self.data_ingestion_config.training_file_path, index=False, header=True
#             )

#             test_set.to_csv(
#                 self.data_ingestion_config.testing_file_path, index=False, header=True
#             )
#             logging.info(f"Exported train and test file path.")

            
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
#     def initiate_data_ingestion(self):
#         try:
#             dataframe = self.export_collection_as_dataframe()
#             dataframe = self.export_data_into_feature_store(dataframe)
#             self.split_data_as_train_test(dataframe)
#             dataingestionartifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
#                                                           test_file_path=self.data_ingestion_config)
#             return dataingestionartifact
        
#         except Exception as e:
#             raise NetworkSecurityException(str(e), sys)

        