import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import b64decode
import ast

data = """{'value': [{'subscriptionId': '58fd0b47-30a4-4169-9517-d12c87905bbf', 'subscriptionExpirationDateTime': '2023-11-25T18:38:58.388138+00:00', 'changeType': 'created', 'resource': "Users('099ba34e-ce8b-4660-84de-7911e9c3a4ef')/messages('AAMkAGMxZTY4NGExLTdiMTctNGJiMy1hOGJiLTU1ODFiMDAzNDk2ZQBGAAAAAAA_8jfAn_F5QKsq8M9yie2mBwDiCXJ_prOST6K0k5P70wweAAAAAAEMAADiCXJ_prOST6K0k5P70wweAAAE_WKMAAA=')", 'clientState': 'secretclientState', 'tenantId': 'ada817f9-c174-4a32-aeb7-712fe13090da', 'encryptedContent': {'data': '/qqHNVxlayl8dsqGABVNMweeAKA4pOWuot05I6RYoCbQn5xCsNdtyu82B8CmHfaDRUWlVuj3Th0WKAnLiFXINFQwuMQguSmDTH6ABn+xBqMg8o/uS82RTFQKwoIC2yM3fu5nzanvoV85uM844c9XOuZuoeYidCi7EpI+okDYHizGlspOgj4m1X9mSinGDuyV9qhDumAW+GLw+dpRhO2HGTszIX7cahtTrq1AD0R4Um3QSUk97f7mdnoss9x8xh/iKlP3hoSoDDUlRTEZOlgoSp7RM6gslDvyNtTF31oLHLcyjsPnJmbeK1fUD7Y7IxXMCxbloYeG/HCVE/bktybkdrfF6Gtucmyno/OESKelD/UT+tLb9gDPiavl0ZP2RN3a/Gyre/2fU//pXdWXawZH6YZc9kb7O9rX+/GJ0n2dl6K7oE3fUioWUie4q4KYkC9gGOcXxZNKRlguSAyhrMxlXNgFeOUM4Sfdrr6O3QwGwsp475K84ZvajQNTvtTAYKcT', 'dataKey': 'JoewPt4wtpewHnT2DeEmWW37IKNg+cYprMKwpyzPS5HwncOKV4wL9pYiNxGMJXTm4KBYFzhjzNGZHxpDzYPbZr87WmGCN2KiFhh+/+CukGCZFT8TXlNLKJc2xHwkkzkMh7Izblsk2F9PJWl6wHNIsGxEKvV3RNIcv/xDsAof7uIdVcBZEMnldOiDB6O3/qW9DCVUKkH3VfCURymxpy8KsFCor/1yAE0OLHe0pAr0hDoLIQqNSxmE/kVgBLYhGPFpq9nnyDSC8sjlC+RcJ0Pc6W8TAczMVviFlgyOMWVhtxTqE1pizWTj8cpLkwzAlFRd8rnnBAI52r55+Tu9tZBpLkqhZ7cwirJMcZSj6WiTt7loCSPejx9t+IV+xCSCnTwN/x5Tt7iDJ0oa7ScMegx/CWpq6XWRtUC1ZdMnDYRG1I90CWQS2YL9FXlQGgtNqYg7PKBa32phpSzzR2vNnxO5zZKbz/aHVZan+sCqXAzjGUD4z9ufs31UqkTxEjDzgksh/tVE5Z9HzhTxRQditFKiNjEN4Qeaqhtz1Yz8GAAAAAAA_8jfAn_F5QKsq8M9yie2mBwDiCXJ_prOST6K0k5P70wweAAAAAAEMAADiCXJ_prOST6K0k5P70wweAAAE_WKMAAA='}}], 'validationTokens': ['eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlQxU3QtZExUdnlXUmd4Ql82NzZ1OGtyWFMtSSIsImtpZCI6IlQxU3QtZExUdnlXUmd4Ql82NzZ1OGtyWFMtSSJ9.eyJhdWQiOiJhYWU4NmEzMS1iZTY4LTRkZmEtYjJkNy01MDhiYWI2ODYwOWUiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9hZGE4MTdmOS1jMTc0LTRhMzItYWViNy03MTJmZTEzMDkwZGEvIiwiaWF0IjoxNzAwOTMwMjczLCJuYmYiOjE3MDA5MzAyNzMsImV4cCI6MTcwMTAxNjk3MywiYWlvIjoiRTJWZ1lHalZibnJ5Sy9GeWVpQzd3ZjJPQmZOVUFRPT0iLCJhcHBpZCI6IjBiZjMwZjNiLTRhNTItNDhkZi05YTgyLTIzNDkxMGM0YTA4NiIsImFwcGlkYWNyIjoiMiIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0L2FkYTgxN2Y5LWMxNzQtNGEzMi1hZWI3LTcxMmZlMTMwOTBkYS8iLCJvaWQiOiIwZjU1NTJjMi05ODA0LTRkNzMtODFkNS0yODI3MDBiNGNmMmMiLCJyaCI6IjAuQWE0QS1SZW9yWFRCTWtxdXQzRXY0VENRMmpGcTZLcG92dnBOc3RkUWk2dG9ZSjZyQUFBLiIsInN1YiI6IjBmNTU1MmMyLTk4MDQtNGQ3My04MWQ1LTI4MjcwMGI0Y2YyYyIsInRpZCI6ImFkYTgxN2Y5LWMxNzQtNGEzMi1hZWI3LTcxMmZlMTMwOTBkYSIsInV0aSI6Il9peEU1RVpBa2t1V0FPMTZPeVVUQXciLCJ2ZXIiOiIxLjAifQ.XSbt2iz--paxOwAPkNYTHkoy9ZM0cKopjHLNJUr7n7bS3C6NoE6d9xOwgLFCcfGwB4Mo1Fw67VH2JvXFHd8gq9KaZO0U-5hyWuBd6Ja359wTfm6KI4HbrNcb6PlGwFZFIQfnaUhiqCL1Iws1r21efqDv-g4-9iVjEaeFIzxOG62pmpSeo41WC60kvFJ-BHJjRTjRTIzgbXoQBwTF-Ud5YCynJh1DI-jgOi8w1l3_buUlt6nv8BX19_e29g2ai1IJIIV41yzvjU8cA8Xf3PwyHne8mTkNb8EJN7Mr8pi2lzSwWjqGmRfZPPDKk3EsjKW8X1Wstc9Y9E8pNe6FgJBMzQ']}"""
data_clean = ast.literal_eval(data)

