from datetime import datetime, timedelta
from app.utils.logger import get_logger

logger = get_logger()


class Heartbeat:
    """
    Sistema de heartbeat para monitorar que o agente está ativo.
    """
    
    def __init__(self, interval_minutes: int):
        self.interval = timedelta(minutes=interval_minutes)
        self.last = datetime.now()
        logger.info(f"Heartbeat configurado para {interval_minutes} minutos")
    
    def check(self) -> bool:
        """
        Verifica se é hora de emitir heartbeat.
        
        Returns:
            True se deve emitir heartbeat, False caso contrário
        """
        now = datetime.now()
        
        if now - self.last >= self.interval:
            self.last = now
            elapsed = str(self.interval)
            logger.info(f"💓 Heartbeat - Agente ativo (última verificação: {elapsed} atrás)")
            return True
        
        return False
    
    def reset(self):
        """Reseta o timer do heartbeat."""
        self.last = datetime.now()
        logger.debug("Heartbeat resetado")
