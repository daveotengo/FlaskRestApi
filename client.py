import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE+"/helloWorld/tim")

#response = requests.put(BASE+"/video/1", {"name":"tim","likes": 10,"views":20})

#response_patch = requests.patch(BASE+"/video/1", {"name":"tema"})




response_delete = requests.delete(BASE+"/video/1")
#response_get = requests.get(BASE+"/video/2")


response_get = requests.get(BASE+"/video/1")




#response2 = requests.post(BASE+"/helloWorld")

#print(response_patch)

#print(response.json())

print(response_delete)

print(response_get.json())


#print(response2.json())
#source mypython/bin/activate