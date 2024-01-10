import sqlite3

with sqlite3.connect('artists.db') as connection:
    # create a connection to the database
    sql = connection.cursor()

    # execute sql command to create the table
    sql.execute(
        'create table if not exists band (name text, genre text, members integer);')

    # example of inserting data
    sql.execute(
        'insert into band (name, genre, members) values ("band 1", "rock", 3)')
    # and
    # sql.execute(
    #    'insert into band (name, genre, members) values ("Coldplay", "rock-pop", 5)')

    # example of adding data to the table using user input
    name = input('enter the band name: ')
    genre = input('enter the band genre: ')
    member_count = int(input('number of band members: '))

    sql.execute('insert into band (name, genre, members) values (?, ?, ?)',
                (name, genre, member_count))

    # saving data in the database
    connection.commit()

    # display records in the console
    bands = sql.execute('select * from band;')
    for band in bands:
        print(band)
