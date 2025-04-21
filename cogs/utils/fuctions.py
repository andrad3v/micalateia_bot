import os

def get_env_variable(var_name):
    """Get the environment variable or raise an exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        raise EnvironmentError(f"Set the {var_name} environment variable.") from None