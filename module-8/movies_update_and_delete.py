# MELISSA FAVELLI
# 8/8/2025
# ASSIGNMENT 8.2
# MOVIES_UPDATE_AND_DELETE

import mysql.connector
from mysql.connector import errorcode
import dotenv
from dotenv import dotenv_values

# Load environment variables
secrets = dotenv_values(".env")

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

def show_films(cursor, title):

    
    # Inner join query
    cursor.execute("""SELECT film_name as Name, 
                            film_director as Director, 
                            genre_name as Genre, 
                            studio_name as 'Studio Name' 
                     FROM film 
                     INNER JOIN genre ON film.genre_id=genre.genre_id 
                     INNER JOIN studio ON film.studio_id=studio.studio_id""")
    
    # Get the results from the cursor object
    films = cursor.fetchall()
    
    # Format the output label
    print("\n-- {} --".format(title))
    
    # Iterate over the film data set and display the results
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name: {}\nStudio Name: {}\n".format(
            film[0], film[1], film[2], film[3]))

try:
    
    # Connect to the database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    
    # Display initial films
    show_films(cursor, "DISPLAYING FILMS")
    
    # Insert a new film record
    # Using Universal Pictures (studio_id = 3) and SciFi genre (genre_id = 2)
    insert_query = """INSERT INTO film (film_name, film_releaseDate, film_runtime, 
                      film_director, studio_id, genre_id) 
                      VALUES (%s, %s, %s, %s, %s, %s)"""
    
    film_data = ("Avatar", "2009", 162, "James Cameron", 3, 2)
    cursor.execute(insert_query, film_data)
    db.commit() # commit update
    
    # Display films after insert
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")
    
    # Update Alien to Horror genre (genre_id = 1 is Horror)
    update_query = "UPDATE film SET genre_id = 1 WHERE film_name = 'Alien'"
    cursor.execute(update_query)
    db.commit()  # Commit update
    
    # Display films after update
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")
    
    # Delete Gladiator
    delete_query = "DELETE FROM film WHERE film_name = 'Gladiator'"
    cursor.execute(delete_query)
    db.commit()  # Commit delete
    
    # Display films after delete
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")
    
    print("Database operations completed successfully!")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print("Database error: {}".format(err))

finally:
    if 'db' in locals():
        db.close()
        print("Database connection closed.")