import ollama
from app.config.settings import OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_TIMEOUT
from app.utils.logger import get_logger

logger = get_logger()


class AIService:
    """
    Serviço de IA usando Ollama com Llama 3.2 3B.
    Focado em classificação e análise simples de emails.
    """
    
    def __init__(self):
        self.model = OLLAMA_MODEL
        self.host = OLLAMA_HOST
        self.timeout = OLLAMA_TIMEOUT
        logger.info(f"AI Service inicializado com modelo: {self.model}")
    
    def _call_ollama(self, prompt: str) -> str:
        """
        Chama o Ollama de forma segura com tratamento de erros.
        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.3,  # Mais determinístico
                    'num_predict': 150,  # Limita resposta
                }
            )
            return response['message']['content'].strip()
        
        except Exception as e:
            logger.error(f"Erro ao chamar Ollama: {e}")
            return None
    
    def _call_ollama_chat(self, messages: list) -> str:
        """
        Chama Ollama com histórico de conversa.
        
        Args:
            messages: Lista de mensagens [{'role': 'user/assistant', 'content': '...'}]
        
        Returns:
            Resposta da IA
        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    'temperature': 0.7,  # Mais conversacional
                    'num_predict': 300,  # Permite respostas maiores
                }
            )
            return response['message']['content'].strip()
        
        except Exception as e:
            logger.error(f"Erro ao chamar Ollama chat: {e}")
            return "Desculpe, tive um problema ao processar sua mensagem."
    
    def classify_urgency(self, email: dict) -> str:
        """
        Classifica a urgência do email em: ALTA, MÉDIA, BAIXA.
        
        Args:
            email: Dicionário com dados do email (subject, from, body preview)
        
        Returns:
            String com classificação: "ALTA", "MÉDIA" ou "BAIXA"
        """
        try:
            # Limita o contexto para não sobrecarregar o modelo
            subject = email.get('subject', '')[:200]
            sender = email.get('from', {}).get('emailAddress', {}).get('address', 'desconhecido')
            body_preview = email.get('bodyPreview', '')[:300]
            
            prompt = f"""Analise este email e classifique sua urgência em ALTA, MÉDIA ou BAIXA.

ALTA: Requer ação imediata, prazos curtos, problemas críticos
MÉDIA: Importante mas pode aguardar algumas horas
BAIXA: Informativo, sem pressa

Email:
De: {sender}
Assunto: {subject}
Prévia: {body_preview}

Responda APENAS com uma palavra: ALTA, MÉDIA ou BAIXA."""

            logger.debug(f"Classificando email: {subject[:50]}...")
            
            result = self._call_ollama(prompt)
            
            if result:
                # Normaliza a resposta
                urgency = result.upper().strip()
                
                # Validação
                if urgency in ['ALTA', 'MÉDIA', 'BAIXA']:
                    logger.info(f"Email classificado como: {urgency}")
                    return urgency
                else:
                    logger.warning(f"Resposta inesperada do modelo: {result}. Usando MÉDIA como padrão.")
                    return "MÉDIA"
            else:
                logger.warning("Ollama não retornou resposta. Usando MÉDIA como padrão.")
                return "MÉDIA"
        
        except Exception as e:
            logger.error(f"Erro ao classificar urgência: {e}")
            return "MÉDIA"  # Fallback seguro
    
    def suggest_reply(self, email: dict) -> str:
        """
        Gera sugestão de resposta genérica (placeholder por enquanto).
        Será implementado em sprints futuras.
        """
        urgency = self.classify_urgency(email)
        
        if urgency == "ALTA":
            return (
                "Olá,\n\n"
                "Recebi seu email e vou priorizar esta demanda.\n"
                "Retorno com mais detalhes em breve.\n\n"
                "Atenciosamente"
            )
        else:
            return (
                "Olá,\n\n"
                "Obrigado pelo contato. Vou analisar e retorno em breve.\n\n"
                "Atenciosamente"
            )
