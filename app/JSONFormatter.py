class JSONFormatter:
    def format(self, text: str) -> list:
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")
        lines = text.splitlines()
        return [line.strip() for line in lines if line.strip()]
