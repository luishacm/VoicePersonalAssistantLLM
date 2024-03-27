import subprocess
import platform
import re
import string
import sys
import os
from typing import NoReturn
import base64


commands = {
    "abrir": ["abrir", "abri", "abre", "abra", "abriu", "abrindo", "aberto", 
              "destravar", "destrave", "destravou", "destravando", 
              "iniciar", "inicie", "iniciou", "iniciando", 
              "ativar", "ative", "ativou", "ativando", 
              "lançar", "lançou", "lançando", 
              "carregar", "carregue", "carregou", "carregando"],
    
    "fechar": ["fechar", "fecha", "feche", "fechou", "fechando", "fechado", 
               "encerrar", "encerra", "encerre", "encerrado", "encerrando", "encerraram", 
               "desligar", "desligue", "desligou", "desligando", "desliga", "desligui"
               "sair", "saia", "saiu", "saindo", 
               "cancelar", "cancele", "cancelou", "cancelado", "cancelando", 
               "finalizar", "finalize", "finalizou", "finalizando", 
               "desativar", "desative", "desativou", "desativando"],
    
    "pesquisar": ["pesquisar", "pesquise", "pesquisi", "pesquisou", "pesquisa", "pesquisando", 
                  "buscar", "busque", "busqui", "busca" "buscou", "buscando", 
                  "procurar", "procure", "procurou", "procurando", 
                  "achar", "ache", "achou", "achando", "acha", "achi", 
                  "encontrar", "encontre", "encontra", "encontri", "encontrou", "encontrando", 
                  "rastrear", "rastreie", "rastreia", "rastrea", "rastreou", "rastreando", 
                  "explorar", "explora", "explori", "explore", "explorou", "explorando"]
}
applications = {
    "spotify": ["spotify", "spotfy", "espotify", "spotifai", "spotfai"]
}

