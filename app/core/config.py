# app/core/config.py
import os
from dotenv import load_dotenv
from google.cloud import secretmanager
from google.api_core import exceptions

# --- Load local environment variables from .env file for development ---
# This line looks for a .env file in the root directory of the project
load_dotenv()

# --- Core Settings ---
# Fetch the Google Cloud Project ID from an environment variable.
# This makes the code portable, as you can set this variable differently
# in production vs. local environments.
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "gen-lang-client-0073667672")
# We also specify the location for Vertex AI, as it's required.
GCP_LOCATION = "us-central1"

# --- Secret Loading Function ---
def get_secret(secret_id: str, project_id: str, version: str = "latest") -> str:
    """
    Retrieves a secret from Google Cloud Secret Manager.
    If it fails (e.g., in local development without gcloud auth),
    it gracefully falls back to loading from local environment variables.
    """
    try:
        # First, attempt to use the professional, secure method.
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except (exceptions.NotFound, exceptions.PermissionDenied, Exception) as e:
        # If Secret Manager access fails, fall back to the local .env file.
        # This is perfect for local development.
        print(f"--- INFO: Could not access secret '{secret_id}' from Secret Manager. "
              f"Falling back to local .env file. (Error: {e.__class__.__name__})")
        secret = os.getenv(secret_id)
        if not secret:
            # If it's not in the .env file either, the app can't run securely.
            raise ValueError(f"CRITICAL: Secret '{secret_id}' not found in Secret Manager or local .env file.")
        return secret

# --- Load all critical settings and secrets on application startup ---
# This makes them available as simple variables to other parts of the app.
try:
    print(">>> Loading application configuration...")

    # Load from Secret Manager, with .env as fallback
    JWT_SECRET_KEY = get_secret("JWT_SECRET_KEY", GCP_PROJECT_ID)
    GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY", GCP_PROJECT_ID)

    # General API settings
    API_V1_STR: str = "/api/v1"

    print(">>> Configuration and secrets loaded successfully.")

except ValueError as e:
    print(f"!!! FATAL ERROR: {e}")
    # Exit or raise the exception to prevent the app from starting in an insecure state
    raise