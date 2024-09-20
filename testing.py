import requests as req



#Authenticate
data = {
	'username':'test',
	'password':'test'
	}
url = 'http://0.0.0.0:5200/api/authenticate'

r = req.post(url,data=data)
token = r.json().get('access_token')
headers = {'Authorization':"Bearer "+token}


#Add_note
url = 'http://0.0.0.0:5200/api/notes/new'
r = req.post(url,data={'name':'som3not3','content':'аблака'}, headers=headers)
print(r.text)

#Get_my_notes
url = 'http://0.0.0.0:5200/api/notes'
r = req.get(url,headers=headers)
print(r.text)

#Get_a_specific_note
url = 'http://0.0.0.0:5200/api/notes/1'
r = req.get(url,headers=headers)
print(r.text)