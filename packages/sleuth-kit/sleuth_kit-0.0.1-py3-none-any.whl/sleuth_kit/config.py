from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

class Config:
    TRANSPOSE_API_KEY = os.getenv('TRANSPOSE_API_KEY')
    SAVE_AS_CSV = os.getenv('SAVE_AS_CSV', 'True').lower() in ['true', '1']
    SAVE_AS_SQLITE = os.getenv('SAVE_AS_SQLITE', 'True').lower() in ['true', '1']
    UPLOAD_TO_XATA = os.getenv('UPLOAD_TO_XATA', 'False').lower() in ['true', '1']

def save_api_key(key_name, value):
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    with open(env_path, 'a') as f:
        f.write(f"\n{key_name}={value}")
    os.environ[key_name] = value
    load_dotenv()