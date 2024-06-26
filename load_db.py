import csv
import os
import sqlite3
import sys

def create_db():
	# Define the SQL script to create the database schema
	create_table_sql = """
	CREATE TABLE IF NOT EXISTS access (
		uid TEXT,
		has_Access INTEGER NOT NULL,
		is_inside INTEGER NOT NULL
	);

	CREATE TABLE IF NOT EXISTS accessLog (
		uid TEXT NOT NULL,
		is_inside INTEGER NOT NULL,
		timestamp DATETIME NOT NULL
	);
	"""

	# Connect to the SQLite database (this will create the database file if it doesn't exist)
	conn = sqlite3.connect('RIR.db')

	# Create a cursor object using the cursor() method
	cursor = conn.cursor()

	# Execute the SQL script
	cursor.executescript(create_table_sql)

	# Commit the changes and close the connection
	conn.commit()
	conn.close()

	print("Database and tables created successfully.")

def load_db(csv_file_path):
	# Connect to the SQLite database
	conn = sqlite3.connect('RIR.db')
	cursor = conn.cursor()

	# Open the CSV file
	with open(csv_file_path, newline='') as csvfile:
		csvreader = csv.reader(csvfile)
		
		# Skip the header row
		next(csvreader)
		
		# Iterate over the rows in the CSV file
		for row in csvreader:
			uid = row[0]
			print (uid)
			uid = uid[:2] + ':' + uid[2:]
			uid = uid[:5] + ':' + uid[5:]
			uid = uid[:8] + ':' + uid[8:]
			print (uid)

			# Insert the data into the access table
			cursor.execute("""
			INSERT INTO access (uid, has_Access, is_inside) 
			VALUES (?, 1, 0)
			""", (uid,))

	# Commit the transaction
	conn.commit()

	# Close the connection
	conn.close()

	print("CSV data loaded into the access table successfully.")

if __name__=='__main__':
	if(not os.path.exists('RIR.db')):
		create_db()
	load_db(sys.argv[1])

