from core.auth.permissions import UserRole, Permissions

class AlertManager:
    @staticmethod
    def get_module_alerts(module: str, user_role: UserRole) -> list:
        """Retorna alertas específicos do módulo se o usuário tem permissão"""
        if not Permissions.can_access_module(user_role, module):
            return []
            
        alerts = {
            "comercial": [
                ("warning", "Meta de vendas próxima do prazo"),
                ("info", "Novos leads aguardando contato")
            ],
            "financeiro": [
                ("warning", "Contas a pagar vencendo esta semana"),
                ("info", "Relatório mensal disponível")
            ],
            "marketing": [
                ("info", "Nova campanha iniciada"),
                ("success", "Meta de leads atingida")
            ],
            "operacional": [
                ("warning", "Estoque de matéria-prima X abaixo do mínimo"),
                ("info", "5 ordens de produção aguardando aprovação")
            ],
            "pcp": [
                ("warning", "Capacidade próxima do limite"),
                ("info", "Novas ordens de produção disponíveis")
            ],
            "rh": [
                ("info", "Avaliações de desempenho pendentes"),
                ("success", "Treinamento concluído com sucesso")
            ]
        }
        return alerts.get(module, []) 