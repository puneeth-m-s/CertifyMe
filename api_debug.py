import requests
BASE='http://127.0.0.1:5000'

print('Logging in...')
r = requests.post(BASE + '/auth/login', json={'email':'testadmin@certify.com','password':'TestPass@123456'})
print(r.status_code)
print(r.text)
if r.ok:
    token = r.json().get('access_token')
    print('Token:', token[:60])
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    r2 = requests.post(BASE + '/opportunities', json={'title':'Test','description':'Desc'}, headers=headers)
    print('Add status', r2.status_code)
    print(r2.text)
else:
    print('Login failed')
