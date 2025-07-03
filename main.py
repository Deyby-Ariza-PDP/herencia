from abc import ABC, abstractmethod
from typing import Dict, List

registro_comandos: Dict[str, 'Comando'] = {}

class Comando(ABC):
    nombre: str = ""
    orden: int = 0
    independiente: bool = False

    def __init__(self):
        if not self.nombre:
            raise ValueError("El nombre del comando no puede estar vacío")
        # Registro al instanciar comando
        registro_comandos[self.nombre] = self

    @abstractmethod
    def ejecutar(self) -> None:
        pass

class Init(Comando):
    nombre = "iniciar"
    orden = 5
    independiente = False

    def ejecutar(self) -> None:
        print("Inicializando proyecto...")

class Test(Comando):
    nombre = "test"
    orden = 3
    independiente = False

    def ejecutar(self) -> None:
        print("Inicializando tests...")

class Build(Comando):
    nombre = "build"
    orden = 2
    independiente = False

    def ejecutar(self) -> None:
        print("Compilando fuente...")

class Deploy(Comando):
    nombre = "deploy"
    orden = 4
    independiente = True

    def ejecutar(self) -> None:
        print("Desplegando aplicación...")

class Migrate(Comando):
    nombre = "migrate"
    orden = 1
    independiente = True

    def ejecutar(self) -> None:
        print("Ejecutando migración...")

class Revert(Comando):
    nombre = "revert"
    orden = 0
    independiente = True

    def ejecutar(self) -> None:
        print("Ejecutando reversión...")

# TODO: Agregar registro dinámico para todos los comandos
_init = Init()
_test = Test()
_build = Build()
_deploy = Deploy()
_migrate = Migrate()
_revert = Revert()

class CLI:
    def __init__(self, nombres_comandos: List[str]):
        self.comandos = self._resolver_comandos(nombres_comandos)

    def _resolver_comandos(self, nombres: List[str]) -> List[Comando]:
        lista_comandos: List[Comando] = []
        for nombre in nombres:
            comando = registro_comandos.get(nombre)
            if not comando:
                raise ValueError(f"Comando '{nombre}' no reconocido")
            lista_comandos.append(comando)
        return lista_comandos

    def validar_orden(self) -> None:
        if not self.comandos:
            raise ValueError("No se especificaron comandos")

        if len(self.comandos) == 1:
            return

        comandos_independientes = [cmd.nombre for cmd in self.comandos if cmd.independiente]
        if comandos_independientes:
            raise ValueError(
                f"Los siguientes comandos están marcados como independientes y no pueden "
                f"ejecutarse junto a otros: {', '.join(comandos_independientes)}"
            )

        orden_recibido = [cmd.orden for cmd in self.comandos]
        if orden_recibido != sorted(orden_recibido):
            raise ValueError("El orden de los comandos no es válido")

    def ejecutar(self) -> None:
        self.validar_orden()
        for comando in self.comandos:
            comando.ejecutar()

def main():
    print("Hola")
    print("Sistema de comandos:")
    CLI(["build", "test"]).ejecutar()
    CLI(["revert"]).ejecutar()
    CLI(["no_command"]).ejecutar()

main()
