#!/usr/bin/env python3
"""
Email Monitor Agent - Sistema com Menu Interativo
Versão: 2.0 (Com Menu)
"""

from app.config.settings import TENANT_ID, CLIENT_ID, SCOPES
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.services.user_service import UserService
from app.services.report_service import ReportService
from app.services.ai_service import AIService
from app.services.chat_service import ChatService
from app.menu import MenuSystem
from app.utils.logger import get_logger

logger = get_logger()


def main():
    """
    Entry point do agente com menu interativo.
    """
    logger.info("=" * 60)
    logger.info("🤖 EMAIL MONITOR AGENT v2.1 - Menu + Chat")
    logger.info("=" * 60)
    
    try:
        # Autenticação
        logger.info("🔐 Iniciando autenticação...")
        auth = AuthService(TENANT_ID, CLIENT_ID, SCOPES)
        token = auth.get_token()
        logger.info("✅ Autenticação bem-sucedida")
        
        # Inicialização dos serviços
        logger.info("⚙️  Inicializando serviços...")
        email_service = EmailService(token)
        user_service = UserService(token)
        ai_service = AIService()
        report_service = ReportService(email_service)
        chat_service = ChatService(email_service, ai_service, report_service)
        logger.info("✅ Serviços inicializados")
        
        # Criação e execução do menu
        menu = MenuSystem(
            email_service=email_service,
            user_service=user_service,
            report_service=report_service,
            chat_service=chat_service
        )
        
        logger.info("🚀 Iniciando menu interativo...")
        menu.run()
    
    except KeyboardInterrupt:
        logger.info("\n🛑 Execução interrompida pelo usuário")
    
    except Exception as e:
        logger.error(f"\n❌ Erro fatal na inicialização: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
