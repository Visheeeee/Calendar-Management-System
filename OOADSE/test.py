import json
f=open("events.json","r+")
j=json.loads(f.read())
new={"title":"holiday","start":"2020-05-01","end":"2020-05-02"}
f.seek(0)
f.truncate()
j.append(new)
print(j)
json.dump(j,f)

