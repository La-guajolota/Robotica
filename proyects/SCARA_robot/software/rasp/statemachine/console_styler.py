# console_styler.py
import sys

class ConsoleStyler:
    """Una clase de utilidad para estilizar la salida de la consola con colores y emojis."""
    
    # Códigos de escape ANSI para colores
    COLORS = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }
    
    # Emojis para diferentes contextos
    EMOJIS = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "system": "⚙️",
        "plc": "🔌",
        "camera": "📷",
        "scara": "🤖",
        "box": "📦",
        "idle": "😴",
        "data": "📩",
        "rocket": "🚀",
        "bye": "👋",
        "prompt": "👉",
        "play": "▶️",
        "stop": "⏹️",
        "connect": "🔗",
        "disconnect": "💔",
        "loop": "🔄",
        "state": "🏷️",
        "debug": "🐞"
    }

    def __init__(self):
        # Para una solución compatible con Windows, se usaría la librería 'colorama'.
        self.use_colors = sys.platform != "win32"

    def _style(self, text, color=None, bold=False):
        """Aplica estilo ANSI al texto si es compatible."""
        if not self.use_colors:
            return text
        
        style_str = ""
        if color and color in self.COLORS:
            style_str += self.COLORS[color]
        if bold:
            style_str += "\033[1m"
            
        return f"{style_str}{text}{self.COLORS['reset']}"

    def print(self, message, emoji_key=None, color=None, bold=False):
        """Imprime un mensaje estilizado en la consola."""
        emoji = self.EMOJIS.get(emoji_key, "")
        styled_message = self._style(message, color, bold)
        print(f"{emoji} {styled_message}".strip())

    def print_title(self, message, color="magenta", bold=True):
        """Imprime un título con un borde decorativo."""
        styled_title = self._style(f" {message} ", color=color, bold=bold)
        border = self._style("═" * (len(message) + 4), color=color)
        print(f"\n{border}\n{self.EMOJIS.get('rocket', '🚀')} {styled_title} {self.EMOJIS.get('rocket', '🚀')}\n{border}")

    def print_separator(self, length=50):
        """Imprime una línea separadora."""
        print(self._style("─" * length, color="cyan"))
        
    def get_input(self, prompt_message):
        """Obtiene la entrada del usuario con un indicador estilizado."""
        emoji = self.EMOJIS.get("prompt", ">")
        prompt = self._style(f"{prompt_message}: ", color="yellow", bold=True)
        return input(f"{emoji} {prompt}")

# Instancia global para ser importada en otros módulos
styler = ConsoleStyler()