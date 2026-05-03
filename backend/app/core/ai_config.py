"""
IBM watsonx.ai Configuration Module
Manages API credentials, model configuration, and connection settings
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

# Get the backend directory path (where .env should be)
BACKEND_DIR = Path(__file__).parent.parent.parent
ENV_FILE_PATH = BACKEND_DIR / ".env"


class WatsonxAIConfig(BaseSettings):
    """Configuration for IBM watsonx.ai integration"""
    
    # API Credentials
    watsonx_api_key: str = Field(
        default="",
        description="IBM watsonx.ai API key"
    )
    watsonx_project_id: str = Field(
        default="",
        description="IBM watsonx.ai project ID"
    )
    watsonx_url: str = Field(
        default="https://us-south.ml.cloud.ibm.com",
        description="IBM watsonx.ai API URL"
    )
    
    # Model Configuration
    watsonx_model_id: str = Field(
        default="ibm/granite-13b-chat-v2",
        description="Model ID to use for code analysis"
    )
    
    # Generation Parameters
    max_new_tokens: int = Field(
        default=1024,
        description="Maximum number of tokens to generate"
    )
    min_new_tokens: int = Field(
        default=50,
        description="Minimum number of tokens to generate"
    )
    temperature: float = Field(
        default=0.7,
        description="Sampling temperature (0.0 to 1.0)"
    )
    top_p: float = Field(
        default=0.9,
        description="Nucleus sampling parameter"
    )
    top_k: int = Field(
        default=50,
        description="Top-k sampling parameter"
    )
    repetition_penalty: float = Field(
        default=1.1,
        description="Repetition penalty"
    )
    
    # Retry Configuration
    max_retries: int = Field(
        default=3,
        description="Maximum number of retry attempts"
    )
    retry_delay: float = Field(
        default=1.0,
        description="Delay between retries in seconds"
    )
    
    # Timeout Configuration
    request_timeout: int = Field(
        default=60,
        description="Request timeout in seconds"
    )
    
    # Mock Mode (for testing without real credentials)
    use_mock_responses: bool = Field(
        default=True,
        description="Use mock responses instead of real API calls"
    )
    
    class Config:
        env_file = str(ENV_FILE_PATH)
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def is_configured(self) -> bool:
        """Check if watsonx.ai is properly configured"""
        if self.use_mock_responses:
            return True
        return bool(self.watsonx_api_key and self.watsonx_project_id)
    
    def get_generation_params(self) -> dict:
        """Get generation parameters for watsonx.ai API"""
        return {
            "max_new_tokens": self.max_new_tokens,
            "min_new_tokens": self.min_new_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "repetition_penalty": self.repetition_penalty,
        }


# Global configuration instance
_config: Optional[WatsonxAIConfig] = None


def get_ai_config() -> WatsonxAIConfig:
    """Get or create the AI configuration instance"""
    global _config
    if _config is None:
        _config = WatsonxAIConfig()
    return _config


def reload_ai_config() -> WatsonxAIConfig:
    """Reload the AI configuration from environment"""
    global _config
    _config = WatsonxAIConfig()
    return _config


# Made with Bob