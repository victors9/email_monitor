from app.config.settings import *
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.services.calendar_service import CalendarService
from app.services.ai_service import AIService
from app.utils.heartbeat import Heartbeat
from app.agent import EmailMonitorAgent


def main():
    try:
        auth = AuthService(TENANT_ID, CLIENT_ID, SCOPES)
        token = auth.get_token()

        email_service = EmailService(token)
        calendar_service = CalendarService(token)
        ai_service = AIService()
        heartbeat = Heartbeat(HEARTBEAT_MINUTES)

        agent = EmailMonitorAgent(
            email_service,
            calendar_service,
            ai_service,
            heartbeat
        )

        agent.run()

    except KeyboardInterrupt:
        print("\n🛑 Execução interrompida pelo usuário. Finalizando agente...")
    except Exception as e:
        print(f"\n❌ Erro fatal na inicialização do agente: {e}")


if __name__ == "__main__":
    main()