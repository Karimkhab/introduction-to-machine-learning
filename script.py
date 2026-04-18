from geopy.geocoders import Nominatim

import psycopg2

con = psycopg2.connect(database="demo", user="karimkhabib",
                       password="1234", host="127.0.0.1", port="5432")


cur = con.cursor()
cur.execute('''SELECT * FROM get_coordinates();''')
rows = cur.fetchall()

cur.execute('''CREATE TABLE IF NOT EXISTS Address (address_id VARCHAR(3) PRIMARY KEY, address_text TEXT, address_x FLOAT, address_y FLOAT);''')


geolocator = Nominatim(user_agent="coord_to_real_addr")

for row in rows:
    airport_code, x, y = row
    location = geolocator.reverse(f"{y}, {x}")
    cur.execute(
        "INSERT INTO Address (address_id, address_text, address_x, address_y) VALUES (%s, %s, %s, %s)",
        (airport_code, location.address, x, y)
    )
con.commit()
cur.close()
con.close()