def correct_padding(s):
    return s + '=' * (-len(s) % 4)

encrypted_data_key = b64decode(correct_padding(data_clean['value'][0]['encryptedContent']['data']))
encrypted_data = b64decode(correct_padding(data_clean['value'][0]['encryptedContent']['dataKey']))
data_signature = b64decode(correct_padding(data_clean['validationTokens'][0]))

# encrypted_data_key_b64  = data_clean['value'][0]['encryptedContent']['data']
# encrypted_data_b64 = data_clean['value'][0]['encryptedContent']['dataKey']
# data_signature_b64 = data_clean['validationTokens'][0]

# Base64 decode the encrypted data key and data
encrypted_data_key = b64decode(encrypted_data_key)
encrypted_data = b64decode(encrypted_data)
data_signature = b64decode(data_signature)

# Path to your private key file
private_key_file_path = 'private_key.pem'
private_key_pem = b""""""

# Load your private RSA key
private_key = serialization.load_pem_private_key(
    private_key_pem,
    password=None,  # Provide password if your key is encrypted
    backend=default_backend()
)

# Function to load a private key from a file
def load_private_key(file_path):
    with open(file_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # Replace with 'b"yourpassword"' if the key is encrypted
            backend=default_backend()
        )
    return private_key

def decryptData(encrypted_data):
    # Load your private key
    #private_key = load_private_key(private_key_file_path)
    # Decrypt the symmetric key (dataKey)
    decrypted_data_key = private_key.decrypt(
        encrypted_data_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None  # This will usually be None
        )
    )
    
    iv = decrypted_data_key[:16]
    cipher = Cipher(
        algorithms.AES(decrypted_data_key),
        modes.CBC(iv),
        backend=default_backend()
    )

    # Decrypt the data
    plaintext = private_key.decrypt(
        b64decode(encrypted_data),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None  # This is typically None, but check your encryption details
        )
    )
    return plaintext

# Decrypt the data

decryptData(data)