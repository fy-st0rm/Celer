import random
import string

# Functions to encrypt and decrypt the string


"""
def generate_key():
	key = Fernet.generate_key()
	return key


def encrypt(string, key):
	fernet = Fernet(key)

	enc_str = fernet.encrypt(string.encode())
	return enc_str.decode()


def decrypt(string, key):
	fernet = Fernet(key)

	dec_str = fernet.decrypt(string.encode()).decode()
	return dec_str
"""


def generate_key():
	key = ''.join(random.choices(string.digits, k=5))
	return key


def encrypt(string, key):
	enc_str = ""
	new_key = 0
	key = int(key)

	while key > 0:
		r = key % 10
		new_key += r
		key = int(key / 10)

	for i in string:
		enc_str += chr(ord(i) + new_key)
	
	return enc_str


def decrypt(string, key):
	dec_str = ""
	new_key = 0
	key = int(key)
	
	while key > 0:
		r = key % 10
		new_key += r
		key = int(key / 10)

	for i in string:
		dec_str += chr(ord(i) - new_key)
	
	return dec_str

"""
def encrypt(string, key):
	enc_str = ""
	key_index = 0

	for i in string:
		enc_str += chr(ord(i) - (int(key[key_index])))
		
		key_index += 1
		if key_index >= 5:
			key_index = 0

	return enc_str


def decrypt(string, key):
	dec_str = ""
	key_index = 0

	for i in string:
		dec_str += chr(ord(i) + (int(key[key_index])))
		
		key_index += 1
		if key_index >= 5:
			key_index = 0

	return dec_str
"""
"""
test = "[slok]: helo\n[slok]: hey"
key = generate_key()
print("key:", key)
enc = encrypt(test, key)
print("enc:", enc)
dec = decrypt(enc, key)
print("dec:", dec)

print(len(enc))
print(len(dec))
"""

