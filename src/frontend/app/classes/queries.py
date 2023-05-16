import psycopg2

PGHOST = 'localhost'
PGPORT = "5432"
PGDATABASE = 'IceCreamEmpire'
PGUSER = 'postgres'
PGPASSWORD = '1234'


class Queries:
    def __init__(self)-> None:
        self.conn = psycopg2.connect(host=PGHOST, port=PGPORT, dbname=PGDATABASE, user=PGUSER, password=PGPASSWORD)
        

    def get_users(self):
        """
        Example Function to execute a sql statement
        """
        sql= """
            SELECT * FROM Student
        """
        return self.__execute_sql(sql)
    
    def __execute_sql(self, sql: str):
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)