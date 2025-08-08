# MELISSA FAVELLI
# CSD310 DATABASE USE & DEVELOPMENT
# 8/7/25
# ASSIGNMENT 7.2


""" import statements """
import mysql.connector
from mysql.connector import errorcode
import dotenv
from dotenv import dotenv_values


secrets = dotenv_values(".env")

""" database config object """

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

try:
    """ try/catch block for handling potential MySQL database errors """
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    
    print("Welcome to the Movies Database!")
    print("=" * 50)

    print("\n-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT studio_id, studio_name FROM studio")
    studios = cursor.fetchall()
    
    for studio in studios:
        print(f"Studio ID: {studio[0]}")
        print(f"Studio Name: {studio[1]}")
        print()

    print("-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    genres = cursor.fetchall()
    
    for genre in genres:
        print(f"Genre ID: {genre[0]}")
        print(f"Genre Name: {genre[1]}")
        print()
    
    print("-- DISPLAYING Short Film RECORDS --")
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120") # more than 2 hours
    short_films = cursor.fetchall()
    
    for film in short_films:
        print(f"Film Name: {film[0]}")
        print(f"Runtime: {film[1]}")
        print()
    
    print("-- DISPLAYING Director RECORDS in Order --")
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")
    films_by_director = cursor.fetchall()
    
    for film in films_by_director:
        print(f"Film Name: {film[0]}")
        print(f"Director: {film[1]}")
        print()

except mysql.connector.Error as err:
    """ on error code """
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)

finally:
    """ close the connection to MySQL """
    if 'db' in locals():
        db.close()
        print("\nConnection closed.")