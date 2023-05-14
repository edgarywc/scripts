import sys, base64

print("ORIGEM: " + sys.argv[1])
print("DESTINO: " + sys.argv[2])

file = open(sys.argv[1],"rb")
data_binary = file.read()
b64data = (base64.b64encode(data_binary)).decode('ascii')


with open(sys.argv[2],"wb") as b64File:
  b64File.write(b64data.encode('ascii'))

