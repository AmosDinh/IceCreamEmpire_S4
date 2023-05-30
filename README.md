# IceCreamEmpire 

## Run the application
- Open a cmd in the IceCreamEmpire folder

- Start the application with the command:
    ```
    docker-compose up
    ```

The application is now available via [http://localhost](http://localhost) on HTTP port 80.

- Stop the application with the command:
    ```
    doocker-compose down
    ```

## Navigation
### Backend
- The <strong>Queries</strong> can be found in [queries.sql](src/db/queries.sql)
- To perform <strong>SQL-Statements</strong> the Queries class is used. The source-code can be found in [queries.py](src/frontend/app/classes/queries.py)


### Frontend
The Frontend is implemented using the streamlit framework in Python
- The source-code of the main page can be found in [app.py](/src/frontend/app/app.py)
- The implementation for the CRUD sites can be found in 
[crudorder.py](src/frontend/app/crudorder.py) and [crudtour.py](src/frontend/app/crudtour.py)

### Documentation
- The documentation can be found in [/doc/](/doc/.) folder