#!/usr/bin/env python3
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

# Test 1: Signup
print("Testing Signup...")
payload = {
    "username": "TestAdmin",
    "email": "testadmin@test.com",
    "password": "TestPass@123456"
}

try:
    response = requests.post(f"{BASE_URL}/auth/signup", json=payload, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Login
print("\nTesting Login...")
login_payload = {
    "email": "testadmin@test.com",
    "password": "TestPass@123456"
}

try:
    response = requests.post(f"{BASE_URL}/auth/login", json=login_payload, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
