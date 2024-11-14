from dotenv import load_dotenv
import os
load_dotenv()
seceret_key = os.getenv("SECERET_KEY")
db_url = os.getenv("DB_URL")