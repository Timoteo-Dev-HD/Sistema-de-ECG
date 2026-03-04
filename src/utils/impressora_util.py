import socket

def print_pdf_to_ip(printer_ip, pdf_path):
    printer_port = 9100

    with open(pdf_path, "rb") as f:
        pdf_data = f.read()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((printer_ip, printer_port))
    sock.sendall(pdf_data)
    sock.close()

    print("PDF enviado para impressora!")