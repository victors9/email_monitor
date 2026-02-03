import requests
from app.utils.logger import get_logger

logger = get_logger()


class UserService:
    """
    Serviço para interação com usuários e presença no Microsoft Graph.
    """
    
    BASE_URL = "https://graph.microsoft.com/v1.0"
    
    # Mapeamento de status para emoji e descrição
    PRESENCE_MAP = {
        'Available': {'emoji': '🟢', 'description': 'Disponível'},
        'AvailableIdle': {'emoji': '🟡', 'description': 'Disponível (Ausente)'},
        'Away': {'emoji': '🟡', 'description': 'Ausente'},
        'BeRightBack': {'emoji': '🟡', 'description': 'Volto Logo'},
        'Busy': {'emoji': '🔴', 'description': 'Ocupado'},
        'BusyIdle': {'emoji': '🔴', 'description': 'Ocupado (Ausente)'},
        'DoNotDisturb': {'emoji': '⛔', 'description': 'Não Perturbe'},
        'InACall': {'emoji': '📞', 'description': 'Em Chamada'},
        'InAConferenceCall': {'emoji': '📞', 'description': 'Em Conferência'},
        'Inactive': {'emoji': '⚪', 'description': 'Inativo'},
        'InAMeeting': {'emoji': '📅', 'description': 'Em Reunião'},
        'Offline': {'emoji': '⚫', 'description': 'Offline'},
        'OffWork': {'emoji': '🏠', 'description': 'Fora do Trabalho'},
        'OutOfOffice': {'emoji': '✈️', 'description': 'Fora do Escritório'},
        'PresenceUnknown': {'emoji': '❓', 'description': 'Desconhecido'},
        'Presenting': {'emoji': '🖥️', 'description': 'Apresentando'},
        'UrgentInterruptionsOnly': {'emoji': '🚨', 'description': 'Apenas Urgências'},
    }
    
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        logger.info("UserService inicializado")
    
    def get_all_users(self) -> list:
        """
        Lista todos os usuários da organização.
        
        Returns:
            Lista de usuários com id, displayName, email
        """
        try:
            url = f"{self.BASE_URL}/users?$select=id,displayName,mail,userPrincipalName"
            
            logger.debug("Buscando usuários da organização...")
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            users = response.json().get('value', [])
            logger.info(f"Encontrados {len(users)} usuários")
            
            return users
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar usuários: {e}")
            return []
    
    def get_user_presence(self, user_id: str) -> dict:
        """
        Obtém status de presença de um usuário específico.
        
        Args:
            user_id: ID do usuário
        
        Returns:
            Dict com availability, activity
        """
        try:
            url = f"{self.BASE_URL}/users/{user_id}/presence"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            presence = response.json()
            return {
                'availability': presence.get('availability', 'Unknown'),
                'activity': presence.get('activity', 'Unknown')
            }
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.debug(f"Presença não disponível para usuário {user_id}")
                return {'availability': 'Unknown', 'activity': 'Unknown'}
            else:
                logger.error(f"Erro ao buscar presença: {e}")
                return {'availability': 'Unknown', 'activity': 'Unknown'}
        
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar presença: {e}")
            return {'availability': 'Unknown', 'activity': 'Unknown'}
    
    def get_all_users_with_presence(self, max_users: int = 50) -> list:
        """
        Lista todos os usuários COM status de presença.
        
        NOTA: Pode ser lento se tiver muitos usuários.
        
        Args:
            max_users: Número máximo de usuários a buscar
        
        Returns:
            Lista de dicts com user info + presence
        """
        users = self.get_all_users()[:max_users]
        
        result = []
        for user in users:
            user_id = user.get('id')
            display_name = user.get('displayName', 'Sem nome')
            email = user.get('mail') or user.get('userPrincipalName', 'Sem email')
            
            # Busca presença
            presence = self.get_user_presence(user_id)
            availability = presence['availability']
            
            # Mapeia para formato amigável
            presence_info = self.PRESENCE_MAP.get(
                availability,
                {'emoji': '❓', 'description': availability}
            )
            
            result.append({
                'name': display_name,
                'email': email,
                'status': availability,
                'emoji': presence_info['emoji'],
                'status_description': presence_info['description']
            })
        
        return result
    
    def format_users_table(self, users: list) -> str:
        """
        Formata lista de usuários em tabela ASCII.
        """
        if not users:
            return "Nenhum usuário encontrado."
        
        # Header
        lines = []
        lines.append("=" * 80)
        lines.append(f"{'Status':<10} {'Nome':<30} {'Email':<40}")
        lines.append("-" * 80)
        
        # Body
        for user in users:
            status = f"{user['emoji']} {user['status_description']}"
            name = user['name'][:28]
            email = user['email'][:38]
            
            lines.append(f"{status:<10} {name:<30} {email:<40}")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
