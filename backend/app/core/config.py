# app/core/config.py
import os
from dotenv import load_dotenv
from google.cloud import secretmanager
from google.api_core import exceptions

# --- Load local environment variables from .env file for development ---
load_dotenv()

# --- Core Settings ---
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id-here")
GCP_LOCATION = "us-central1"

# --- Secret Loading Function ---
def get_secret(secret_id: str, project_id: str, version: str = "latest") -> str:
    """
    Retrieves a secret from Google Cloud Secret Manager.
    Falls back to loading from local environment variables for development.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except (exceptions.NotFound, exceptions.PermissionDenied, Exception) as e:
        print(f"--- INFO: Could not access secret '{secret_id}' from Secret Manager. "
              f"Falling back to local .env file. (Error: {e.__class__.__name__})")
        secret = os.getenv(secret_id)
        if not secret:
            raise ValueError(f"CRITICAL: Secret '{secret_id}' not found in Secret Manager or local .env file.")
        return secret

# --- Load all critical settings and secrets on application startup ---
try:
    print(">>> Loading application configuration...")

    # Load from Secret Manager, with .env as fallback
    JWT_SECRET_KEY = get_secret("SECRET_KEY", GCP_PROJECT_ID)
    GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY", GCP_PROJECT_ID)
    DATABASE_URL = get_secret("DATABASE_URL", GCP_PROJECT_ID)


    # --- General API & Token Settings ---
    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM = "HS256"

    print(">>> Configuration and secrets loaded successfully.")

except ValueError as e:
    print(f"!!! FATAL ERROR: {e}")
    raise