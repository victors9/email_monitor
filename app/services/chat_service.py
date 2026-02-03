import json
from datetime import datetime, timedelta
from app.utils.logger import get_logger

logger = get_logger()


class ChatService:
    """
    Serviço de chat interativo com IA.
    Permite conversar com o agente sobre emails.
    """
    
    def __init__(self, email_service, ai_service, report_service):
        self.email_service = email_service
        self.ai_service = ai_service
        self.report_service = report_service
        self.conversation_history = []
        logger.info("ChatService inicializado")
    
    def _get_email_context(self) -> str:
        """
        Busca contexto atual dos emails para a IA.
        """
        try:
            # Busca emails recentes (últimos 3 dias)
            start_date = datetime.now() - timedelta(days=3)
            start_date_iso = start_date.isoformat() + 'Z'
            
            url = (
                f"{self.email_service.BASE_URL}/me/messages"
                f"?$filter=receivedDateTime ge {start_date_iso}"
                f"&$select=id,subject,from,receivedDateTime,isRead,hasAttachments,importance"
                f"&$orderby=receivedDateTime desc"
                f"&$top=50"
            )
            
            result = self.email_service._make_request(url)
            emails = result.get('value', [])
            
            # Resume informações importantes
            total_emails = len(emails)
            unread_emails = [e for e in emails if not e.get('isRead', True)]
            with_attachments = [e for e in emails if e.get('hasAttachments', False)]
            high_importance = [e for e in emails if e.get('importance') == 'high']
            
            # Agrupa remetentes
            senders = {}
            for email in emails:
                sender = email.get('from', {}).get('emailAddress', {}).get('address', 'Desconhecido')
                senders[sender] = senders.get(sender, 0) + 1
            
            # Top 5 remetentes
            top_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Monta contexto
            context = f"""CONTEXTO DA CAIXA DE ENTRADA (Últimos 3 dias):

ESTATÍSTICAS:
- Total de emails: {total_emails}
- Não lidos: {len(unread_emails)}
- Com anexos: {len(with_attachments)}
- Marcados como importantes: {len(high_importance)}

TOP 5 REMETENTES:
"""
            for sender, count in top_senders:
                context += f"- {sender}: {count} email(s)\n"
            
            # Adiciona últimos 10 assuntos
            context += "\nÚLTIMOS 10 EMAILS:\n"
            for idx, email in enumerate(emails[:10], 1):
                subject = email.get('subject', 'Sem assunto')[:60]
                sender = email.get('from', {}).get('emailAddress', {}).get('address', 'Desconhecido')
                read_status = "✓" if email.get('isRead') else "✗"
                context += f"{idx}. [{read_status}] {subject} (de: {sender})\n"
            
            return context
        
        except Exception as e:
            logger.error(f"Erro ao obter contexto de emails: {e}")
            return "Não foi possível obter informações dos emails no momento."
    
    def chat(self, user_message: str) -> str:
        """
        Processa mensagem do usuário e retorna resposta da IA.
        
        Args:
            user_message: Pergunta do usuário
        
        Returns:
            Resposta da IA
        """
        try:
            # Adiciona mensagem do usuário no histórico
            self.conversation_history.append({
                'role': 'user',
                'content': user_message
            })
            
            # Busca contexto dos emails
            email_context = self._get_email_context()
            
            # Monta prompt para a IA
            system_prompt = f"""Você é um assistente inteligente que ajuda o usuário a gerenciar seus emails.

{email_context}

INSTRUÇÕES:
- Responda de forma clara, objetiva e amigável
- Use o contexto dos emails para responder perguntas
- Se não souber algo, seja honesto
- Sugira ações úteis quando apropriado
- Mantenha respostas concisas (máximo 200 palavras)

EXEMPLOS DE PERGUNTAS:
- "Quantos emails não lidos eu tenho?"
- "Quem mais me enviou emails recentemente?"
- "Tenho algum email importante?"
- "Me fale sobre os emails de hoje"
- "Preciso responder algum email urgente?"
"""
            
            # Prepara mensagens para a IA
            messages = [
                {'role': 'system', 'content': system_prompt}
            ] + self.conversation_history[-5:]  # Últimas 5 mensagens
            
            # Chama a IA
            response = self.ai_service._call_ollama_chat(messages)
            
            # Adiciona resposta no histórico
            self.conversation_history.append({
                'role': 'assistant',
                'content': response
            })
            
            logger.info(f"Chat - Pergunta: '{user_message[:50]}...', Resposta gerada")
            
            return response
        
        except Exception as e:
            logger.error(f"Erro no chat: {e}")
            return "Desculpe, tive um problema ao processar sua pergunta. Tente novamente."
    
    def get_suggested_questions(self) -> list:
        """
        Retorna lista de perguntas sugeridas.
        """
        return [
            "Quantos emails não lidos eu tenho?",
            "Quem mais me enviou emails esta semana?",
            "Tenho algum email importante ou urgente?",
            "Me fale sobre os emails de hoje",
            "Há emails com anexos?",
            "Preciso responder algum email?",
            "Qual foi o último email que recebi?",
            "Resuma minha caixa de entrada",
        ]
    
    def clear_history(self):
        """Limpa histórico da conversa."""
        self.conversation_history = []
        logger.info("Histórico de chat limpo")
    
    def execute_command(self, command: str) -> str:
        """
        Executa comandos especiais do chat.
        
        Args:
            command: Comando especial (ex: '/resumo', '/help')
        
        Returns:
            Resultado do comando
        """
        if command == '/resumo':
            summary = self.report_service.get_today_summary()
            return f"""📊 RESUMO RÁPIDO

Total hoje: {summary['total']}
Com anexos: {summary['with_attachments']}
Sem anexos: {summary['without_attachments']}"""
        
        elif command == '/help':
            return """🤖 COMANDOS DISPONÍVEIS

/resumo - Resumo rápido de hoje
/limpar - Limpa histórico de chat
/sugestões - Mostra perguntas sugeridas
/sair - Volta ao menu

Ou faça perguntas normalmente!"""
        
        elif command == '/limpar':
            self.clear_history()
            return "✅ Histórico de conversa limpo!"
        
        elif command == '/sugestões':
            suggestions = self.get_suggested_questions()
            result = "💡 PERGUNTAS SUGERIDAS:\n\n"
            for idx, q in enumerate(suggestions, 1):
                result += f"{idx}. {q}\n"
            return result
        
        else:
            return f"❌ Comando '{command}' não reconhecido. Digite /help para ver comandos."
