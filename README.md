# IceCreamEmpire_S4

## Development

### Setup (Python 3.10.9)

```
python -m venv venv
```

Activate environment

On windows:

cmd

```
venv\Scripts\activate.bat  
```

powershell

```
.\.venv\Scripts\Activate.ps1
```

On Linux:

```
source venv/bin/activate
```

After activation

```
pip install -r requirements.txt

```

Add new package to requirements.txt

```
pip freeze > requirements.txt
```

### Frontend

#### Run streamlit app:

```
streamlit run src/frontend/app.py
```
