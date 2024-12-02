from dotenv import load_dotenv
import os
load_dotenv()
seceret_key = os.getenv("SECERET_KEY")
db_url = os.getenv("DB_URL")
auth_email = os.getenv("AUTHOR_EMAIL")
password_email = os.getenv("PASSWORD_EMAIL")
redis_port = os.getenv("REDIS_PORT")
redis_host = os.getenv("REDIS_HOST")
