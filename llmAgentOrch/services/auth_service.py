class AuthService:
    VALID_API_KEYS = {"secret-key-123", "admin-key-456"}

    @staticmethod
    def validate(api_key: str) -> bool:
        return api_key in AuthService.VALID_API_KEYS
