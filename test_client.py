#!/usr/bin/env python3
"""
Test script to verify Azure OpenAI client initialization
"""

import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")

print(f"Endpoint: {AOAI_ENDPOINT}")
print(f"Key exists: {bool(AOAI_KEY)}")

try:
    from openai import AzureOpenAI
    
    client = AzureOpenAI(
        api_key=AOAI_KEY,
        azure_endpoint=AOAI_ENDPOINT,
        api_version="2023-05-15"
    )
    
    print("✅ Azure OpenAI client initialized successfully!")
    
    # Test a simple completion
    response = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    
    print("✅ Test completion successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
