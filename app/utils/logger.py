import logging
import logging.handlers
import os
from pathlib import Path
from decouple import config


class AgentLogger:
    """
    Logger centralizado para o Email Monitor Agent.
    Suporta logging em arquivo com rotação e console.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.logger = logging.getLogger('EmailMonitorAgent')
        
        # Configurações do .env
        log_level = config('LOG_LEVEL', default='INFO')
        log_file = config('LOG_FILE', default='logs/email_agent.log')
        max_bytes = config('LOG_MAX_BYTES', default=10485760, cast=int)  # 10MB
        backup_count = config('LOG_BACKUP_COUNT', default=5, cast=int)
        
        # Set level
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Evitar duplicação de handlers
        if not self.logger.handlers:
            # Criar diretório de logs se não existir
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Formato de log
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            # Handler para arquivo com rotação
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            # Handler para console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def get_logger(self):
        return self.logger


# Singleton para facilitar o uso
def get_logger():
    """Retorna a instância do logger."""
    return AgentLogger().get_logger()
