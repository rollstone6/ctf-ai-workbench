"""Known-answer RSA/AES checks; use check-sage.sh for algebra tooling."""
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from sympy import factorint
p,q,e,message=101,103,7,1234
n=p*q
assert factorint(n)=={101:1,103:1}
d=pow(e,-1,(p-1)*(q-1))
assert pow(pow(message,e,n),d,n)==message
key=bytes(range(16))
plain=b'offline crypto fixture'
cipher=AES.new(key,AES.MODE_CBC,iv=bytes(16)).encrypt(pad(plain,16))
assert unpad(AES.new(key,AES.MODE_CBC,iv=bytes(16)).decrypt(cipher),16)==plain
print('Crypto Python 自检通过：整数分解、RSA 往返及 AES-CBC 往返。')
