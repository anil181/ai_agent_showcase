import sys

class Formatter:
    @staticmethod
    def print_status(message: str):
        """Prints a status message with a prefix."""
        print("[STATUS] {message}")

    @staticmethod
    def print_separator(title: str):
        """Prints a visual separator for different sections."""
        print(f"\\n{'='*40}")
        print(f"  {title.upper()}")
        print("="*40)

    @staticmethod
    def highlight(text: str):
        """Wraps text in bold-like markers (simulated)."""
        return f"*** {text} ***"
