from decouple import config

# Microsoft Azure AD Configuration
TENANT_ID = config('TENANT_ID')
CLIENT_ID = config('CLIENT_ID')

# Scopes necessários para o Microsoft Graph
SCOPES = [
    "Mail.Read",
    "Mail.ReadWrite",
    "Calendars.Read"
]

# Email Monitor Settings
CHECK_INTERVAL_SECONDS = config('CHECK_INTERVAL_SECONDS', default=30, cast=int)
HEARTBEAT_MINUTES = config('HEARTBEAT_MINUTES', default=20, cast=int)
MAX_EMAILS_PER_CHECK = config('MAX_EMAILS_PER_CHECK', default=5, cast=int)

# Ollama Configuration
OLLAMA_MODEL = config('OLLAMA_MODEL', default='llama3.2:3b')
OLLAMA_HOST = config('OLLAMA_HOST', default='http://localhost:11434')
OLLAMA_TIMEOUT = config('OLLAMA_TIMEOUT', default=30, cast=int)

# Logging
LOG_LEVEL = config('LOG_LEVEL', default='INFO')
LOG_FILE = config('LOG_FILE', default='logs/email_agent.log')
