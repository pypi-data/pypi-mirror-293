import os

from sonarcloud_report.logger_manager import die


def must_get_env_var(env_var_name: str) -> str:
    env_var = os.environ.get(env_var_name)
    if not env_var:
        die(f"Environment variable '{env_var_name}' is missing")
    return env_var
