import psycopg2
connect = psycopg2.connect("dbname='ridemyway' host='localhost' user='dario' password='riot'")
curs = connect.cursor()

def createall_tables():
    commands=(
        """
        CREATE TABLE IF NOT EXISTS new_user(
            id SERIAL PRIMARY KEY NOT NULL,
            email VARCHAR NOT NULL,
            username VARCHAR(10) NOT NULL,
            password VARCHAR NOT NULL
            )
        """,
        """
        CREATE TABLE IF NOT EXISTS ride(
            r_id SERIAL PRIMARY KEY NOT NULL,
            car_license VARCHAR(10) NOT NULL,
            title VARCHAR(20) NOT NULL,
            ride_date VARCHAR(10) NOT NULL,
            distance INT NOT NULL,
            num_seats INT NOT NULL,
            start_time VARCHAR(10) NOT NULL,
            arrival_time VARCHAR(10) NOT NULL,
            ride_price INT NOT NULL,
            creator VARCHAR(20) NOT NULL
            )
        """,
        """
        CREATE TABLE IF NOT EXISTS requestss(
            req_id SERIAL PRIMARY KEY NOT NULL,
            ride_id INT NOT NULL REFERENCES ride(r_id),
            car_license VARCHAR(10) NOT NULL,
            requester_name VARCHAR(20) NOT NULL,
            ride_date VARCHAR(10) NOT NULL,
            title VARCHAR(20) NOT NULL,
            num_seats INT NOT NULL,
            ride_price INT NOT NULL,
            creator VARCHAR(20) NOT NULL,
            action VARCHAR(10)
            )
        """
    )

    for db_table in commands:
        curs.execute(db_table)
    
    curs.close()
    connect.commit()
    connect.close()

createall_tables()
