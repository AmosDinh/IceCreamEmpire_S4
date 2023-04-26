# DBProjectS4


## Development
### Setup (Python 3.10.9)
````
python -m venv venv
````
Activate environment
On windows:
````
venv\bin\activate.bat
````
On Linux:
````
source venv\bin\activate
````

After activation
````
pip install -r requirements.txt

````

Add new package to requirements.txt
````
pip freeze > requirements.txt
````

### Frontend

#### Run streamlit app:
````
streamlit run src/streamlit/app.py
````