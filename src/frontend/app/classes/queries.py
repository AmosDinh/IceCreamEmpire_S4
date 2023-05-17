import psycopg2
import pandas as pd

PGHOST = "postgres-IceCreamEmpire"
PGPORT = "5432"
PGDATABASE = 'IceCreamEmpire'
PGUSER = 'postgres'
PGPASSWORD = '1234'


class Queries:
    def __init__(self)-> None:
        self.conn = psycopg2.connect(host=PGHOST, port=PGPORT, dbname=PGDATABASE, user=PGUSER, password=PGPASSWORD)

    def get_vehicles(self):
        """
        Example Function to execute a sql statement
        """
        sql= """
            SELECT * FROM Vehicles
        """
        return self.sql(sql)
    
    def get_dtypes(self,table_name) -> pd.DataFrame:
        q ="""
               SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public' AND 
            table_name = 'Flavors';
        """ 
        
        return self.sql(q)
       
    def convert_to_numeric(self, col):
        # Check if column is of dtype object
        if col.dtypes == 'object':
            # Try to convert column to numeric
            col = pd.to_numeric(col, errors='ignore')
            # If column is now numeric, check if it can be converted to int
            if pd.api.types.is_numeric_dtype(col):
                if col.eq(col.astype(int)).all():
                    col = col.astype(int)
        return col

    def sql(self, sql: str)-> pd.DataFrame:
        """
        Execute a query and returns a DataFrame
        """
        # Open a cursor to perform database operations
        cursor = self.conn.cursor()
        sql = sql.strip()
        
        # execute the query
        try:
            cursor.execute(sql)
            if sql.lower().startswith("select"):
                columns = list(cursor.description)
                result = cursor.fetchall()
                results = []
                for row in result:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        row_dict[col.name] = row[i]
                    results.append(row_dict)

                df = pd.DataFrame(results)

                # needed so streamlit dataframe editing works correctly
                df = df.convert_dtypes() # for some reason column with 1.12 is not recognized as numeric
                df = df.apply(self.convert_to_numeric, axis=0) # therefore use this
                return df
            else:
                self.conn.commit()
                print("Successfully inserted data")
        except (Exception, psycopg2.DatabaseError) as e:
            cursor.close()
            print(e)
        finally:
            cursor.close()