import socket

class PrinterService:
    @staticmethod
    def print_zpl(
        ip: str,
        port: int,
        zpl: str,
        timeout: int = 5
    ) -> None:
        try:
            with socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            ) as printer_socket:
                printer_socket.settimeout(timeout)
                printer_socket.connect((ip, port))
                printer_socket.sendall(
                    zpl.encode("utf-8")
                )
        except socket.timeout:
            raise ConnectionError(
                "Tempo limite ao conectar com a impressora"
            )
        except ConnectionRefusedError as error:
            raise ConnectionError(
                f"Erro ao conectar com a impressora: {error}"
            )

    @staticmethod
    def test_printer(
        ip: str,
        port: int
    ) -> None:

        zpl = """
^XA
^CF0,40
^FO50,50^FDZEBRA PRINTER MANAGER^FS
^FO50,110^FDTESTE DE IMPRESSAO^FS
^FO50,170^FDIP: %s^FS
^XZ
""" % ip

        PrinterService.print_zpl(
            ip=ip,
            port=port,
            zpl=zpl
        )