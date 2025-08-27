import os

mode = os.getenv("DB_MODE", "local")  # default = local

if mode == "docker":
    from db_docker import get_conn
else:
    from db_local import get_conn
