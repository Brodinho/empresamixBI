from enum import Enum
from typing import List, Dict
import yaml
from pathlib import Path

class UserRole(Enum):
    ADMIN = "admin"
    COMERCIAL = "comercial"
    FINANCEIRO = "financeiro"
    MARKETING = "marketing"
    OPERACIONAL = "operacional"
    RH = "rh"

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

class Permissions:
    @staticmethod
    def get_allowed_kpis(role: UserRole) -> dict:
        """Define quais KPIs cada perfil pode ver"""
        permissions = {
            UserRole.ADMIN: ["all"],
            UserRole.COMERCIAL: ["faturamento", "leads", "conversao", "satisfacao"],
            UserRole.FINANCEIRO: ["faturamento", "margem_ebitda", "custo_operacional"],
            UserRole.MARKETING: ["leads", "conversao", "satisfacao"],
            UserRole.OPERACIONAL: ["eficiencia", "ordens_producao"],
            UserRole.RH: ["turnover", "eficiencia"]
        }
        return permissions.get(role, [])

    @staticmethod
    def can_view_kpi(role: UserRole, kpi_name: str) -> bool:
        """Verifica se o usuário pode ver determinado KPI"""
        allowed_kpis = Permissions.get_allowed_kpis(role)
        return "all" in allowed_kpis or kpi_name in allowed_kpis

    @staticmethod
    def get_allowed_modules(role: UserRole) -> list:
        """Define quais módulos cada perfil pode acessar"""
        permissions = {
            UserRole.ADMIN: ["all"],
            UserRole.COMERCIAL: ["comercial", "marketing"],
            UserRole.FINANCEIRO: ["financeiro", "comercial"],
            UserRole.MARKETING: ["marketing", "comercial"],
            UserRole.OPERACIONAL: ["operacional", "pcp"],
            UserRole.RH: ["rh"]
        }
        return permissions.get(role, [])

    @staticmethod
    def can_access_module(role: UserRole, module_id: str) -> bool:
        """Verifica se o usuário pode acessar determinado módulo"""
        allowed_modules = Permissions.get_allowed_modules(role)
        return "all" in allowed_modules or module_id in allowed_modules

permission_manager = PermissionManager()
