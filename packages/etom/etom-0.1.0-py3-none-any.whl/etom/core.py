import os
from cryptography.fernet import Fernet
import toml
import json
from typing import Any, Dict, List, Union

class EncryptedTOML:
    def __init__(self, key: Union[str, bytes] = None):
        if key is None:
            key = Fernet.generate_key()
        elif isinstance(key, str):
            key = key.encode()
        self.fernet = Fernet(key)
    
    def encrypt(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode())
    
    def decrypt(self, encrypted_data: bytes) -> str:
        return self.fernet.decrypt(encrypted_data).decode()
    
    def save(self, data: Dict[str, Any], filename: str) -> None:
        encrypted_data = self.encrypt(toml.dumps(data))
        with open(filename, 'wb') as f:
            f.write(encrypted_data)
    
    def load(self, filename: str) -> Dict[str, Any]:
        with open(filename, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = self.decrypt(encrypted_data)
        return toml.loads(decrypted_data)
    
    def update(self, filename: str, new_data: Dict[str, Any]) -> None:
        current_data = self.load(filename)
        current_data.update(new_data)
        self.save(current_data, filename)
    
    def update_key(self, filename: str, key_path: List[str], value: Any) -> None:
        data = self.load(filename)
        current = data
        for key in key_path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[key_path[-1]] = value
        self.save(data, filename)
    
    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()
    
    @staticmethod
    def save_key(key: bytes, filename: str) -> None:
        with open(filename, 'wb') as f:
            f.write(key)
    
    @staticmethod
    def load_key(filename: str) -> bytes:
        with open(filename, 'rb') as f:
            return f.read()
    
    def to_json(self, filename: str) -> str:
        data = self.load(filename)
        return json.dumps(data, indent=2)
    
    def from_json(self, json_str: str, filename: str) -> None:
        data = json.loads(json_str)
        self.save(data, filename)