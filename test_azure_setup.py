#!/usr/bin/env python3
"""
Simple test script to verify Azure OpenAI setup.
Run this to check if your Azure OpenAI configuration is working.
"""

import os
from pydantic import BaseModel
from cheat_at_search.agent.enrich import create_cached_enricher


class TestResponse(BaseModel):
    message: str
    status: str


def test_azure_setup():
    """Test that the Azure OpenAI setup is working."""
    print("Testing Azure OpenAI setup...")
    
    # Check environment variables
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print(f"Azure endpoint: {'✓' if azure_endpoint else '✗'}")
    print(f"Azure API key: {'✓' if azure_api_key else '✗'}")
    print(f"OpenAI API key: {'✓' if openai_key else '✗'}")
    
    if azure_endpoint and azure_api_key:
        print("Using Azure OpenAI")
    elif openai_key:
        print("Using OpenAI")
    else:
        print("No API keys found. Please set either Azure or OpenAI credentials.")
        return False
    
    # Test enricher creation
    try:
        enricher = create_cached_enricher(
            cls=TestResponse,
            system_prompt="You are a helpful assistant. Respond with a simple test message.",
            model="gpt-4o-mini"  # Change this to your Azure deployment name if using Azure
        )
        print("✓ Enricher created successfully")
        
        # Test a simple enrichment
        result = enricher.enrich("Say hello")
        print(f"✓ Test enrichment successful: {result}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing enricher: {e}")
        return False


if __name__ == "__main__":
    success = test_azure_setup()
    exit(0 if success else 1) 