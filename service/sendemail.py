import yagmail
from settings import auth_email,password_email
yag = yagmail.SMTP(auth_email,password_email)
