class ConfigNotFoundException(Exception):
    """Raised when a configuration file isn't found"""
    pass

class UnsupportedProjectionTypeException(Exception):
    """Raised when attempting to access an unsupported projection system"""
    pass