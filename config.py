class Config:
    SECRET_KEY = "docuvault-super-secret-hardcoded-2024"
    DB_PASSWORD = "comex26"
    INTERNAL_STORAGE_HOST = "192.168.1.100"
    SQLALCHEMY_DATABASE_URI = "sqlite:///docuvault.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRY_HOURS = 24
