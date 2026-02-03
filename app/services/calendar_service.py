import requests
from datetime import datetime, timedelta
from app.utils.logger import get_logger

logger = get_logger()


class CalendarService:
    """
    Serviço para interação com Microsoft Graph API (calendário).
    """
    
    BASE_URL = "https://graph.microsoft.com/v1.0"
    
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        logger.info("CalendarService inicializado")
    
    def get_events(self, days_ahead: int = 1, limit: int = 5) -> list:
        """
        Busca eventos do calendário.
        
        Args:
            days_ahead: Quantos dias à frente buscar eventos
            limit: Número máximo de eventos a retornar
        
        Returns:
            Lista de eventos
        """
        try:
            # Período: de agora até X dias à frente
            start_time = datetime.now().isoformat()
            end_time = (datetime.now() + timedelta(days=days_ahead)).isoformat()
            
            url = (
                f"{self.BASE_URL}/me/calendarview"
                f"?startDateTime={start_time}"
                f"&endDateTime={end_time}"
                f"&$top={limit}"
                f"&$select=subject,start,end,location,isOnlineMeeting,onlineMeetingUrl"
                f"&$orderby=start/dateTime"
            )
            
            logger.debug(f"Buscando eventos dos próximos {days_ahead} dias...")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            events = response.json().get('value', [])
            logger.info(f"Encontrados {len(events)} eventos futuros")
            
            return events
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar eventos: {e}")
            return []
        
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar eventos: {e}")
            return []
