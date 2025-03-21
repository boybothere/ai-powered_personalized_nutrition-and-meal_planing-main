import os
from google.cloud import vision

def set_gcp_credentials():
    """Set Google Cloud credentials from the service account JSON file."""
    
    # Set the path to your service account key JSON file
    key_path = os.path.join(
        os.path.dirname(__file__), 
        "engaged-symbol-454322-r2-e8bdee8629a6.json"
    )
    
    # Set the environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
