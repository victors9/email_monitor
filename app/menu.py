import sys
from app.utils.logger import get_logger

logger = get_logger()


class MenuSystem:
    """
    Sistema de menu interativo para o Email Monitor Agent.
    """
    
    def __init__(self, email_service, user_service, report_service, chat_service):
        self.email_service = email_service
        self.user_service = user_service
        self.report_service = report_service
        self.chat_service = chat_service
        logger.info("MenuSystem inicializado")
    
    def clear_screen(self):
        """Limpa a tela (funciona no Linux/Mac/Windows)."""
        import os
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self):
        """Imprime cabeçalho do menu."""
        self.clear_screen()
        print("\n" + "=" * 80)
        print("🤖 EMAIL MONITOR AGENT - MENU PRINCIPAL")
        print("=" * 80)
    
    def print_menu(self):
        """Imprime opções do menu."""
        print("\nESCOLHA UMA OPÇÃO:\n")
        print("1️⃣  Resumo de Emails Recebidos Hoje")
        print("    └─ Visualiza emails do dia com informação de anexos\n")
        
        print("2️⃣  Emails Sem Resposta (Últimos 7 dias)")
        print("    └─ Lista emails que você ainda não respondeu\n")
        
        print("3️⃣  Status de Usuários da Organização")
        print("    └─ Mostra presença (online/offline/reunião) de todos\n")
        
        print("4️⃣  Iniciar Monitoramento Automático")
        print("    └─ Inicia o agente em modo contínuo (loop)\n")
        
        print("5️⃣  Chat com o Agente (IA)")
        print("    └─ Converse com a IA sobre seus emails\n")
        
        print("0️⃣  Sair")
        print("\n" + "-" * 80)
    
    def option_1_today_summary(self):
        """Opção 1: Resumo de emails de hoje."""
        logger.info("Executando: Resumo de emails de hoje")
        
        print("\n🔄 Buscando emails recebidos hoje...")
        summary = self.report_service.get_today_summary()
        
        formatted = self.report_service.format_today_summary(summary)
        print(formatted)
        
        self.pause()
    
    def option_2_unanswered_emails(self):
        """Opção 2: Emails sem resposta."""
        logger.info("Executando: Emails sem resposta")
        
        print("\n🔄 Buscando emails sem resposta dos últimos 7 dias...")
        print("⏳ (Isso pode demorar alguns segundos...)")
        
        unanswered = self.report_service.get_unanswered_emails(days=7)
        
        formatted = self.report_service.format_unanswered_emails(unanswered)
        print(formatted)
        
        self.pause()
    
    def option_3_user_presence(self):
        """Opção 3: Status de usuários."""
        logger.info("Executando: Status de usuários")
        
        print("\n🔄 Buscando status dos usuários...")
        print("⏳ (Isso pode demorar alguns segundos...)")
        
        users = self.user_service.get_all_users_with_presence(max_users=50)
        
        print("\n" + "=" * 80)
        print("👥 STATUS DE USUÁRIOS DA ORGANIZAÇÃO")
        print("=" * 80)
        
        if not users:
            print("\n⚠️  Não foi possível buscar usuários.")
        else:
            # Agrupa por status
            status_groups = {}
            for user in users:
                status = user['status_description']
                if status not in status_groups:
                    status_groups[status] = []
                status_groups[status].append(user)
            
            # Imprime estatísticas
            print(f"\n📊 Total de usuários: {len(users)}")
            print("\nResumo por status:")
            for status, group in sorted(status_groups.items()):
                emoji = group[0]['emoji']
                print(f"  {emoji} {status}: {len(group)} usuário(s)")
            
            # Imprime tabela detalhada
            print("\n" + "-" * 80)
            print("DETALHES:")
            print("-" * 80)
            
            formatted = self.user_service.format_users_table(users)
            print(formatted)
        
        self.pause()
    
    def option_4_start_monitoring(self):
        """Opção 4: Inicia monitoramento automático."""
        logger.info("Executando: Monitoramento automático")
        
        print("\n" + "=" * 80)
        print("🚀 INICIANDO MONITORAMENTO AUTOMÁTICO")
        print("=" * 80)
        print("\n⚠️  O agente vai rodar em loop contínuo.")
        print("⚠️  Pressione Ctrl+C para voltar ao menu.\n")
        
        confirm = input("Deseja continuar? (s/n): ").strip().lower()
        
        if confirm == 's':
            # Importa e executa o agente
            from app.agent import EmailMonitorAgent
            from app.services.ai_service import AIService
            from app.utils.heartbeat import Heartbeat
            from app.config.settings import CHECK_INTERVAL_SECONDS, HEARTBEAT_MINUTES
            
            ai_service = AIService()
            heartbeat = Heartbeat(HEARTBEAT_MINUTES)
            
            agent = EmailMonitorAgent(
                email_service=self.email_service,
                calendar_service=None,  # Opcional
                ai_service=ai_service,
                heartbeat=heartbeat,
                check_interval=CHECK_INTERVAL_SECONDS
            )
            
            try:
                agent.run()
            except KeyboardInterrupt:
                print("\n\n⚠️  Monitoramento interrompido. Retornando ao menu...")
                logger.info("Monitoramento interrompido pelo usuário")
        else:
            print("\n❌ Operação cancelada.")
        
        self.pause()
    
    def option_5_chat(self):
        """Opção 5: Chat interativo com IA."""
        logger.info("Executando: Chat com IA")
        
        print("\n" + "=" * 80)
        print("💬 CHAT COM O AGENTE")
        print("=" * 80)
        print("\n🤖 Olá! Sou seu assistente inteligente.")
        print("📧 Posso responder perguntas sobre seus emails.\n")
        print("💡 Dica: Digite /help para ver comandos especiais")
        print("💡 Digite /sugestões para ver perguntas exemplo")
        print("💡 Digite /sair para voltar ao menu\n")
        print("-" * 80)
        
        while True:
            try:
                # Lê pergunta do usuário
                user_input = input("\n👤 Você: ").strip()
                
                # Verifica se quer sair
                if user_input.lower() in ['/sair', 'sair', 'exit', 'quit']:
                    print("\n👋 Voltando ao menu principal...")
                    break
                
                # Ignora mensagens vazias
                if not user_input:
                    continue
                
                # Verifica se é comando especial
                if user_input.startswith('/'):
                    response = self.chat_service.execute_command(user_input)
                    print(f"\n🤖 Agente: {response}")
                    continue
                
                # Processa pergunta com IA
                print("\n🤖 Agente: ", end="", flush=True)
                print("⏳ Pensando...", end="\r", flush=True)
                
                response = self.chat_service.chat(user_input)
                
                print("🤖 Agente: " + " " * 20)  # Limpa "Pensando..."
                print(f"🤖 Agente: {response}")
            
            except KeyboardInterrupt:
                print("\n\n⚠️  Chat interrompido.")
                confirm = input("Deseja voltar ao menu? (s/n): ").strip().lower()
                if confirm == 's':
                    break
            
            except Exception as e:
                logger.error(f"Erro no chat: {e}")
                print(f"\n❌ Erro: {e}")
                print("Tente novamente ou digite /sair para voltar ao menu.")
        
        self.pause()
    
    def pause(self):
        """Pausa para o usuário ler a saída."""
        input("\n\nPressione ENTER para voltar ao menu...")
    
    def run(self):
        """
        Loop principal do menu.
        """
        while True:
            try:
                self.print_header()
                self.print_menu()
                
                choice = input("Digite sua opção: ").strip()
                
                if choice == '1':
                    self.option_1_today_summary()
                
                elif choice == '2':
                    self.option_2_unanswered_emails()
                
                elif choice == '3':
                    self.option_3_user_presence()
                
                elif choice == '4':
                    self.option_4_start_monitoring()
                
                elif choice == '5':
                    self.option_5_chat()
                
                elif choice == '0':
                    print("\n👋 Encerrando... Até logo!")
                    logger.info("Menu encerrado pelo usuário")
                    sys.exit(0)
                
                else:
                    print("\n❌ Opção inválida! Tente novamente.")
                    self.pause()
            
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupção detectada.")
                confirm = input("Deseja realmente sair? (s/n): ").strip().lower()
                if confirm == 's':
                    print("\n👋 Até logo!")
                    sys.exit(0)
            
            except Exception as e:
                logger.error(f"Erro no menu: {e}", exc_info=True)
                print(f"\n❌ Erro: {e}")
                self.pause()
