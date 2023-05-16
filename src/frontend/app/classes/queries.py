import psycopg2
from pandas import DataFrame

PGHOST = 'localhost'
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
    
    
    def sql(self, sql: str)-> DataFrame:
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
                return DataFrame(results)
            else:
                self.conn.commit()
                print("Successfully inserted data")
        except (Exception, psycopg2.DatabaseError) as e:
            cursor.close()
            print(e)
        finally:
            cursor.close()