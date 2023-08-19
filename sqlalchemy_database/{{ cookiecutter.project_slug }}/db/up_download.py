import pandas as pd
import numpy as np
import os
import sys
sys.path.append("..")
home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)
from . import dataModel

from glob import glob

from typing import List, Dict, Union, Tuple

import warnings
warnings.filterwarnings("ignore")

### helper funcs
from db.helper_functions import HelperFunctions

## crud
from db.crud import BulkUpload

class UploadData(HelperFunctions):

    """The UploadData class is the core of the upload process. In this class, there are functions which are used to upload data
        to different tables in the database
    """

    def __init__(self):
        self.engine = dataModel.engine

    def upload_info(self, df:pd.DataFrame = pd.DataFrame(), dbTable:str ='', cols_dict = {"base_url":"base_url"}):
        '''
        General upload function which should be able to upload anything thrown at it
        Usage: upload_info(df=geos_df, dbTable = "dataModel.Geos", cols_dict = {"geo":"geo"})
        '''

        dbTable_evl = eval(dbTable)

        for col in list(cols_dict.keys()):
            df = df[~df[col].isna()]
            df = df[~df[col].duplicated()].reset_index(drop=True)

        df = self.replace_nan_with_none(df)
        bulk = BulkUpload(dbTable, self.engine)
        bulk.upsert_table(dbTable_evl, df, cols_dict, True)

    def upload_info_atomic(self, dbTable:str ='', df:pd.DataFrame = pd.DataFrame(), unique_idx_elements:list = [], column_update_fields:list = []) -> List[int]:
        '''
        General upload function which should be able to upload anything thrown at it
        Usage:
        idx_cols = ["somecolone", "somecoltwo"] -> a list of columns which have a UniqueConstraint and which when taken together give us a unique row in the table
        update_cols = ["someupdatecolone", "someupdatecoltwo"] -> a lost of columns we want to update

        row_id_x = upload.upload_info_atomic(
                                dbTable="dataModel.User",
                                df=import_df_unformatted[update_cols + idx_cols],
                                unique_idx_elements=idx_cols,
                                column_update_fields=update_cols,
                            )

        where row_id_x is a list of id of inserted or updated records

        '''

        for col in unique_idx_elements:
            df = df[~df[col].isna()]
        
        df = df.drop_duplicates(subset=unique_idx_elements).reset_index(drop=True)

        df = self.replace_nan_with_none(df)
        bulk = BulkUpload(dbTable, self.engine)

        row_ids = bulk.atomic_bulk_upsert(df, unique_idx_elements, column_update_fields)

        return row_ids

class DownloadData(HelperFunctions):

    """The UploadData class is the core of the upload process. In this class, there are functions which are used to upload data
        to different tables in the database
    """

    def __init__(self):
        self.engine = dataModel.engine

    def download_info(self, dbTable:str ='', fltr_output = True, fltr = ["_sa_instance_state", "id"], exclude_filter:bool = True, useSubset:bool = False, subset_col:str="", subset:list=[]):
        '''
        General upload function which should be able to download from the database
        Usage: download_info(dbTable = "dataModel.Geos", fltr_output = True, fltr = ["_sa_instance_state"], exclude_filter = True)
        '''

        bulk = BulkUpload(dbTable, self.engine)
        dbTable_evl = eval(dbTable)
        data = pd.DataFrame(bulk.select_table(dbTable_evl, fltr_output = False, useSubset = useSubset, subset_col=subset_col, subset=subset))

        if len(data.columns) > 0 and len(data) > 0:
            if exclude_filter:
                data = data.drop(columns=fltr)
            else:
                data = data[fltr]
        else:
            data = pd.DataFrame()

        return data

class DeleteData(HelperFunctions):

    """The UploadData class is the core of the upload process. In this class, there are functions which are used to upload data
        to different tables in the database

    """

    def __init__(self):
        self.engine = dataModel.engine

    def delete_data_from_table_using_ids(self, dbTable:str, pk_col_of_table:str, lst_of_ids:List):

        """Usage: delete_data_from_table_using_ids(dbTable='dataModel.User', pk_col_of_table = 'dataModel.User.id', lst_of_ids = list(user_ids['id']))
            where user_ids is a dataframe in this instance
        """

        bulk = BulkUpload(dbTable, self.engine)
        bulk.delete_from_table(table = dbTable, pk_col_of_table = pk_col_of_table, lst_of_ids = lst_of_ids)