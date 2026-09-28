
import sys
from pathlib import Path

# Menambahkan root project (folder AI-agent-linux) ke sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import connect_db

connection = connect_db.connect_to_db()
cursor = connection.cursor()

cursor.execute("SELECT current_user, current_database();")
result = cursor.fetchone()

print("Connected as:", result[0])
print("Database:", result[1])

cursor.close()
connection.close()