class Utils:
    def getString(self, string: object) -> str:
        return str(string) if isinstance(string, (str, int, float)) else ""
