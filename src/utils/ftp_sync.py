# from pyftpdlib.authorizers import DummyAuthorizer
# from pyftpdlib.handlers import FTPHandler
# from pyftpdlib.servers import FTPServer
# import os

# HOST = "172.19.0.18"
# PORT = 21

# FTP_USER = "admin"
# FTP_PASS = "4815926"

# FTP_ROOT = "/srv/zoncare"  # vai conter /srv/zoncare/ecg
# os.makedirs(os.path.join(FTP_ROOT, "ecg"), exist_ok=True)

# authorizer = DummyAuthorizer()
# # permissões completas para upload e criação de diretórios
# authorizer.add_user(FTP_USER, FTP_PASS, homedir=FTP_ROOT, perm="elradfmwMT")

# handler = FTPHandler
# handler.authorizer = authorizer
# handler.banner = "Zoncare FTP server ready."

# server = FTPServer((HOST, PORT), handler)
# server.serve_forever()

from ftplib import FTP
import os

FTP_HOST = "172.19.0.18"
FTP_USER = "admin"
FTP_PASS = "4815926"
REMOTE_DIR = "ecg"
LOCAL_DIR = "./ecg_local"

def sync_ftp():
    os.makedirs(LOCAL_DIR, exist_ok=True)

    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.cwd(REMOTE_DIR)

    files = ftp.nlst()

    for filename in files:
        local_path = os.path.join(LOCAL_DIR, filename)

        # evita baixar duplicado
        if os.path.exists(local_path):
            continue

        with open(local_path, "wb") as f:
            ftp.retrbinary(f"RETR {filename}", f.write)

    ftp.quit()