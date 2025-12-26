from dotenv import load_dotenv
import os

my_secrets = {}

load_dotenv()
my_secrets["x_bearer_token"] = os.getenv("X_BEARER_TOKEN")
my_secrets["x_consumer_key"] = os.getenv("X_CONSUMER_KEY")
my_secrets["x_consumer_secret"] = os.getenv("X_CONSUMER_SECRET")
my_secrets["x_access_token"] = os.getenv("X_ACCESS_TOKEN")
my_secrets["x_access_token_secret"] = os.getenv("X_ACCESS_TOKEN_SECRET")

# print("X_CONSUMER_KEY: ", x_consumer_key)
# print("X_CONSUMER_SECRET: ", x_consumer_secret)
my_secrets["logfile"] = os.getenv("LOGFILE")
