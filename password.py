# from documentation in 
# https://docs.python.org/3/library/hashlib.html#key-derivation
# an example for creating a login system
# in this example, the hash cannot be decrypted
# but you can input the same password and get the same 
# hash back.
# For encrypting/decrypting see Fernet


from hashlib import pbkdf2_hmac
import os
import time

start_time = time.time()

PASSWORD = 'hello world'

# use a randomly generated salts 
salt = os.urandom(20)
print(type(salt))
iters = 4000000
dk = pbkdf2_hmac('sha256', bytes(PASSWORD ,'UTF8') , salt, iters)
what = dk.hex()
print(what)

# used to calculate time to compute, for security should be greater than 241ms
print("--- %s seconds ---" % (time.time() - start_time))

# Comparing with a different password
# Same salt or different salt for testing

PASSWORD2 = 'hello world'
# salt2 = os.urandom(20)
dk2 = pbkdf2_hmac('sha256', bytes(PASSWORD2 ,'UTF8') , salt, iters)
what2 = dk2.hex()
print(what2)

print(what == what2)