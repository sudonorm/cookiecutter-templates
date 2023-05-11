import pandas as pd
import numpy as np
import sys
sys.path.append("..")
from . import dataModel

from glob import glob

from typing import List, Dict, Union, Tuple

import warnings
warnings.filterwarnings("ignore")

### helper funcs
from .helper_functions import HelperFunctions

## crud
from .crud import BulkUpload

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

    def upload_info_atomic(self, dbTable:str ='', df:pd.DataFrame = pd.DataFrame(), unique_idx_elements:list = [], column_update_fields:list = []):
        '''
        General upload function which should be able to upload anything thrown at it
        Usage: upload_info_atomic(dbTable="dataModel.Geos", df=geos_df, unique_idx_elements=['geo'], column_update_fields=['geo_url'],)

        '''

        for col in unique_idx_elements:
            df = df[~df[col].isna()]
        
        df = df.drop_duplicates(subset=unique_idx_elements).reset_index(drop=True)

        df = self.replace_nan_with_none(df)
        bulk = BulkUpload(dbTable, self.engine)

        bulk.atomic_bulk_upsert(df, unique_idx_elements, column_update_fields )

class DownloadData(HelperFunctions):

    """The UploadData class is the core of the upload process. In this class, there are functions which are used to upload data
        to different tables in the database
    """

    def __init__(self):
        self.engine = dataModel.engine

    def download_info(self, dbTable:str ='', fltr_output = True, fltr = ["_sa_instance_state", "id"], exclude_filter:bool = True):
        '''
        General upload function which should be able to download from the database
        Usage: download_info(dbTable = "dataModel.Geos", fltr_output = True, fltr = ["_sa_instance_state"], exclude_filter = True)
        '''

        bulk = BulkUpload(dbTable, self.engine)
        dbTable_evl = eval(dbTable)
        data = pd.DataFrame(bulk.select_table(dbTable_evl, fltr_output = False))

        if len(data.columns) > 0 and len(data) > 0:
            if exclude_filter:
                data = data.drop(columns=fltr)
            else:
                data = data[fltr]
        else:
            data = pd.DataFrame()

        return data