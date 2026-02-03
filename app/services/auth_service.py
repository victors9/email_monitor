import msal
import pickle
from pathlib import Path
from app.utils.logger import get_logger

logger = get_logger()


class AuthService:
    """
    Serviço de autenticação com Microsoft usando MSAL.
    Implementa cache de token para evitar re-autenticação constante.
    """
    
    TOKEN_CACHE_FILE = ".token_cache"
    
    def __init__(self, tenant_id: str, client_id: str, scopes: list):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.scopes = scopes
        
        self.app = msal.PublicClientApplication(
            client_id=client_id,
            authority=f"https://login.microsoftonline.com/{tenant_id}"
        )
        
        logger.info("AuthService inicializado")
    
    def _load_token_cache(self) -> dict:
        """Carrega token do cache se existir."""
        cache_path = Path(self.TOKEN_CACHE_FILE)
        
        if cache_path.exists():
            try:
                with open(cache_path, 'rb') as f:
                    cached = pickle.load(f)
                    logger.info("Token carregado do cache")
                    return cached
            except Exception as e:
                logger.warning(f"Erro ao carregar cache de token: {e}")
        
        return None
    
    def _save_token_cache(self, token_data: dict):
        """Salva token no cache."""
        try:
            with open(self.TOKEN_CACHE_FILE, 'wb') as f:
                pickle.dump(token_data, f)
                logger.info("Token salvo no cache")
        except Exception as e:
            logger.error(f"Erro ao salvar cache de token: {e}")
    
    def get_token(self) -> str:
        """
        Obtém token de acesso. Tenta usar cache primeiro,
        senão solicita nova autenticação via device flow.
        
        Returns:
            Access token válido
        """
        # Tenta obter token das contas em cache
        accounts = self.app.get_accounts()
        
        if accounts:
            logger.info("Tentando autenticação silenciosa...")
            result = self.app.acquire_token_silent(self.scopes, account=accounts[0])
            
            if result and "access_token" in result:
                logger.info("Token obtido silenciosamente (refresh)")
                return result["access_token"]
        
        # Se não conseguiu silenciosamente, faz device flow
        logger.info("Iniciando device flow para autenticação...")
        
        try:
            flow = self.app.initiate_device_flow(scopes=self.scopes)
            
            if "user_code" not in flow:
                raise Exception(f"Falha ao criar device flow: {flow.get('error_description')}")
            
            print("\n" + "="*60)
            print(flow["message"])
            print("="*60 + "\n")
            
            result = self.app.acquire_token_by_device_flow(flow)
            
            if "access_token" in result:
                logger.info("Autenticação via device flow bem-sucedida")
                self._save_token_cache(result)
                return result["access_token"]
            else:
                error_msg = result.get('error_description', 'Erro desconhecido')
                raise Exception(f"Falha na autenticação: {error_msg}")
        
        except Exception as e:
            logger.error(f"Erro durante autenticação: {e}")
            raise
