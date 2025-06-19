# console_styler.py
import sys

class ConsoleStyler:
    """A utility class to style console output with colors and emojis using ANSI escape codes."""
    
    # ANSI escape codes for colors
    COLORS = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"  # Code to reset all styling
    }
    
    # Emojis for different message contexts
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
        """Initializes the styler. Colors are disabled on Windows for compatibility."""
        # The 'colorama' library would be needed for a cross-platform solution.
        self.use_colors = sys.platform != "win32"

    def _style(self, text, color=None, bold=False):
        """
        Applies ANSI styling to text if supported.
        
        Args:
            text: The string to style.
            color: The name of the color to apply.
            bold: Whether to apply bold styling.
            
        Returns:
            The styled string.
        """
        if not self.use_colors:
            return text
        
        style_str = ""
        if color and color in self.COLORS:
            style_str += self.COLORS[color]
        if bold:
            style_str += "\033[1m"  # ANSI code for bold
            
        return f"{style_str}{text}{self.COLORS['reset']}"

    def print(self, message, emoji_key=None, color=None, bold=False):
        """Prints a styled message to the console."""
        emoji = self.EMOJIS.get(emoji_key, "")
        styled_message = self._style(message, color, bold)
        print(f"{emoji} {styled_message}".strip())

    def print_title(self, message, color="magenta", bold=True):
        """Prints a decorative title with a border."""
        styled_title = self._style(f" {message} ", color=color, bold=bold)
        border = self._style("═" * (len(message) + 4), color=color)
        print(f"\n{border}\n{self.EMOJIS.get('rocket', '🚀')} {styled_title} {self.EMOJIS.get('rocket', '🚀')}\n{border}")

    def print_separator(self, length=50):
        """Prints a horizontal separator line."""
        print(self._style("─" * length, color="cyan"))
        
    def get_input(self, prompt_message):
        """Gets user input with a styled prompt."""
        emoji = self.EMOJIS.get("prompt", ">")
        prompt = self._style(f"{prompt_message}: ", color="yellow", bold=True)
        return input(f"{emoji} {prompt}")

# Global instance to be imported and used in other modules
styler = ConsoleStyler()