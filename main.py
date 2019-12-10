from get_countries_data import *


region = get_all_regions()
given_region = 'africa'
given_country = 'Angola'
#Get country by region given region and country to get your languaje
country = get_country_by_region(region[region.index(given_region)], given_country)
language = str(country.get('languages')[0].get('name')).encode("utf-8")

#Time start process
startTime = time.perf_counter()

#Calculate ms on time end process
data = [[region[region.index('africa')], country.get('name'), hashlib.sha1(language), '{:.2f}'.format((time.perf_counter() - startTime) * 1000)]]

#Create DataFrame
df = pd.DataFrame(data, columns = ['Region', ' City Name', 'Languaje', 'Time'])

#Calculate Basic statistics
total_time = df['Time'].sum()
max_time = df.max()
min_time = df.min()
avg_time = df['Time'].mean()

#SQLITE connection
connection = sqlite3.connect("RESULTS_db.sqlite")
connection.row_factory = json_factory
 
cursor = connection.cursor()
#Create and insert dataResults
try:
	cursor.execute('CREATE TABLE results (total_time VARCHAR, avg_time VARCHAR, min_time VARCHAR, max_time VARCHAR)')
	connection.commit()

except OperationalError:
    print "SQLite DB exist"

cursor.execute('INSERT INTO results (total_time, avg_time, min_time, max_time) values (?, ?, ?, ?)', (str(total_time), str(avg_time), str(min_time), str(max_time)))
cursor.execute("select * from results")
 
results = cursor.fetchall()

#Create JSON file
with open('data.json', 'w') as outfile:
	json.dump(results, outfile)
 
connection.close()

#Invoke mongoDB to insert statistics dataResults
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["resultsdb"]
results_db = db["results"]

results_data = [
  { "total_time": str(total_time) , "avg_time": str(avg_time), "min_time": str(min_time) , "max_time": str(max_time) }
]

x = results_db.insert_many(results_data)

for x in results_db.find():
	print(x)