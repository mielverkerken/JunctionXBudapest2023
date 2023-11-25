import json
import hashlib, hmac
from base64 import b64decode, b64encode
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

encrypted_symmetric_key = "JoewPt4wtpewHnT2DeEmWW37IKNg+cYprMKwpyzPS5HwncOKV4wL9pYiNxGMJXTm4KBYFzhjzNGZHxpDzYPbZr87WmGCN2KiFhh+/+CukGCZFT8TXlNLKJc2xHwkkzkMh7Izblsk2F9PJWl6wHNIsGxEKvV3RNIcv/xDsAof7uIdVcBZEMnldOiDB6O3/qW9DCVUKkH3VfCURymxpy8KsFCor/1yAE0OLHe0pAr0hDoLIQqNSxmE/kVgBLYhGPFpq9nnyDSC8sjlC+RcJ0Pc6W8TAczMVviFlgyOMWVhtxTqE1pizWTj8cpLkwzAlFRd8rnnBAI52r55+Tu9tZBpLkqhZ7cwirJMcZSj6WiTt7loCSPejx9t+IV+xCSCnTwN/x5Tt7iDJ0oa7ScMegx/CWpq6XWRtUC1ZdMnDYRG1I90CWQS2YL9FXlQGgtNqYg7PKBa32phpSzzR2vNnxO5zZKbz/aHVZan+sCqXAzjGUD4z9ufs31UqkTxEjDzgksh/tVE5Z9HzhTxRQditFKiNjEN4Qeaqhtz1Yz8GAAAAAAA_8jfAn_F5QKsq8M9yie2mBwDiCXJ_prOST6K0k5P70wweAAAAAAEMAADiCXJ_prOST6K0k5P70wweAAAE_WKMAAA="
encrypted_payload = "/qqHNVxlayl8dsqGABVNMweeAKA4pOWuot05I6RYoCbQn5xCsNdtyu82B8CmHfaDRUWlVuj3Th0WKAnLiFXINFQwuMQguSmDTH6ABn+xBqMg8o/uS82RTFQKwoIC2yM3fu5nzanvoV85uM844c9XOuZuoeYidCi7EpI+okDYHizGlspOgj4m1X9mSinGDuyV9qhDumAW+GLw+dpRhO2HGTszIX7cahtTrq1AD0R4Um3QSUk97f7mdnoss9x8xh/iKlP3hoSoDDUlRTEZOlgoSp7RM6gslDvyNtTF31oLHLcyjsPnJmbeK1fUD7Y7IxXMCxbloYeG/HCVE/bktybkdrfF6Gtucmyno/OESKelD/UT+tLb9gDPiavl0ZP2RN3a/Gyre/2fU//pXdWXawZH6YZc9kb7O9rX+/GJ0n2dl6K7oE3fUioWUie4q4KYkC9gGOcXxZNKRlguSAyhrMxlXNgFeOUM4Sfdrr6O3QwGwsp475K84ZvajQNTvtTAYKcT"
data_signature = "/qqHNVxlayl8dsqGABVNMweeAKA4pOWuot05I6RYoCbQn5xCsNdtyu82B8CmHfaDRUWlVuj3Th0WKAnLiFXINFQwuMQguSmDTH6ABnLxBqMg8o/uS82RTFQKwoIC2yM3fu5nzanvoV85uM844c9XOuZuoeYidCi7EpI+okDYHizGlspOgj4m1X9mSinGDuyV9qhDumAW+GLw+dpRhO2HGTszIX7cahtTrq1AD0R4Um3QSUk97f7mdnoss9x8xh/iKlP3hoSoDDUlRTEZOlgoSp7RM6gslDvyNtTF31oLHLcyjsPnJmbeK1fUD7Y7IxXMCxbloYeG/HCVE/bktybkdrfF6Gtucmyno/OESKelD/UT+tLb9gDPiavl0ZP2RN3a/Gyre/2fU//pXdWXawZH6YZc9kb7O9rX+/GJ0n2dl6K7oE3fUioWUie4q4KYkC9gGOcXxZNKRlguSAyhrMxlXNgFeOUM4Sfdrr6O3QwGwsp475K84ZvajQNTvtTAYKcT"

encrypted_symmetric_key: bytes = b64decode(encrypted_symmetric_key.encode())
encrypted_payload = b64decode(encrypted_payload.encode())


private_key_file = 'private_key.pem'
with open(private_key_file, 'r') as file:
    private_key = file.read()
rsa_key = RSA.import_key(private_key)
cipher = PKCS1_OAEP.new(rsa_key)
# if length of encrypted_symmetric_key is > 128 we will get ciphertext with incorrect length, to avoid that lets split and decrypt in chunks
default_length = 128
length = len(encrypted_symmetric_key)
if length < default_length:
    decrypt_byte = cipher.decrypt(encrypted_symmetric_key)
else:
    offset = 0
    res = []
    while length - offset > 0:
        if length - offset > default_length:
            res.append(cipher.decrypt(encrypted_symmetric_key[offset:offset + default_length]))
        else:
           res.append(cipher.decrypt(encrypted_symmetric_key[offset:]))
        offset += default_length
    decrypt_byte = b''.join(res)
decrypted_symmetric_key = decrypt_byte

hash_state_machine = hmac.new(decrypted_symmetric_key, msg=encrypted_payload, digestmod=hashlib.sha256)
raw_signature = hash_state_machine.digest()

actual_signature_bytes: bytes = b64encode(raw_signature)
actual_signature: str = actual_signature_bytes.decode()

if actual_signature != expected_data_signature:
   raise Exception("data hash is not as expected")

iv = decrypted_symmetric_key[:16]
cipher2 = AES.new(decrypted_symmetric_key, AES.MODE_CBC, iv=iv)

message_str = unpad(cipher2.decrypt(encrypted_payload), block_size=16).decode()
message_dict = json.loads(message_str)
