#!/usr/bin/env python3
"""
Email Monitor Agent - Sistema de monitoramento inteligente de emails
Usando IA local (Llama 3.2 via Ollama) e Microsoft Graph API
"""

from app.config.settings import (
    TENANT_ID, CLIENT_ID, SCOPES,
    CHECK_INTERVAL_SECONDS, HEARTBEAT_MINUTES
)
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.services.calendar_service import CalendarService
from app.services.ai_service import AIService
from app.utils.heartbeat import Heartbeat
from app.utils.logger import get_logger
from app.agent import EmailMonitorAgent

logger = get_logger()


def main():
    """
    Entry point do agente.
    """
    logger.info("="*60)
    logger.info("🤖 EMAIL MONITOR AGENT")
    logger.info("="*60)
    
    try:
        # Autenticação
        logger.info("🔐 Iniciando autenticação...")
        auth = AuthService(TENANT_ID, CLIENT_ID, SCOPES)
        token = auth.get_token()
        logger.info("✅ Autenticação bem-sucedida")
        
        # Inicialização dos serviços
        logger.info("⚙️  Inicializando serviços...")
        email_service = EmailService(token)
        calendar_service = CalendarService(token)
        ai_service = AIService()
        heartbeat = Heartbeat(HEARTBEAT_MINUTES)
        logger.info("✅ Serviços inicializados")
        
        # Criação e execução do agente
        agent = EmailMonitorAgent(
            email_service=email_service,
            calendar_service=calendar_service,
            ai_service=ai_service,
            heartbeat=heartbeat,
            check_interval=CHECK_INTERVAL_SECONDS
        )
        
        agent.run()
    
    except KeyboardInterrupt:
        logger.info("\n🛑 Execução interrompida pelo usuário")
    
    except Exception as e:
        logger.error(f"\n❌ Erro fatal na inicialização: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
