import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import decimal

PGHOST = "postgres-IceCreamEmpire"
if os.path.exists('amoshost.json'):
    PGHOST = open('amoshost.json').read().strip()

PGPORT = "5432"
PGDATABASE = 'IceCreamEmpire'
PGUSER = 'postgres'
PGPASSWORD = '1234'


class Queries:
    def __init__(self) -> None:
        conn_string = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
        self.engine: Engine = create_engine(conn_string)

    def get_vehicles(self) -> pd.DataFrame:
        """
        Example Function to execute a SQL statement
        """
        sql = """
            SELECT * FROM Vehicles
        """
        return self.sql(sql)

    def get_dtypes(self, table_name: str) -> pd.DataFrame:
        q = """
               SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public' AND 
            table_name = :table_name;
        """
        return self.sql(q, params={"table_name": table_name})


    def sql(self, sql: str, params: dict = None) -> pd.DataFrame:
        """
        Execute a query and returns a DataFrame
        """
        if params is None:
            params = {}

        stmt = text(sql.strip())

        with self.engine.connect() as connection:
            try:
                result = connection.execute(stmt, **params)
                if result.returns_rows:
                    r = result.fetchall()
                    for i in range(len(r)):
                        r[i] = [v if type(v) != decimal.Decimal else round(float(v),2) for v in r[i]]
                    df = pd.DataFrame(r, columns=result.keys())

                    # needed so streamlit dataframe editing works correctly
                    #df = df.convert_dtypes()  # for some reason column with 1.12 is not recognized as numeric
                    #df = df.apply(self.convert_to_numeric, axis=0)  # therefore use this
                    return df
                else:
                    connection.commit()
                    print("Successfully inserted data")
            except Exception as e:
                connection.rollback()
                print(e)

    def get_relation(self, relation_name):
        primary_keys = {
            'IceCreamVendors': ['vendor_id'],
            'Neighborhoods': ['Neighborhood_id'],
            'Vehicles': ['vehicle_id'],
            'Tours': ['tours_id'],
            'Flavors': ['flavor_id'],
            'Contents': ['flavor_id'],
            'Orders': ['order_id'],
            'OrderDetails': ['order_id', 'flavor_id'],
            'Warehouses': ['warehouse_id'],
            'WarehouseStoresFlavors': ['warehouse_id', 'flavor_id'],
            'VehicleStoresFlavors': ['vehicle_id', 'flavor_id']
        }
        primary_keys = {k.lower(): v for k, v in primary_keys.items()}
        non_changable = primary_keys[relation_name.lower()] # for the streamlit df editor
        query = f"SELECT * FROM {relation_name}"
        df = self.sql(query)

        for col in non_changable:
            assert col in df.columns, f"Column {col} not in {relation_name}"
        
        return df, non_changable
    

    