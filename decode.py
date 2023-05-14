import sys, base64

print("ORIGEM: " + sys.argv[1])
print("DESTINO: " + sys.argv[2])

file = open(sys.argv[1],"rb")
data_ascii = file.read()
b64decoded = (base64.b64decode(data_ascii))

#print(b64data)
with open(sys.argv[2],"wb") as b64File:
  b64File.write(b64decoded)