class ExternalCommands:
   
    @classmethod
    def execute_commands(cls, message_normalized):
        message_normalized_split = message_normalized.split(" ")
        first_3_words = message_normalized_split[:4]
        first_5_words = message_normalized_split[:6]
        if any(i in commands["abrir"] for i in first_3_words):
            if any(i in first_5_words for i in applications["spotify"]):
                cls.abrir_spotify()
                return message_normalized
            elif "youtube" in first_5_words:
                cls.abrir_youtube()
                return message_normalized
            elif "word" in first_5_words:
                cls.abrir_word()
                return message_normalized
            elif "steam" in first_5_words:
                cls.abrir_steam()
                return message_normalized
            elif "stream" in first_5_words:
                cls.abrir_stremio()
                return message_normalized
            elif "netflix" in first_5_words:
                cls.abrir_netflix()
                return message_normalized
            elif "prime" in first_5_words:
                cls.abrir_prime_video()
                return message_normalized
            elif "rocket" in first_5_words:
                cls.abrir_rocket_league()
                return message_normalized
            
        elif any(i in commands["pesquisar"] for i in first_3_words):
            if "youtube" in first_5_words:
                cls.pesquisar_youtube(message_normalized)
                return message_normalized
            
            elif "google" in first_5_words:
                cls.pesquisar_google(message_normalized)
                return message_normalized
            
            elif "cifra" in first_5_words:
                cls.pesquisar_cifraclub(message_normalized)
                return message_normalized

        elif any(i in commands["fechar"] for i in first_3_words):
            if "rocket" in first_5_words:
                cls.fechar_rocket_league()
                return message_normalized

            elif "luma" in first_5_words:
                cls.desligar_script()

            elif "firefox" in first_5_words:
                cls.fechar_firefox()
                return message_normalized

            elif "gather" in first_5_words:
                cls.fechar_gather()
                return message_normalized

            elif "discord" in first_5_words:
                cls.fechar_discord()
                return message_normalized
                        
            elif "desligar" in first_3_words and "computador" in first_3_words:
                cls.desligar_computador()

        elif "reiniciar computador" in first_3_words:
            cls.reiniciar_computador()

        else:
            return False

    
    @classmethod
    def normalize_message(cls, message: str) -> str:
        """
        Normalizes a message by converting to lowercase and removing special characters.

        Parameters:
        message (str): The message to be normalized.

        Returns:
        str: The normalized message.
        """
        message = message.lower()
        message = re.sub(f'[{string.punctuation}]+', '', message)
        return message.strip()

    @classmethod
    def abrir_spotify(cls):
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen("start spotify", shell=True)
        elif os_type == "Linux":
            subprocess.Popen(["xdg-open", "spotify"])
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Spotify"])
        else:
            print("Operating system not supported.")

    @classmethod
    def abrir_youtube(cls):
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen('start firefox "https://www.youtube.com"', shell=True)
        elif os_type == "Linux":
            subprocess.Popen(["firefox", "https://www.youtube.com"])
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Firefox", "https://www.youtube.com"])
        else:
            print("Operating system not supported.")

    @classmethod
    def pesquisar_youtube(cls, message: str):
        parts = message.split("youtube", 1)
        if len(parts) > 1:
            youtube_query = parts[1].strip()
        else:
            youtube_query = ""

        youtube_query = f'"https://www.youtube.com/results?search_query={youtube_query}"'
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen(f'start firefox {youtube_query}', shell=True)
        elif os_type == "Linux":
            subprocess.Popen(["firefox", youtube_query])
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Firefox", youtube_query])
        else:
            print("Operating system not supported.")

    @classmethod
    def pesquisar_cifraclub(cls, message: str):
        parts = message.split("club", 1)
        if len(parts) > 1:
            cifra_query = parts[1].strip()
        else:
            parts = message.split("clube", 1)
            if len(parts) > 1:
                cifra_query = parts[1].strip()
            else:
                parts = message.split("cifra", 1)
                if len(parts) > 1:
                    cifra_query = parts[1].strip()
                else:
                    cifra_query = message

        cifra_query = f'"https://www.cifraclub.com.br/?q={cifra_query}"'
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen(f'start firefox {cifra_query}', shell=True)
        elif os_type == "Linux":
            subprocess.Popen(["firefox", cifra_query])
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Firefox", cifra_query])
        else:
            print("Operating system not supported.")

    @classmethod
    def pesquisar_google(cls, message: str):
        parts = message.split("google", 1)
        if len(parts) > 1:
            google_query = parts[1].strip()
        else:
            google_query = ""
        url = f"https://www.google.com/search?q={google_query}"
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen(f'start firefox "{url}"', shell=True)
        elif os_type == "Linux":
            subprocess.Popen(["firefox", url])
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Firefox",  url])
        else:
            print("Operating system not supported.")

    @classmethod
    def abrir_word(cls):
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen("start winword", shell=True)
        elif os_type == "Linux":
            print("Microsoft Word is not natively supported on Linux.")
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Microsoft Word"])
        else:
            print("Operating system not supported.")

    @classmethod
    def abrir_steam(cls):
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen(r'"C:/Program Files (x86)/Steam/Steam.exe"', shell=True)
        elif os_type == "Linux":
            subprocess.Popen(["steam"])
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Steam"])
        else:
            print("Operating system not supported.")

    @classmethod
    def abrir_stremio(cls):
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen(r'"C:/Users/Luis/AppData/Local/Programs/LNV/Stremio-4/stremio.exe"', shell=True)
        elif os_type == "Linux":
            subprocess.Popen(["stremio"])
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Stremio"])
        else:
            print("Operating system not supported.")


    @classmethod
    def abrir_netflix(cls):
        """
        Opens Netflix in the Firefox web browser.

        This method checks the operating system of the user and opens Netflix
        in Firefox according to the appropriate command for the OS.
        """
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen('start firefox "https://www.netflix.com"', shell=True)
        elif os_type == "Linux":
            subprocess.Popen(["firefox", "https://www.netflix.com"])
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Firefox", "https://www.netflix.com"])
        else:
            print("Operating system not supported.")

    @classmethod
    def abrir_prime_video(cls):
        """
        Opens Amazon Prime Video in the Firefox web browser.

        This method checks the operating system of the user and opens Amazon Prime Video
        in Firefox according to the appropriate command for the OS.
        """
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen('start firefox "https://www.primevideo.com"', shell=True)
        elif os_type == "Linux":
            subprocess.Popen(["firefox", "https://www.primevideo.com"])
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Firefox", "https://www.primevideo.com"])
        else:
            print("Operating system not supported.")

    @classmethod
    def abrir_rocket_league(cls):
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen(r'"C:/Program Files (x86)/Steam/steamapps/common/rocketleague/Binaries/Win64/RocketLeague.exe"', shell=True)
        elif os_type == "Linux":
            subprocess.Popen(["Rocket League"])
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Rocket League"])
        else:
            print("Operating system not supported.")

    @classmethod
    def fechar_rocket_league(cls):
        """
        Closes Rocket League on the system using taskkill on Windows or pkill on Unix-like systems.
        """
        os_type = platform.system()
        if os_type == "Windows":
            subprocess.Popen("taskkill /f /im RocketLeague.exe", shell=True)
        elif os_type in ["Linux", "Darwin"]:  # Linux and macOS
            subprocess.Popen(["pkill", "-f", "RocketLeague"])
        else:
            print("Operating system not supported.")

    @classmethod
    def desligar_script(cls):
        """
        Terminates the running script.
        """
        print("Desligando o script...")
        sys.exit()


    @classmethod
    def fechar_firefox(cls):
        """
        Closes all instances of the Firefox browser.
        """
        os_type = platform.system()
        if os_type == "Windows":
            # TASKKILL é o comando para matar um processo no Windows.
            subprocess.run(["taskkill", "/F", "/IM", "firefox.exe"], check=True)
        elif os_type == "Linux" or os_type == "Darwin":
            # pkill enviará o sinal SIGTERM para todos os processos com o nome 'firefox'.
            subprocess.run(["pkill", "firefox"], check=True)
        else:
            print("Operating system not supported.")

    @classmethod
    def fechar_gather(cls):
        """
        Closes the Gather application.
        """
        os_type = platform.system()
        if os_type == "Windows":
            # TASKKILL é o comando para matar um processo no Windows.
            subprocess.run(["taskkill", "/F", "/IM", "Gather.exe"], check=True)
        elif os_type == "Linux" or os_type == "Darwin":
            # pkill enviará o sinal SIGTERM para todos os processos com o nome 'Gather'.
            subprocess.run(["pkill", "-f", "Gather"], check=True)
        else:
            print("Operating system not supported.")

    @classmethod
    def fechar_discord(cls):
        """
        Closes the Discord application.
        """
        os_type = platform.system()
        if os_type == "Windows":
            # TASKKILL é o comando para matar um processo no Windows.
            subprocess.run(["taskkill", "/F", "/IM", "Discord.exe"], check=True)
        elif os_type == "Linux" or os_type == "Darwin":
            # pkill enviará o sinal SIGTERM para todos os processos com o nome 'Discord'.
            subprocess.run(["pkill", "Discord"], check=True)
        else:
            print("Operating system not supported.")

    @classmethod
    def reiniciar_computador(cls):
        """Reinicia o computador."""
        os_type = platform.system()
        if os_type == "Windows":
            os.system("shutdown /r /t 1")
        elif os_type == "Linux" or os_type == "Darwin":  # Darwin é o sistema subjacente ao macOS
            os.system("sudo shutdown -r now")
        else:
            print("Sistema operacional não suportado.")
            sys.exit(1)

    @classmethod
    def desligar_computador(cls):
        """Desliga o computador."""
        os_type = platform.system()
        if os_type == "Windows":
            os.system("shutdown /s /t 1")
        elif os_type == "Linux" or os_type == "Darwin":  # Darwin é o sistema subjacente ao macOS
            os.system("sudo shutdown -h now")
        else:
            print("Sistema operacional não suportado.")
            sys.exit(1)

    @classmethod
    def run_gpt_command(cls, voice_transcription: str):

        cls.run_code()
            
    @classmethod
    def run_code(cls, code: str) -> NoReturn:
        """
        Run the provided Python code in a new command prompt window and close it after execution.

        Args:
            code (str): A string containing Python code to be executed.
        """
        # Base64 encode the Python code
        b64_code = base64.b64encode(code.encode()).decode()

        # Construct the command to decode and run the Python code
        python_command = f'python -c "import base64; exec(base64.b64decode(\'{b64_code}\'))"'

        # Open a new command prompt window, run the Python command, and close it after execution
        subprocess.Popen(f'start cmd /C "{python_command}"', shell=True)
