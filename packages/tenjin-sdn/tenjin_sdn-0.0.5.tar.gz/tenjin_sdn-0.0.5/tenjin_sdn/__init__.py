from .tenjin_sdn  import *

def cli():
    cli_default()

def speak_hello():
    a = say_hello()
    print(a)

class Ctrl13:
    address: str
    port: int
    def __init__(self, address: str = "127.0.0.1", port: int = 6653) -> None:
        self.address = address
        self.port = port
        pass

    def run(self):
        controller13(f"{self.address}:{self.port}")

class Ctrl10:
    address: str
    port: int
    def __init__(self, address: str = "127.0.0.1", port: int = 6653) -> None:
        self.address = address
        self.port = port
        pass

    def run(self):
        controller10(f"{self.address}:{self.port}")