import requests
import time
from app.utils.logger import get_logger

logger = get_logger()


class EmailService:
    """
    Serviço para interação com Microsoft Graph API (emails).
    Inclui retry automático e tratamento de erros.
    """
    
    BASE_URL = "https://graph.microsoft.com/v1.0"
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # segundos
    
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        logger.info("EmailService inicializado")
    
    def _make_request(self, url: str, method: str = "GET", data: dict = None, retries: int = 0):
        """
        Faz requisição HTTP com retry automático.
        """
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=10)
            elif method == "PATCH":
                response = requests.patch(url, headers=self.headers, json=data, timeout=10)
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("Token expirado ou inválido. Necessário re-autenticar.")
                raise
            elif e.response.status_code == 429:
                logger.warning("Rate limit atingido. Aguardando...")
                time.sleep(self.RETRY_DELAY * 2)
                if retries < self.MAX_RETRIES:
                    return self._make_request(url, method, data, retries + 1)
            else:
                logger.error(f"Erro HTTP {e.response.status_code}: {e}")
                raise
        
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout na requisição. Tentativa {retries + 1}/{self.MAX_RETRIES}")
            if retries < self.MAX_RETRIES:
                time.sleep(self.RETRY_DELAY)
                return self._make_request(url, method, data, retries + 1)
            else:
                logger.error("Max retries atingido")
                raise
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            if retries < self.MAX_RETRIES:
                time.sleep(self.RETRY_DELAY)
                return self._make_request(url, method, data, retries + 1)
            else:
                raise
    
    def get_unread_emails(self, limit: int = 5) -> list:
        """
        Busca emails não lidos.
        
        Args:
            limit: Número máximo de emails a retornar
        
        Returns:
            Lista de emails não lidos
        """
        try:
            url = (
                f"{self.BASE_URL}/me/messages"
                f"?$filter=isRead eq false"
                f"&$top={limit}"
                f"&$select=id,subject,from,receivedDateTime,importance,bodyPreview,isRead"
                f"&$orderby=receivedDateTime desc"
            )
            
            logger.debug(f"Buscando até {limit} emails não lidos...")
            result = self._make_request(url)
            
            emails = result.get('value', [])
            logger.info(f"Encontrados {len(emails)} emails não lidos")
            
            return emails
        
        except Exception as e:
            logger.error(f"Erro ao buscar emails: {e}")
            return []
    
    def mark_as_read(self, email_id: str) -> bool:
        """
        Marca email como lido.
        
        Args:
            email_id: ID do email
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            url = f"{self.BASE_URL}/me/messages/{email_id}"
            data = {"isRead": True}
            
            self._make_request(url, method="PATCH", data=data)
            logger.info(f"Email {email_id[:8]}... marcado como lido")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao marcar email como lido: {e}")
            return False
