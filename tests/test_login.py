#!/usr/bin/env python3
"""
Teste Simples de Login
"""

import requests
import json

def test_login():
    url = "http://localhost:8001/api/v1/auth/login"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Token: {result.get('access_token', 'N/A')[:50]}...")
            return result.get('access_token')
        else:
            return None
            
    except Exception as e:
        print(f"Erro: {e}")
        return None

if __name__ == "__main__":
    token = test_login()
    if token:
        print("✅ Login bem-sucedido!")
    else:
        print("❌ Login falhou!")
