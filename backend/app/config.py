import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Keys validated upon initialization
    LLAMA_CLOUD_API_KEY: str
    GEMINI_API_KEY: str
    
    # Paths with fallback defaults
    INPUT_DIR: str = "backend/data/input_pdfs"
    OUTPUT_DIR: str = "backend/data/extracted_images"

    # Match system to look for .env file in the root
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        extra="ignore"
    )

# Instantiate settings for global app use
settings = Settings()

if __name__ == "__main__":
    print("Environment variables loaded successfully!")
    print(f"Input Directory configured to: {settings.INPUT_DIR}")