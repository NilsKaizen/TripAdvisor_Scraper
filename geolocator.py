from geopy.geocoders import Nominatim
import pandas as pd
import sql_administrator as sql

locator = Nominatim(user_agent="myGeocoder")
# location = locator.geocode("Via Leoncino, 29, 37121, Verona Italy")

# print(location.latitude, location.longitude)

# Read the csv with restaurants address
df = pd.read_csv("restaurants-raw-data.csv")

# Backup the csv file
rest_loc = df.copy()
rest_loc = rest_loc[["restaurant_id", "direction"]]

# Create a DF for restaurant ID and coordinates
geo_points = pd.DataFrame(columns=['restaurant_id', 'latitude', 'longitude'])


for i in range(1, rest_loc.shape[0]):
    temp_df = rest_loc.loc[rest_loc["restaurant_id"] == i]
    address = temp_df["direction"].to_string(index=False)
    try:
        loc = locator.geocode(address)
        lat = loc.latitude
        lon = loc.longitude
    except Exception as e:
        lat = 'n_a'
        lon = 'n_a'
        print('ERROR (geolocator): ', str(e))
    print(lat, lon)

    geo_points = geo_points.append({'restaurant_id': int(i), 'latitude': lat,
                                    'longitude': lon}, ignore_index=True)
# Save the coordinates to a csv file
geo_points.to_csv("rest_coordinates.csv", index=False)

# EXECUTE THIS INTO MYSQL

# DROP TABLE IF EXISTS rest_coordinates

# CREATE TABLE IF NOT EXISTS rest_coordinates
# (restaurant_id INT NOT NULL,
#  latitude VARCHAR(255) DEFAULT NULL,
#  longitude VARCHAR(255) DEFAULT NULL)

# SET GLOBAL local_infile = true

# LOAD DATA LOCAL INFILE "C:\\Users\\nils0\\PycharmProjects\\Yelp_Scraping\\rest_coordinates.csv"
# INTO TABLE rest_coordinates
# FIELDS TERMINATED BY ','

# SET GLOBAL local_infile = false
