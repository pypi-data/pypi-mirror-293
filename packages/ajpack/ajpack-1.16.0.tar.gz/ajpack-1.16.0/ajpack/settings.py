class Settings:
    # Module settings here

    def __init__(self) -> None:
        self.send_init_msg: bool = True # If true --> The package will print, that it is initialized.
        
        # Reset color/mode
        self.RESET: str = "\033[0m"

        # Formats
        self.BOLD: str = "\033[1m"
        self.ITALIC: str = "\033[3m"
        self.UNDERLINE: str = "\033[4m"
        self.INVISIBLE: str = "\033[8m"
        self.STRIKETHROUGH: str = "\033[9m"
        self.UNDERLINE_DOUBLE: str = "\033[21m"

        # Colors
        self.GRAY: str = "\033[90m"
        self.RED: str = "\033[91m"
        self.GREEN: str = "\033[92m"
        self.YELLOW: str = "\033[93m"
        self.BLUE: str = "\033[94m"
        self.MAGENTA: str = "\033[95m"
        self.CYAN: str = "\033[96m"

        # Reset color
        self.WHITE: str = "\033[97m"

settings = Settings()