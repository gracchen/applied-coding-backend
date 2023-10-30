import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_TABLE = ("CREATE TABLE IF NOT EXISTS acronyms (_id SERIAL PRIMARY KEY, acronym TEXT, definition TEXT);")

INSERT_ACRONYM = ("INSERT INTO acronyms (acronym, definition) VALUES (%s, %s) RETURNING _id;")

GET_ACRONYMS = ("SELECT acronym FROM acronyms;")

UPDATE_ACRONYM_DEFINITION = ("UPDATE acronym SET definition = %s WHERE _id = %d;")

DELETE_ACRONYM = ("DELETE FROM acronym WHERE _id = %d;")

load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)
url = os.environ.get("DATABASE_URL")  # gets variables from environment
connection = psycopg2.connect('postgres://vcpmwfhh:e6hP1zQ_mA4ion--13Icdj1LAp6cjP-T@isabelle.db.elephantsql.com/vcpmwfhh')

# GET /acronym
@app.get("/acronym")
def get_acronym():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ACRONYMS)
            acronyms = [row[0] for row in cursor.fetchall()]  # Extract acronyms from the query result
    return {"": acronyms} #send the list as string

# POST /acronym
@app.post("/acronym")
def create_acronym():
    data = request.get_json() # python dict of sent data
    acronym = data["acronym"]
    definition = data["definition"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE) #in case table not yet created
            cursor.execute(INSERT_ACRONYM, (acronym, definition)) #pass in tuple
            id = cursor.fetchone()[0] # get id of current row
    return {"id": id, "message": f"Acronym {acronym} with definition {definition} created."}, 201 #201 status = created

# PATCH /acronym/:acronymID
@app.patch("/acronym/<int:acronymID>")
def update_acronym(acronymID):
    data = request.get_json() 
    new_definition = data["definition"]
    if new_definition is None:
        return {"message": "Please provide a new definition for the acronym."}, 400

    with connection:
        with connection.cursor() as cursor:
            # Check if the acronymID exists
            cursor.execute("SELECT acronym FROM acronyms WHERE _id = %s", (acronymID,))
            existing_acronym = cursor.fetchone()
            if existing_acronym is None:
                return {"message": "Acronym not found."}, 404
            # Update the definition
            cursor.execute("UPDATE acronyms SET definition = %s WHERE _id = %s", (new_definition, acronymID))
    return {"message": f"Acronym with ID {acronymID} updated to {new_definition}."}

# DELETE /acronym/:acronymID
@app.delete("/acronym/<int:acronymID>")
def delete_acronym(acronymID):
    with connection:
        with connection.cursor() as cursor:
            # Check if the acronymID exists
            cursor.execute("SELECT acronym FROM acronyms WHERE _id = %s", (acronymID,))
            existing_acronym = cursor.fetchone()
            if existing_acronym is None:
                return {"message": "Acronym not found."}, 404
            cursor.execute("DELETE FROM acronyms WHERE _id = %s", (acronymID,))
    return {"message": f"Acronym with ID {acronymID} deleted."}
