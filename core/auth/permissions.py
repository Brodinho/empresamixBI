from enum import Enum
from typing import List, Dict
import yaml
from pathlib import Path

class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class ModulePermission(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

class PermissionManager:
    def __init__(self):
        self.permissions: Dict = self._load_permissions()
    
    def _load_permissions(self) -> Dict:
        """Carrega as permissões do arquivo YAML"""
        permissions_file = Path("config/permissions.yaml")
        if permissions_file.exists():
            with open(permissions_file) as f:
                return yaml.safe_load(f)
        return {}
    
    def get_user_modules(self, username: str) -> List[str]:
        """Retorna lista de módulos que o usuário tem acesso"""
        if username not in self.permissions:
            return []
        return list(self.permissions[username]["modules"].keys())
    
    def can_access_module(self, username: str, module: str) -> bool:
        """Verifica se usuário tem acesso ao módulo"""
        if username not in self.permissions:
            return False
        return module in self.permissions[username]["modules"]
    
    def get_module_permission_level(self, username: str, module: str) -> ModulePermission:
        """Retorna nível de permissão do usuário no módulo"""
        if not self.can_access_module(username, module):
            return None
        return ModulePermission(self.permissions[username]["modules"][module])

permission_manager = PermissionManager()
