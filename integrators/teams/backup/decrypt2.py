from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import HMAC, SHA256
from Crypto.Util.Padding import unpad
import base64

# Replace these variables with your actual data and keys
encrypted_symmetric_key = "JoewPt4wtpewHnT2DeEmWW37IKNg+cYprMKwpyzPS5HwncOKV4wL9pYiNxGMJXTm4KBYFzhjzNGZHxpDzYPbZr87WmGCN2KiFhh+/+CukGCZFT8TXlNLKJc2xHwkkzkMh7Izblsk2F9PJWl6wHNIsGxEKvV3RNIcv/xDsAof7uIdVcBZEMnldOiDB6O3/qW9DCVUKkH3VfCURymxpy8KsFCor/1yAE0OLHe0pAr0hDoLIQqNSxmE/kVgBLYhGPFpq9nnyDSC8sjlC+RcJ0Pc6W8TAczMVviFlgyOMWVhtxTqE1pizWTj8cpLkwzAlFRd8rnnBAI52r55+Tu9tZBpLkqhZ7cwirJMcZSj6WiTt7loCSPejx9t+IV+xCSCnTwN/x5Tt7iDJ0oa7ScMegx/CWpq6XWRtUC1ZdMnDYRG1I90CWQS2YL9FXlQGgtNqYg7PKBa32phpSzzR2vNnxO5zZKbz/aHVZan+sCqXAzjGUD4z9ufs31UqkTxEjDzgksh/tVE5Z9HzhTxRQditFKiNjEN4Qeaqhtz1Yz8GAAAAAAA_8jfAn_F5QKsq8M9yie2mBwDiCXJ_prOST6K0k5P70wweAAAAAAEMAADiCXJ_prOST6K0k5P70wweAAAE_WKMAAA="
data_signature = "/qqHNVxlayl8dsqGABVNMweeAKA4pOWuot05I6RYoCbQn5xCsNdtyu82B8CmHfaDRUWlVuj3Th0WKAnLiFXINFQwuMQguSmDTH6ABnLxBqMg8o/uS82RTFQKwoIC2yM3fu5nzanvoV85uM844c9XOuZuoeYidCi7EpI+okDYHizGlspOgj4m1X9mSinGDuyV9qhDumAW+GLw+dpRhO2HGTszIX7cahtTrq1AD0R4Um3QSUk97f7mdnoss9x8xh/iKlP3hoSoDDUlRTEZOlgoSp7RM6gslDvyNtTF31oLHLcyjsPnJmbeK1fUD7Y7IxXMCxbloYeG/HCVE/bktybkdrfF6Gtucmyno/OESKelD/UT+tLb9gDPiavl0ZP2RN3a/Gyre/2fU//pXdWXawZH6YZc9kb7O9rX+/GJ0n2dl6K7oE3fUioWUie4q4KYkC9gGOcXxZNKRlguSAyhrMxlXNgFeOUM4Sfdrr6O3QwGwsp475K84ZvajQNTvtTAYKcT"


private_key_file = 'private_key.pem'
# Read the private key from the file
with open(private_key_file, 'r') as file:
    private_key = file.read()

# Step 1: Decrypt the symmetric key
rsa_key = RSA.import_key(private_key)
cipher_rsa = PKCS1_OAEP.new(rsa_key)
decrypted_symmetric_key = cipher_rsa.decrypt(base64.b64decode(encrypted_symmetric_key))

# # Step 2: Verify data integrity using HMAC-SHA256
# hmac = HMAC.new(decrypted_symmetric_key, digestmod=SHA256)
# hmac.update(base64.b64decode(encrypted_data))
# try:
#     hmac.verify(base64.b64decode(data_signature))
#     print("Data integrity verified.")
# except ValueError:
#     print("Data integrity verification failed.")
#     exit()

# Step 3: Decrypt the resource data content
cipher_aes = AES.new(decrypted_symmetric_key, AES.MODE_CBC, iv=decrypted_symmetric_key[:16])
decrypted_data = unpad(cipher_aes.decrypt(base64.b64decode(encrypted_data)), AES.block_size)

# Convert decrypted data to string (assuming it's UTF-8 encoded)
decrypted_string = decrypted_data.decode('utf-8')
print("Decrypted Resource Data:", decrypted_string)
