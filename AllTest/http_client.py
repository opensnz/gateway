import requests

resp = requests.post("http://localhost:8080/post-test", json={'type':'JoinRequest'})

print(resp.json())