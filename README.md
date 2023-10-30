### Software requisites:
- pyenv
- python 3.12.0

### To set up app:
- Download git repo and navigate inside
- Run `pyenv local 3.12.0` to set python
- Run `pyenv exec python -m venv .venv` to create virtual environment
- To activate the virtual environment, run `source venv/bin/activate` for MacOS/Linux or `venv\Scripts\activate` for Windows
- Run `pip install -r requirements.txt` to install Flask and other requirements
- Create a PostgreSQL database and replace the embedded url in line 19 of ./src/app.py to your new database or use the one I created: `connection = psycopg2.connect('<url>')`

### To run server:
- `flask run`

### Sending requests:
- `GET http://127.0.0.1:5000/acronym`
- `POST http://127.0.0.1:5000/acronym` with JSON body: `{"acronym": "GL", "definition": "Good luck"}` inserts a new acronym "GL" with definition "Good luck" in the PostgreSQL database.
- `PATCH http://127.0.0.1:5000/acronym/<id>` with the target int id at the end, with JSON body: `{"definition": "hello"}` will change the definition of the id's corresponding acronym to "hello"
- `DELETE /acronym/<id>` with the target int id at the end will delete the acronym entry of that id from the table.