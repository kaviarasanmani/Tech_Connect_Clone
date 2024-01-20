import sqlite3

DATABASE_FILE = "/home/pr1/Desktop/Working/TechConnect/products.db"  # Replace with your actual SQLite database file path

def create_banner_images_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BannerImages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image TEXT NOT NULL,
            status INTEGER DEFAULT 1
        )
    ''')

    conn.commit()
    conn.close()

# Call the function to create the table
create_banner_images_table()
