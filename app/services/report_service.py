from datetime import datetime, timedelta
from typing import List, Dict
from app.utils.logger import get_logger

logger = get_logger()


class ReportService:
    """
    Serviço para geração de relatórios e análises de emails.
    """
    
    def __init__(self, email_service):
        self.email_service = email_service
        logger.info("ReportService inicializado")
    
    def get_today_summary(self) -> Dict:
        """
        Gera resumo de emails recebidos hoje.
        Inclui informação sobre anexos.
        
        Returns:
            {
                'total': 15,
                'with_attachments': 5,
                'without_attachments': 10,
                'emails': [...]
            }
        """
        try:
            # Busca emails recebidos hoje
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_start_iso = today_start.isoformat() + 'Z'
            
            url = (
                f"{self.email_service.BASE_URL}/me/messages"
                f"?$filter=receivedDateTime ge {today_start_iso}"
                f"&$select=id,subject,from,receivedDateTime,hasAttachments,bodyPreview"
                f"&$orderby=receivedDateTime desc"
                f"&$top=100"
            )
            
            logger.debug("Buscando emails recebidos hoje...")
            result = self.email_service._make_request(url)
            
            emails = result.get('value', [])
            
            # Conta emails com/sem anexo
            with_attachments = [e for e in emails if e.get('hasAttachments', False)]
            without_attachments = [e for e in emails if not e.get('hasAttachments', False)]
            
            summary = {
                'total': len(emails),
                'with_attachments': len(with_attachments),
                'without_attachments': len(without_attachments),
                'emails': emails
            }
            
            logger.info(f"Resumo: {len(emails)} emails hoje ({len(with_attachments)} com anexo)")
            
            return summary
        
        except Exception as e:
            logger.error(f"Erro ao gerar resumo do dia: {e}")
            return {
                'total': 0,
                'with_attachments': 0,
                'without_attachments': 0,
                'emails': []
            }
    
    def get_unanswered_emails(self, days: int = 7) -> List[Dict]:
        """
        Busca emails SEM RESPOSTA nos últimos X dias.
        
        NOTA: Verifica se há emails na thread de conversa.
        Se só tem 1 email = sem resposta.
        
        Args:
            days: Número de dias para verificar
        
        Returns:
            Lista de emails sem resposta
        """
        try:
            # Data de início (X dias atrás)
            start_date = datetime.now() - timedelta(days=days)
            start_date_iso = start_date.isoformat() + 'Z'
            
            # Busca emails recebidos (não enviados por mim)
            url = (
                f"{self.email_service.BASE_URL}/me/messages"
                f"?$filter=receivedDateTime ge {start_date_iso}"
                f"&$select=id,subject,from,receivedDateTime,conversationId,isRead"
                f"&$orderby=receivedDateTime desc"
                f"&$top=100"
            )
            
            logger.debug(f"Buscando emails dos últimos {days} dias...")
            result = self.email_service._make_request(url)
            
            emails = result.get('value', [])
            
            # Para cada email, verifica se tem respostas
            unanswered = []
            
            for email in emails:
                conversation_id = email.get('conversationId')
                
                # Busca emails na mesma conversa
                conv_url = (
                    f"{self.email_service.BASE_URL}/me/messages"
                    f"?$filter=conversationId eq '{conversation_id}'"
                    f"&$select=id,from"
                    f"&$top=10"
                )
                
                try:
                    conv_result = self.email_service._make_request(conv_url)
                    thread_emails = conv_result.get('value', [])
                    
                    # Verifica se EU respondi (se tem email MEU na thread)
                    my_replies = [
                        e for e in thread_emails
                        if e.get('from', {}).get('emailAddress', {}).get('address', '').lower() 
                        != email.get('from', {}).get('emailAddress', {}).get('address', '').lower()
                    ]
                    
                    # Se não tem respostas minhas, adiciona na lista
                    if len(my_replies) == 0:
                        unanswered.append(email)
                
                except Exception as e:
                    logger.warning(f"Erro ao verificar conversa {conversation_id}: {e}")
                    continue
            
            logger.info(f"Encontrados {len(unanswered)} emails sem resposta")
            
            return unanswered
        
        except Exception as e:
            logger.error(f"Erro ao buscar emails sem resposta: {e}")
            return []
    
    def format_today_summary(self, summary: Dict) -> str:
        """
        Formata resumo do dia em texto legível.
        """
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("📊 RESUMO DE EMAILS RECEBIDOS HOJE")
        lines.append("=" * 80)
        
        # Estatísticas
        lines.append(f"\n📬 Total de emails: {summary['total']}")
        lines.append(f"📎 Com anexos: {summary['with_attachments']}")
        lines.append(f"📄 Sem anexos: {summary['without_attachments']}")
        
        if summary['emails']:
            lines.append("\n" + "-" * 80)
            lines.append("DETALHES DOS EMAILS:")
            lines.append("-" * 80)
            
            for idx, email in enumerate(summary['emails'][:20], 1):  # Limita em 20
                sender = email.get('from', {}).get('emailAddress', {}).get('address', 'Desconhecido')
                subject = email.get('subject', 'Sem assunto')[:50]
                received = email.get('receivedDateTime', '')[:16]  # Só data e hora
                has_attachment = "📎" if email.get('hasAttachments') else "  "
                
                lines.append(f"\n{idx}. {has_attachment} [{received}] {subject}")
                lines.append(f"   De: {sender}")
        
        lines.append("\n" + "=" * 80)
        
        return "\n".join(lines)
    
    def format_unanswered_emails(self, emails: List[Dict]) -> str:
        """
        Formata lista de emails sem resposta.
        """
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("⚠️  EMAILS SEM RESPOSTA (Últimos 7 dias)")
        lines.append("=" * 80)
        
        if not emails:
            lines.append("\n✅ Parabéns! Todos os emails foram respondidos.")
        else:
            lines.append(f"\n📭 Total: {len(emails)} emails aguardando resposta")
            lines.append("\n" + "-" * 80)
            
            for idx, email in enumerate(emails[:30], 1):  # Limita em 30
                sender = email.get('from', {}).get('emailAddress', {}).get('address', 'Desconhecido')
                subject = email.get('subject', 'Sem assunto')[:50]
                received = email.get('receivedDateTime', '')[:10]  # Só data
                
                # Calcula dias sem resposta
                received_dt = datetime.fromisoformat(email.get('receivedDateTime', '').replace('Z', '+00:00'))
                days_ago = (datetime.now().astimezone() - received_dt).days
                
                urgency = "🔴" if days_ago >= 3 else "🟡" if days_ago >= 1 else "🟢"
                
                lines.append(f"\n{idx}. {urgency} {subject}")
                lines.append(f"   De: {sender}")
                lines.append(f"   Recebido: {received} ({days_ago} dia(s) atrás)")
        
        lines.append("\n" + "=" * 80)
        
        return "\n".join(lines)
