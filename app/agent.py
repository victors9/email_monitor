import time
from datetime import datetime
from app.services.email_service import EmailService
from app.services.calendar_service import CalendarService
from app.services.ai_service import AIService
from app.utils.heartbeat import Heartbeat
from app.utils.logger import get_logger

logger = get_logger()


class EmailMonitorAgent:
    """
    Agente principal que monitora emails e calendário.
    Usa IA para classificar e sugerir respostas.
    """
    
    def __init__(self, email_service: EmailService, calendar_service: CalendarService, 
                 ai_service: AIService, heartbeat: Heartbeat, check_interval: int = 30):
        self.email_service = email_service
        self.calendar_service = calendar_service
        self.ai_service = ai_service
        self.heartbeat = heartbeat
        self.check_interval = check_interval
        self.running = False
        
        logger.info("EmailMonitorAgent inicializado")
    
    def _process_email(self, email: dict):
        """
        Processa um único email.
        """
        try:
            email_id = email.get('id', 'unknown')
            subject = email.get('subject', 'Sem assunto')
            sender = email.get('from', {}).get('emailAddress', {}).get('address', 'Desconhecido')
            received = email.get('receivedDateTime', '')
            
            logger.info(f"\n{'='*60}")
            logger.info(f"📧 NOVO EMAIL")
            logger.info(f"De: {sender}")
            logger.info(f"Assunto: {subject}")
            logger.info(f"Recebido: {received}")
            
            # Classificação de urgência com IA
            urgency = self.ai_service.classify_urgency(email)
            
            # Emoji visual baseado na urgência
            urgency_emoji = {
                'ALTA': '🔴',
                'MÉDIA': '🟡',
                'BAIXA': '🟢'
            }.get(urgency, '⚪')
            
            logger.info(f"Urgência: {urgency_emoji} {urgency}")
            
            # Sugestão de resposta (simplificado por enquanto)
            if urgency == "ALTA":
                suggestion = self.ai_service.suggest_reply(email)
                logger.info(f"\n💡 Sugestão de resposta:\n{suggestion}")
            
            logger.info(f"{'='*60}\n")
            
        except Exception as e:
            logger.error(f"Erro ao processar email: {e}")
    
    def _check_emails(self):
        """
        Verifica e processa emails não lidos.
        """
        try:
            emails = self.email_service.get_unread_emails()
            
            if not emails:
                logger.debug("Nenhum email novo")
                return
            
            logger.info(f"📬 {len(emails)} email(s) não lido(s) encontrado(s)")
            
            for email in emails:
                self._process_email(email)
        
        except Exception as e:
            logger.error(f"Erro ao verificar emails: {e}")
    
    def _check_calendar(self):
        """
        Verifica eventos próximos do calendário.
        """
        try:
            events = self.calendar_service.get_events(days_ahead=1, limit=3)
            
            if not events:
                logger.debug("Nenhum evento próximo")
                return
            
            logger.info(f"\n📅 {len(events)} evento(s) nas próximas 24h:")
            
            for event in events:
                subject = event.get('subject', 'Sem título')
                start = event.get('start', {}).get('dateTime', '')
                location = event.get('location', {}).get('displayName', 'Sem local')
                is_online = event.get('isOnlineMeeting', False)
                
                meeting_type = "💻 Online" if is_online else f"📍 {location}"
                
                logger.info(f"  • {subject}")
                logger.info(f"    Início: {start}")
                logger.info(f"    Local: {meeting_type}")
        
        except Exception as e:
            logger.error(f"Erro ao verificar calendário: {e}")
    
    def run(self):
        """
        Loop principal do agente.
        """
        self.running = True
        logger.info("🚀 Agente iniciado e monitorando...")
        logger.info(f"⏱️  Verificando a cada {self.check_interval} segundos")
        
        try:
            while self.running:
                # Verifica emails
                self._check_emails()
                
                # Verifica calendário (menos frequente, só no heartbeat)
                if self.heartbeat.check():
                    self._check_calendar()
                
                # Aguarda próximo ciclo
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            logger.info("\n⚠️  Interrupção detectada. Finalizando agente...")
            self.stop()
        
        except Exception as e:
            logger.error(f"❌ Erro fatal no loop principal: {e}")
            self.stop()
            raise
    
    def stop(self):
        """
        Para o agente gracefully.
        """
        self.running = False
        logger.info("🛑 Agente finalizado")
