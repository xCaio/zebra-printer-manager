import socket
from concurrent.futures import ThreadPoolExecutor

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

    @staticmethod
    def check_status(
        ip: str,
        port: int,
        timeout: int = 2
    ) -> bool:
        try:
            with socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            ) as printer_socket:

                printer_socket.settimeout(timeout)
                printer_socket.connect((ip, port))

                return True

        except (
            socket.timeout,
            ConnectionRefusedError,
            OSError
        ):
            return False

    @staticmethod
    def check_multiple_status(
        printers: list
    ) -> list:
        def check(printer):
            online = PrinterService.check_status(
                ip=printer.ip,
                port=printer.port
            )

            return {
                "printer_id": printer.id,
                "name": printer.name,
                "ip": printer.ip,
                "port": printer.port,
                "online": online
            }

        with ThreadPoolExecutor(
            max_workers=10
        ) as executor:

            results = list(
                executor.map(check, printers)
            )

        return results