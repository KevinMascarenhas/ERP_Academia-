# Serviço de logging para registrar ações importantes do sistema. Registra em arquivo log.txt com timestamp.

from datetime import datetime
from pathlib import Path


class Logger:
    # Serviço de logging para registrar ações importantes do sistema."""
    
    def __init__(self, log_file="log.txt"):
        self.log_file = Path(log_file)
        # Garante que o arquivo existe
        if not self.log_file.exists():
            self.log_file.touch()
    
    def registrar(self, usuario: str, acao: str):
        # Registra uma ação no arquivo de log.
        
        # Formato: [YYYY-MM-DD HH:MM:SS] usuario - Ação descritiva
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha_log = f"[{timestamp}] {usuario} - {acao}\n"
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(linha_log)
        except Exception as e:
            print(f"Erro ao registrar log: {e}")
    
    def listar_logs(self):
        try:
            if self.log_file.exists():
                with open(self.log_file, "r", encoding="utf-8") as f:
                    return f.read()
            return "Nenhum log registrado."
        except Exception as e:
            return f"Erro ao ler logs: {e}"
    
    def limpar_logs(self):
        try:
            self.log_file.write_text("")
            return True
        except Exception as e:
            print(f"Erro ao limpar logs: {e}")
            return False
