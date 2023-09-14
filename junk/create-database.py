import sqlite3

# Create a new SQLite3 database or connect to an existing one
conn = sqlite3.connect("image_classification.db")
cursor = conn.cursor()

# Create the Images table
cursor.execute('''
  CREATE TABLE IF NOT EXISTS Images (
  ImageID INTEGER PRIMARY KEY AUTOINCREMENT,
  ImageName TEXT NOT NULL,
  ImageFile TEXT NOT NULL,
  UploadDate DATETIME NOT NULL
  )
''')

# Create the Classes table
cursor.execute('''
  CREATE TABLE IF NOT EXISTS Classes (
  ClassID INTEGER PRIMARY KEY AUTOINCREMENT,
  ClassName TEXT NOT NULL
  )
''')

# Create the Detections table
cursor.execute('''
  CREATE TABLE IF NOT EXISTS Detections (
  DetectionID INTEGER PRIMARY KEY AUTOINCREMENT,
  ImageID INTEGER NOT NULL,
  ClassID INTEGER NOT NULL,
  Confidence REAL NOT NULL,
  Location TEXT NOT NULL,
  FOREIGN KEY (ImageID) REFERENCES Images (ImageID),
  FOREIGN KEY (ClassID) REFERENCES Classes (ClassID)
  )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup completed.")
