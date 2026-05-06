#!/usr/bin/env python3
"""Comprehensive API Test for CertifyMe Backend"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("=" * 70)
print("CertifyMe Backend API Test Suite")
print("=" * 70)

# Test 1: Signup
print("\n✓ Test 1: Admin Signup")
print("-" * 70)
signup_payload = {
    "username": "Admin User",
    "email": "admin@test.com",
    "password": "AdminPass@123456"
}
try:
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_payload, timeout=5)
    print(f"Status: {response.status_code} - {response.json()['message']}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Login
print("\n✓ Test 2: Admin Login")
print("-" * 70)
login_payload = {
    "email": "admin@test.com",
    "password": "AdminPass@123456"
}
try:
    response = requests.post(f"{BASE_URL}/auth/login", json=login_payload, timeout=5)
    token = response.json().get('access_token')
    print(f"Status: {response.status_code} - Login Successful")
    print(f"Token: {token[:50]}...")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Add Opportunity
print("\n✓ Test 3: Add Opportunity")
print("-" * 70)
headers = {"Authorization": f"Bearer {token}"}
opp_payload = {
    "title": "Software Developer Position",
    "description": "We are looking for a skilled software developer with Python expertise."
}
try:
    response = requests.post(f"{BASE_URL}/opportunities", json=opp_payload, headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        opp_data = response.json()
        opp_id = opp_data.get('id')
        print(f"Opportunity Created: {opp_data.get('message')}")
        print(f"Opportunity ID: {opp_id}")
except Exception as e:
    print(f"Error: {e}")

# Test 4: Get All Opportunities
print("\n✓ Test 4: Get All Opportunities")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/opportunities", headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    opportunities = response.json()
    print(f"Found {len(opportunities)} opportunity/opportunities")
    for opp in opportunities:
        print(f"  - {opp['title']} (ID: {opp['id']})")
except Exception as e:
    print(f"Error: {e}")

# Test 5: Update Opportunity
print("\n✓ Test 5: Update Opportunity")
print("-" * 70)
if opp_id:
    update_payload = {
        "title": "Senior Software Developer Position",
        "description": "Updated: We are looking for a senior software developer with 5+ years Python expertise."
    }
    try:
        response = requests.put(f"{BASE_URL}/opportunities/{opp_id}", json=update_payload, headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

# Test 6: Get Opportunity Details
print("\n✓ Test 6: Get Opportunity Details")
print("-" * 70)
if opp_id:
    try:
        response = requests.get(f"{BASE_URL}/opportunities/{opp_id}", headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        opp = response.json()
        print(f"Title: {opp['title']}")
        print(f"Description: {opp['description'][:50]}...")
    except Exception as e:
        print(f"Error: {e}")

# Test 7: Delete Opportunity
print("\n✓ Test 7: Delete Opportunity")
print("-" * 70)
if opp_id:
    try:
        response = requests.delete(f"{BASE_URL}/opportunities/{opp_id}", headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "=" * 70)
print("API Test Suite Completed!")
print("=" * 70)
