import sys
sys.path.append("Avocet")
import unittest
from avocet.avocet import Avocet

class TestPyPyCryptLib(unittest.TestCase):
    
    def test_caeser_cipher(self):
        # Test Caesar cipher with different shifts
        self.assertEqual(Avocet.caeser_cipher('abc', 3), 'def')
        self.assertEqual(Avocet.caeser_cipher('xyz', 3), 'abc')
        self.assertEqual(Avocet.caeser_cipher('Hello, World!', 5), 'Mjqqt, Btwqi!')
    
    def test_base64_encode_decode(self):
        # Test Base64 encoding and decoding
        original_text = 'Hello, World!'
        encoded_text = Avocet.base_64_encode(original_text)
        decoded_text = Avocet.base_64_decode(encoded_text)
        self.assertEqual(original_text, decoded_text)
    
    def test_hex_encode_decode(self):
        # Test Hex encoding and decoding
        original_text = 'Hello, World!'
        encoded_text = Avocet.hex_encode(original_text)
        decoded_text = Avocet.hex_decode(encoded_text)
        self.assertEqual(original_text, decoded_text)
    
    def test_xor_cipher(self):
        # Test XOR cipher encoding and decoding
        text = 'Hello, World!'
        key = 'key'
        encoded_text = Avocet.xor_cipher_encode(text, key)
        decoded_text = Avocet.xor_cipher_decode(encoded_text, key)
        self.assertEqual(text, decoded_text)
        
    
    def test_md5_hash(self):
        # Test MD5 hashing
        text = 'Hello, World!'
        expected_hash = '65a8e27d8879283831b664bd8b7f0ad4'
        self.assertEqual(Avocet.md5_hash(text), expected_hash)
    
    def test_sha1(self):
        # Test SHA-1 hashing
        text = 'Hello, World!'
        expected_hash = '0a0a9f2a6772942557ab5355d76af442f8f65e01'
        self.assertEqual(Avocet.sha1(text), expected_hash)
    
    def test_sha256(self):
        # Test SHA-256 hashing
        text = 'Hello, World!'
        expected_hash = 'dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f'
        self.assertEqual(Avocet.sha256(text), expected_hash)
    
    def test_sha512(self):
        # Test SHA-512 hashing
        text = 'Hello, World!'
        expected_hash = '374d794a95cdcfd8b35993185fef9ba368f160d8daf432d08ba9f1ed1e5abe6cc69291e0fa2fe0006a52570ef18c19def4e617c33ce52ef0a6e5fbe318cb0387'
        self.assertEqual(Avocet.sha512(text), expected_hash)
    
    def test_sha3_256(self):
        # Test SHA-3 256 hashing
        text = 'Hello, World!'
        expected_hash = '1af17a664e3fa8e419b8ba05c2a173169df76162a5a286e0c405b460d478f7ef'
        self.assertEqual(Avocet.sha3_256(text), expected_hash)
    
    def test_sha3_512(self):
        # Test SHA-3 512 hashing
        text = 'Hello, World!'
        expected_hash = '38e05c33d7b067127f217d8c856e554fcff09c9320b8a5979ce2ff5d95dd27ba35d1fba50c562dfd1d6cc48bc9c5baa4390894418cc942d968f97bcb659419ed'
        self.assertEqual(Avocet.sha3_512(text), expected_hash)
    
    def test_rsa_encode_decode(self):
        # Generate RSA keys for testing
        from Cryptodome.PublicKey import RSA
        from Cryptodome.Cipher import PKCS1_OAEP
        import base64
        
        # Generate a pair of RSA keys
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        text = 'Hello, World!'
        
        # Encrypt and decrypt the text
        encrypted_text = Avocet.rsa_encode(text, public_key)
        decrypted_text = Avocet.rsa_decode(encrypted_text, private_key)
        
        self.assertEqual(text, decrypted_text)

if __name__ == '__main__':
    unittest.main()
