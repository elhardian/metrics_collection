class InvalidDatabaseConfiguration(Exception):
    def __init__(self):
        message = "Database configuration is invalid"
        super().__init__(message)