import os

# ______
# |  ____|
# | |__   _ ____   __
# |  __| | '_ \ \ / /
# | |____| | | \ V /
# |______|_| |_|\_/
IS_DEV = False

# _____        _        _
# |  __ \      | |      | |
# | |  | | __ _| |_ __ _| |__   __ _ ___  ___  ___
# | |  | |/ _` | __/ _` | '_ \ / _` / __|/ _ \/ __|
# | |__| | (_| | || (_| | |_) | (_| \__ \  __/\__ \
# |_____/ \__,_|\__\__,_|_.__/ \__,_|___/\___||___/
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "")
MONGODB_HOST = os.getenv("MONGODB_HOST", "")
MONGODB_PORT = os.getenv("MONGODB_PORT", 27017)
MONGODB_USER = os.getenv("MONGODB_USER", "")
MONGODB_PASS = os.getenv("MONGODB_PASS", "")

#   _____
#  / ____|
# | (___  _ __   __ _  ___ ___  ___
#  \___ \| '_ \ / _` |/ __/ _ \/ __|
#  ____) | |_) | (_| | (_|  __/\__ \
# |_____/| .__/ \__,_|\___\___||___/
#        | |
#        |_|
UPLOAD_PATH = "/tmp/videos/"
SPACES_ACCESS_KEY_ID = os.getenv("SPACES_ACCESS_KEY_ID")
SPACES_SECRET_ACCESS_KEY = os.getenv("SPACES_SECRET_ACCESS_KEY")
SPACES_REGION_NAME = os.getenv("SPACES_REGION_NAME")
SPACES_BUCKET_NAME = os.getenv("SPACES_BUCKET_NAME")
SPACES_URL = f"https://{SPACES_REGION_NAME}.digitaloceanspaces.com"
