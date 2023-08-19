import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
import sys
import os
home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)

from glob import glob
from typing import List, Dict, Union, Tuple, Any

import warnings
warnings.filterwarnings("ignore")

### helper funcs
from db.helper_functions import HelperFunctions
from . import dataModel

meta = MetaData()
NUMBER_OF_INSERTS = 9999 # number of inserts should not exceed 9999

class BulkUpload:

    """This class is a collection of methods designed to make database operations easier and faster. 
    """
    
    def __init__(self, dbTable:str, engine:Any):

        """dbTable is the name of the Table class e.g., dataModel.Store
        """

        self.dbTableStr = dbTable
        self.dbTable = eval(dbTable)
        self.engine = engine
        self.pk = self.get_primary_key(self.dbTable)
        self.number_of_inserts = NUMBER_OF_INSERTS 

    def get_primary_key(self, model_instance):
        model_columns = model_instance.__mapper__.columns
        return [c.description for c in model_columns if c.primary_key][0]

    def create_string(self, tup:tuple, sep="||"):
        strng = ""
        for i in range(len(tup)):
            if i == 0:
                strng = tup[i]
            else:
                strng = f'{strng}{sep}{tup[i]}'
        return strng

    def get_or_none(self, df:pd.DataFrame, cols_dict:dict, create_pk:bool = True, df_to_use:str = "df") -> Union[int, None]:
        
        strng = ""
        quote = "'"
        df_in, df_out = pd.DataFrame(), pd.DataFrame()

        if create_pk:
            col_to_use = self.pk
        else:
            col_to_use = f'{self.pk}{"_tmp"}'

        # df_to_use = "df"
        oString = ",".join(x for x in [f'{df_to_use}{"["}{quote}{ky}{quote}{"]"}' for ky in list(cols_dict.keys())])

        tuple_string = f'{"tuple(zip("}{oString}{"))"}'

        df["match_str"] = [self.create_string(x) for x in eval(tuple_string)]

        table_data = pd.DataFrame(self.select_table(self.dbTable, fltr_output = True))

        if len(table_data) != 0:
            df_to_use = "table_data"
            oString = ",".join(x for x in [f'{df_to_use}{"["}{quote}{ky}{quote}{"]"}' for ky in list(cols_dict.keys())])
            tuple_string = f'{"tuple(zip("}{oString}{"))"}'

            table_data["match_str"] = [self.create_string(x) for x in eval(tuple_string)]

            table_data_dict = dict(zip(table_data["match_str"], table_data[self.pk]))

            df_in = df[df["match_str"].isin(list(table_data["match_str"].unique()))]
            df_in[col_to_use] = [table_data_dict[x] for x in list(df_in["match_str"])]

            df_out = df[~df["match_str"].isin(list(table_data["match_str"].unique()))]
        else:
            df_out = df.copy()


        df_out[col_to_use] = None
        
        return pd.concat([df_in, df_out]).reset_index(drop=True)

    def chunked(self, it:Union[List, Tuple], n:int) -> Dict:
        """This function was lifted verbatim from peewee. It's used to chunk up a large dataset into n-sized chunks

        Args:
            it (Union[List, Tuple]): an iterable such as a list or tuple which contains the records to be batched
            n (int): the batch size to use for chunking

        Returns:
            Dict: a dictionary of records

        Yields:
            Iterator[Dict]: a list containing a dictionary of n-sized records
        """

        import itertools
        marker = object()
        for group in (list(g) for g in itertools.zip_longest(*[iter(it)] * n,
                                                    fillvalue=marker)):
            if group[-1] is marker:
                del group[group.index(marker):]
            yield group
    
    def get_maximum_row_id(self) -> int:
        """
        This function is used to return the maximum row used in a primary key column of a Table.
        It will only work if the primary key column is numeric

        Returns:
            int: the maximum row in the primary key (pk) column or 0
        """
        
        tbl = str(self.dbTable)
        tbl = tbl.split(".")[-1].replace(">", "").replace("'", "")
        tbl = f'{"dataModel."}{tbl}'

        with self.engine.connect() as connection:
            result = connection.execute(select(func.max(eval(f'{tbl}{"."}{self.pk}'))))
            for res in result:
                max_row_id = res[0]

        if max_row_id is None:
            return 0
        else:
            return max_row_id

    def upsert(self, df:pd.DataFrame, create_pk:bool = True) -> None:
        """
        The upsert function helps us to update or insert data in bulk. It works by taking a dataframe containing 
        data to be uploaded and splitting this into two dataframes: new and update
        It determines what is new and what should be updated by checking is the primary key column is empty
        The primary key column needs to have been added in the dataframe prior to passing it to this function
        For details on how to add the primary key column, see the upsert_table() function

        Args:
            df (pd.DataFrame): dataframe containing data to be uploaded
            create_pk (bool, optional): option to create the primary key or not. This is important because we have tables
            with static IDs which we do not want to autoincrement. By setting this to False, the primary key column is not created rather the 
            one present in the dataframe is used. Defaults to True.
        """

        dfCopy = df.copy()
        
        if create_pk:
            new = dfCopy[dfCopy[self.pk].isna()].drop(columns=[self.pk])
        else:
            new = dfCopy[dfCopy[f'{self.pk}{"_tmp"}'].isna()].drop(columns=[f'{self.pk}{"_tmp"}'])
            if len(new) > 0:
                new = new.sort_values(by=[self.pk], ascending=True).reset_index(drop=True)
                try:
                    new[self.pk] = new[self.pk].map(int)
                except:
                    pass
                if new.loc[0][self.pk] == 0:
                    new[self.pk] = new[self.pk] + 1

        if create_pk:
            
            max_row = self.get_maximum_row_id()

            print("max row is...", max_row)
            if max_row == 0:
                id_list = list(np.arange(1, len(new)+1))
            else:
                max_row = max_row+1
                id_list = list(np.arange(max_row, max_row+len(new)))

            assert len(new) == len(id_list)
            new[self.pk] = id_list

        if create_pk:
            update = dfCopy[~dfCopy[self.pk].isna()].drop_duplicates(subset=[self.pk]).reset_index(drop=True)
        else:
            update = dfCopy[~dfCopy[f'{self.pk}{"_tmp"}'].isna()].drop_duplicates(subset=[f'{self.pk}{"_tmp"}']).drop(columns=[f'{self.pk}{"_tmp"}']).reset_index(drop=True)

        print("new")
        print(new.head(5))

        print("update")
        print(update.head(5))

        if len(update) > 0:
            try:
                update[self.pk] = update[self.pk].map(int)
            except:
                pass
        
        ## bulk insert new records
        if len(new) > 0:
            new = [u for u in new.to_dict("records")]
            with Session(self.engine) as session, session.begin():
                for batch in self.chunked(new, self.number_of_inserts):
                    print(f'{"Insert for batch of "}{len(batch)}{" is being worked on"}')
                    session.bulk_insert_mappings(
                            self.dbTable,
                            batch
                        )
        
        ## bulk update new records
        if len(update) > 0:     
            update = [u for u in update.to_dict("records")]
            with Session(self.engine) as session, session.begin():
                for batch in self.chunked(update, self.number_of_inserts):
                    print(f'{"Update for batch of "}{len(batch)}{" is being worked on"}')
                    session.bulk_update_mappings(
                            self.dbTable,
                            batch
                        )
    
    def upsert_table(self, dbTable:object, df:pd.DataFrame, cols_dict={}, create_pk:bool=True) -> None:
        """
        The upsert_table function helps us to update or insert data to a table. it uses the upsert() funtion to achieve this.
        Args:
            dbTable (object): the table we want to push data to. This can be passed in as eval(tableName) to convert it into an object e.g., eval("dataModel.categories")
            df (pd.DataFrame): the dataframw which contains data to be updated or inserted
            depth (int): this indicates how many columns from the table we want to use as a KEY to check if the data already exists. Maximum allowed is currently 4.
            dbColX (str): this indicates a column in the DB which should be used as a KEY column for checks. It can be passed in as dataModel.Categories.categoryType_id or as eval("dataModel.Categories.categoryType_id")
            dfColX (str): this indicates a column in the inout dataframe which should be used as a KEY column for checks. The data in this should match dbColX
            create_pk (bool, optional): option to create the primary key or not. This is important because we have tables
            with static IDs which we do not want to autoincrement. By setting this to False, the primary key column is not created rather the 
            one present in the dataframe is used. Defaults to True.
        """
        df = self.get_or_none(df = df.copy(), cols_dict=cols_dict, create_pk = create_pk)
        self.upsert(df, create_pk=create_pk)

    def atomic_bulk_upsert(self, data:pd.DataFrame, unique_idx_elements:list, column_update_fields:list) -> List[int]:
        """Bulk upsert records using the sqlite_upsert method. This method has also been tested to work with not just SQLite but also postgresSQL

        Args:
            dbTable (str): a string representation of the Table to be worked on in the form dataModel.testTable
            data (pd.DataFrame): dataframe containing the data to be uploaded. Column names must match column names in the DB
            unique_idx_elements (list): a list of columns which should be searched for, which when considered together are unique. Can also be one unique field. 
            A sequence consisting of string column names, _schema.Column objects, or other column expression objects that will be used to infer a target index or unique constraint.
            column_update_fields (list): a list of the columns to be updated. 
        """
        dbTable = self.dbTableStr
        records = [u for u in data.to_dict("records")]
        dbTable_eval = eval(dbTable)
        dbTable_eval_id = eval(f'{self.dbTableStr}{".id"}')

        # column_update_fields = list(set(column_update_fields).difference(unique_idx_elements))

        with Session(dataModel.engine) as session, session.begin():
            for batch in self.chunked(records, self.number_of_inserts):
                print(f'{"Insert or update for batch of "}{len(batch)}{" is being worked on"}')
                stmt = sqlite_upsert(dbTable_eval).values(batch)
                column_dict_fields = {column.name:column for column in stmt.excluded._all_columns if column.name in column_update_fields}
                # stmt = stmt.on_conflict_do_update(index_elements=[eval(f'{dbTable}{"."}{x}') for x in unique_idx_elements], set_=column_dict_fields)
                # stmt = stmt.on_conflict_do_update(index_elements=[x.name for x in eval(f'{dbTable}{".__table_args__"}') if x.__visit_name__ in ['unique_constraint']], set_=column_dict_fields)
                stmt = stmt.on_conflict_do_update(index_elements=unique_idx_elements, set_=column_dict_fields)

                result = session.scalars(stmt.returning(dbTable_eval_id))
                row_ids = result.all()

                session.execute(stmt)

                return row_ids

    def select_table(self, dbTable:object, fltr_output:bool = False, fltr:List = ["_sa_instance_state"], useSubset:bool = False, subset_col:str="", subset:list=[]) -> List:
        """
        This function is used to select everything or a filtered output from a Table in the database.

        Args:
            dbTable (object): this refers to a Table class e.g., dataModel.Store
            fltr_output (bool, optional): this indicates if we want the output of the select statement to be filtered or not. Defaults to False.
            fltr (List, optional): whatever is put into this list as an argument will be removed from the results. Defaults to ["_sa_instance_state"].
            subset_col (str): column whcih serves as limiter (only entries matching subset will be returned)
            subset (list): subset of entries to select from subset_col

        Returns:
            List: a list of records from a Table in the database
        """

        subset = subset + [str(x) for x in subset]
        
        with Session(self.engine) as session:

            # elements = [object_as_dict(u) for u in session.query(self.dbTable).all()] # another method that can be used to return a dictionary
            if useSubset:
                elements = [dict(u.__dict__) for u in session.query(dbTable).filter(getattr(dbTable, subset_col).in_(subset)).all()]
            else:
                elements = [dict(u.__dict__) for u in session.query(dbTable).all()]

            if fltr_output:
                elements = [{key : val for key, val in sub.items() if key not in fltr} for sub in elements]
            else:
                elements = [{key : val for key, val in sub.items()} for sub in elements]
        return elements

    def delete_from_table(self, table:str, pk_col_of_table:str, lst_of_ids:List)  -> None:
        """
        This function can be used to delete rows from a database. It works by deleting the rows using the primary key

        Args:
            table (str): the table we want to delete from. This should be passed in as a string. We use eval() to convert it into an object
            pk_col_of_table (str): this should be the primary key column e.g., "dataModel.Categories.id"
            lst_of_ids (List): this should be the list of primary keys to be dropped
        """

        table = eval(table)
        pk_col_of_table = eval(pk_col_of_table)
        with Session(self.engine) as session, session.begin():
            stmt = table.__table__.delete().where(
                pk_col_of_table.in_(lst_of_ids)
            )
            session.execute(stmt)

    def update_table(self, table:str, pk_col_of_table:str, lst_of_ids:List, valuesDict:Dict) -> None:
        """
        This function can be used to update rows in a database. It works by targeting the rows using the primary key
        and updating them using the valuesDict, which should contain records

        Args:
            table (str): the table we want to update. This should be passed in as a string. We use eval() to convert it into an object
            pk_col_of_table (str): this should be the primary key column e.g., "dataModel.Categories.id"
            lst_of_ids (List): this should be the list of primary keys to be updated
            valuesDict (Dict): this should be a dictionary of records which should match the columns of the table
        """

        table = eval(table)
        pk_col_of_table = eval(pk_col_of_table)
        with Session(self.engine) as session, session.begin():
            stmt = table.__table__.update().where(
                pk_col_of_table.in_(lst_of_ids)
            ).values(valuesDict)
            session.execute(stmt)