#!/usr/bin/env python3
"""
CertifyMe Backend API Test Script
Comprehensive testing without Postman/Thunder Client
"""

import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:5000"
TOKEN = None
TEST_EMAIL = None

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{bcolors.HEADER}{bcolors.BOLD}{'='*60}{bcolors.ENDC}")
    print(f"{bcolors.HEADER}{bcolors.BOLD}{text}{bcolors.ENDC}")
    print(f"{bcolors.HEADER}{bcolors.BOLD}{'='*60}{bcolors.ENDC}\n")

def print_success(text):
    print(f"{bcolors.OKGREEN}✓ {text}{bcolors.ENDC}")

def print_error(text):
    print(f"{bcolors.FAIL}✗ {text}{bcolors.ENDC}")

def print_info(text):
    print(f"{bcolors.OKCYAN}ℹ {text}{bcolors.ENDC}")

def print_response(response, title="Response"):
    print(f"\n{bcolors.BOLD}{title}:{bcolors.ENDC}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_signup():
    """Test: Admin Signup"""
    global TEST_EMAIL
    print_header("1. TESTING SIGNUP")
    
    TEST_EMAIL = f"testadmin+{uuid.uuid4().hex[:8]}@certify.com"
    payload = {
        "username": "Test Admin",
        "email": TEST_EMAIL,
        "password": "TestPass@123456"
    }
    
    print_info(f"Signing up with email: {payload['email']}")
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=payload)
        print_response(response)
        
        if response.status_code == 201:
            print_success("Signup successful!")
            return True
        else:
            print_error("Signup failed!")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_login():
    """Test: Admin Login"""
    global TOKEN, TEST_EMAIL
    print_header("2. TESTING LOGIN")
    
    if not TEST_EMAIL:
        print_error("No test email available. Run signup first.")
        return False
    
    payload = {
        "email": TEST_EMAIL,
        "password": "TestPass@123456"
    }
    
    print_info(f"Logging in with email: {payload['email']}")
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            TOKEN = data.get('access_token')
            print_success(f"Login successful!")
            print_info(f"Token: {TOKEN[:50]}...")
            return True
        else:
            print_error("Login failed!")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_add_opportunity():
    """Test: Add Opportunity"""
    global TOKEN
    
    if not TOKEN:
        print_error("No token available. Run login test first.")
        return False
    
    print_header("3. TESTING ADD OPPORTUNITY")
    
    payload = {
        "title": "Full Stack Web Development",
        "description": "Learn HTML, CSS, JavaScript, React, Node.js, and MongoDB. Build real-world projects and become a professional full-stack developer."
    }
    
    print_info(f"Adding opportunity: {payload['title']}")
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/opportunities", json=payload, headers=headers)
        print_response(response)
        
        if response.status_code == 201:
            data = response.json()
            opp_id = data.get('id')
            print_success(f"Opportunity added successfully! ID: {opp_id}")
            return opp_id
        else:
            print_error("Failed to add opportunity!")
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_get_opportunities():
    """Test: Get All Opportunities"""
    global TOKEN
    
    if not TOKEN:
        print_error("No token available. Run login test first.")
        return False
    
    print_header("4. TESTING GET ALL OPPORTUNITIES")
    
    print_info("Fetching all opportunities...")
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/opportunities", headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Retrieved {len(data)} opportunity(ies)")
            return data
        else:
            print_error("Failed to retrieve opportunities!")
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_get_opportunity_details(opp_id):
    """Test: Get Single Opportunity Details"""
    global TOKEN
    
    if not TOKEN:
        print_error("No token available. Run login test first.")
        return False
    
    print_header(f"5. TESTING GET OPPORTUNITY DETAILS (ID: {opp_id})")
    
    print_info(f"Fetching opportunity with ID: {opp_id}")
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/opportunities/{opp_id}", headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            print_success("Opportunity details retrieved successfully!")
            return response.json()
        else:
            print_error("Failed to retrieve opportunity details!")
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_update_opportunity(opp_id):
    """Test: Update Opportunity"""
    global TOKEN
    
    if not TOKEN:
        print_error("No token available. Run login test first.")
        return False
    
    print_header(f"6. TESTING UPDATE OPPORTUNITY (ID: {opp_id})")
    
    payload = {
        "title": "Advanced Full Stack Web Development",
        "description": "Master full-stack development with advanced patterns, microservices, Docker, and deployment strategies."
    }
    
    print_info(f"Updating opportunity with ID: {opp_id}")
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/opportunities/{opp_id}", json=payload, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            print_success("Opportunity updated successfully!")
            return True
        else:
            print_error("Failed to update opportunity!")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_delete_opportunity(opp_id):
    """Test: Delete Opportunity"""
    global TOKEN
    
    if not TOKEN:
        print_error("No token available. Run login test first.")
        return False
    
    print_header(f"7. TESTING DELETE OPPORTUNITY (ID: {opp_id})")
    
    print_info(f"Deleting opportunity with ID: {opp_id}")
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.delete(f"{BASE_URL}/opportunities/{opp_id}", headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            print_success("Opportunity deleted successfully!")
            return True
        else:
            print_error("Failed to delete opportunity!")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_forgot_password():
    """Test: Forgot Password"""
    print_header("8. TESTING FORGOT PASSWORD")
    
    payload = {
        "email": "testadmin@certify.com"
    }
    
    print_info(f"Requesting password reset for: {payload['email']}")
    
    try:
        response = requests.post(f"{BASE_URL}/auth/forgot-password", json=payload)
        print_response(response)
        
        if response.status_code == 200:
            print_success("Password reset token generated!")
            return response.json().get('reset_token')
        else:
            print_error("Failed to generate reset token!")
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def run_full_test():
    """Run complete API test workflow"""
    print(f"\n{bcolors.BOLD}{bcolors.OKBLUE}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║         CertifyMe Backend API Test Suite              ║")
    print("║              Testing All Endpoints                    ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{bcolors.ENDC}")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info("Make sure the Flask backend is running!")
    
    # Step 1: Signup
    if not test_signup():
        print_error("Signup test failed. Stopping.")
        return
    
    # Step 2: Login
    if not test_login():
        print_error("Login test failed. Stopping.")
        return
    
    # Step 3: Add Opportunity
    opp_id = test_add_opportunity()
    if not opp_id:
        print_error("Add opportunity test failed. Stopping.")
        return
    
    # Step 4: Get All Opportunities
    if not test_get_opportunities():
        print_error("Get opportunities test failed. Stopping.")
        return
    
    # Step 5: Get Single Opportunity
    if not test_get_opportunity_details(opp_id):
        print_error("Get opportunity details test failed.")
    
    # Step 6: Update Opportunity
    if not test_update_opportunity(opp_id):
        print_error("Update opportunity test failed.")
    
    # Step 7: Delete Opportunity
    if not test_delete_opportunity(opp_id):
        print_error("Delete opportunity test failed.")
    
    # Step 8: Forgot Password
    reset_token = test_forgot_password()
    
    # Summary
    print_header("TEST SUMMARY")
    print_success("All API tests completed!")
    print_info("Check results above for any failures")
    print_info("Frontend in Test1/sky/ is connected to this backend")

if __name__ == "__main__":
    run_full_test()