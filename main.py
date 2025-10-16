"""
Módulo Principal - Interfaz de Usuario (UI).

Punto de entrada de la aplicación.
Maneja la interacción con el usuario (menús, entradas, salidas) usando la librería rich.
"""

import os

import crud

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

console = Console()

DIRECTORIO_DATOS = 'info'
NOMBRE_ARCHIVO_CSV = 'miembros.csv'
NOMBRE_ARCHIVO_JSON = 'inscipciones.json'

# --- Funciones de Interfaz de Usuario con Rich ---

def solicitar_tipo_suscripcion(permitir_vacio: bool = False) -> str | None:
    """
    Muestra un menú para que el usuario elija el tipo de nombre usando Rich.

    Args:
        permitir_vacio (bool): Si es True, permite la opción de no cambiar.

    Returns:
        str | None: La abreviatura del tipo de nombre seleccionado o None.
    """
    console.print("\nSeleccione el tipo de suscripción:", style="cyan")

    tipos = {
        '1': 'Mensual', '2': 'Anual'
    }

    opciones = list(tipos.keys())
    prompt_texto = ""

    if permitir_vacio:
        prompt_texto += "[bold yellow]0[/bold yellow]. No cambiar\n"
        opciones.insert(0, '0')


    opcion = Prompt.ask("Opción", choices=opciones, show_choices=False)

    if permitir_vacio and opcion == '0':
        return None
    return tipos[opcion]


def menu_crear_miembro(filepath: str):
    """Maneja la lógica para registrar un nuevo miembro."""
    console.print(Panel.fit("[bold cyan]📝 Registrar Nuevo miembro[/bold cyan]"))

    tipo_suscripcion = solicitar_tipo_suscripcion()
    nombres = Prompt.ask("Nombres")
    id_miembro = Prompt.ask("ID Miembro")

    miembro_creado = crud.crear_miembro(
        filepath, tipo_suscripcion, id_miembro, nombres
    )

    if miembro_creado:
        console.print(Panel(f"✅ ¡miembro registrado con éxito!\n   ID Asignado: [bold yellow]{miembro_creado['id']}[/bold yellow]",
                            border_style="green", title="Éxito"))
    else:
        console.print(Panel("⚠️ No se pudo registrar al miembro. Verifique los datos.",
                            border_style="red", title="Error"))


def menu_leer_miembros(filepath: str):
    """Maneja la lógica para mostrar todos los miembros en una tabla."""
    console.print(Panel.fit("[bold cyan]👥 Lista de miembros[/bold cyan]"))
    miembros = crud.leer_todos_los_miembros(filepath)

    if not miembros:
        console.print("[yellow]No hay miembros registrados.[/yellow]")
        return

    # Creamos la tabla
    tabla = Table(title="miembros Registrados", border_style="blue", show_header=True, header_style="bold magenta")
    tabla.add_column("ID", style="dim", width=5)
    tabla.add_column("Ficha", justify="right")
    tabla.add_column("Tipo Doc.", justify="center")
    tabla.add_column("nombre", justify="right")
    tabla.add_column("Nombre Completo")
    tabla.add_column("Teléfono", justify="right")

    # Ordenamos por Ficha y luego por ID
    miembros_ordenados = sorted(miembros, key=lambda x: (int(x['ficha']), int(x['id'])))

    for ap in miembros_ordenados:
        tabla.add_row(
            ap['id'],
            ap['ficha'],
            ap['tipo_suscripcion'],
            ap['nombre'],
            f"{ap['nombres']} {ap['apellidos']}",
            ap['telefono']
        )

    console.print(tabla)


def menu_actualizar_miembro(filepath: str):
    """Maneja la lógica para actualizar un miembro."""
    console.print(Panel.fit("[bold cyan]✏️ Actualizar Datos de miembro[/bold cyan]"))
    nombre = IntPrompt.ask("Ingrese el nombre del miembro a actualizar")

    miembro_actual = crud.buscar_miembro_por_nombre(filepath, str(nombre))
    if not miembro_actual:
        console.print("\n[bold red]❌ No se encontró ningún miembro con ese nombre.[/bold red]")
        return

    console.print("\nDatos actuales. Presione Enter para no modificar un campo.")
    datos_nuevos = {}

    nuevo_tipo_doc = solicitar_tipo_suscripcion(permitir_vacio=True)
    if nuevo_tipo_doc: datos_nuevos['tipo_suscripcion'] = nuevo_tipo_doc

    nombres = Prompt.ask(f"Nombres ({miembro_actual['nombres']})", default=miembro_actual['nombres'])
    if nombres != miembro_actual['nombres']: datos_nuevos['nombres'] = nombres

    apellidos = Prompt.ask(f"Apellidos ({miembro_actual['apellidos']})", default=miembro_actual['apellidos'])
    if apellidos != miembro_actual['apellidos']: datos_nuevos['apellidos'] = apellidos

    direccion = Prompt.ask(f"Dirección ({miembro_actual['direccion']})", default=miembro_actual['direccion'])
    if direccion != miembro_actual['direccion']: datos_nuevos['direccion'] = direccion

    telefono = IntPrompt.ask(f"Teléfono ({miembro_actual['telefono']})", default=int(miembro_actual['telefono']))
    if telefono != int(miembro_actual['telefono']): datos_nuevos['telefono'] = telefono

    ficha = IntPrompt.ask(f"Ficha ({miembro_actual['ficha']})", default=int(miembro_actual['ficha']))
    if ficha != int(miembro_actual['ficha']): datos_nuevos['ficha'] = ficha

    if not datos_nuevos:
        console.print("\n[yellow]No se modificó ningún dato.[/yellow]")
        return

    miembro_actualizado = crud.actualizar_miembro(filepath, str(nombre), datos_nuevos)
    if miembro_actualizado:
        console.print(Panel("✅ ¡Datos del miembro actualizados con éxito!", border_style="green", title="Éxito"))
    else:
        console.print(Panel("❌ Ocurrió un error al actualizar.", border_style="red", title="Error"))


def menu_eliminar_miembro(filepath: str):
    """Maneja la lógica para eliminar un miembro."""
    console.print(Panel.fit("[bold cyan]🗑️ Eliminar miembro[/bold cyan]"))
    nombre = IntPrompt.ask("Ingrese el nombre del miembro a eliminar")

    miembro = crud.buscar_miembro_por_nombre(filepath, str(nombre))
    if not miembro:
        console.print("\n[bold red]❌ No se encontró ningún miembro con ese nombre.[/bold red]")
        return

    confirmacion = Confirm.ask(
        f"¿Está seguro de que desea eliminar a [bold]{miembro['nombres']} {miembro['apellidos']}[/bold]?",
        default=False
    )

    if confirmacion:
        if crud.eliminar_miembro(filepath, str(nombre)):
            console.print(Panel("✅ ¡miembro eliminado con éxito!", border_style="green", title="Éxito"))
        else:
            console.print(Panel("❌ Ocurrió un error al eliminar.", border_style="red", title="Error"))
    else:
        console.print("\n[yellow]Operación cancelada.[/yellow]")


def elegir_almacenamiento() -> str:
    """Pregunta al usuario qué formato de archivo desea usar y construye la ruta."""
    console.print(Panel.fit("[bold cyan]⚙️ Configuración de Almacenamiento[/bold cyan]"))

    prompt_texto = (
        "¿Dónde desea almacenar los datos?\n"
        "[bold yellow]1[/bold yellow]. CSV (Archivo de texto plano)\n"
        "[bold yellow]2[/bold yellow]. JSON (Formato más estructurado)"
    )
    console.print(prompt_texto)

    opcion = Prompt.ask(
        "Opción",
        choices=["1", "2"],
        default="2",
        show_choices=False
    )
    if opcion == '1':
        return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_CSV)
    else:
        return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_JSON)

def mostrar_menu_principal():
    """Imprime el menú principal en la consola usando un Panel de Rich."""
    menu_texto = (
        "[bold yellow]1[/bold yellow]. Registrar un nuevo miembro\n"
        "[bold yellow]2[/bold yellow]. Ver todos los miembros\n"
        "[bold yellow]3[/bold yellow]. Actualizar datos de un miembro\n"
        "[bold yellow]4[/bold yellow]. Eliminar un miembro\n"
        "[bold red]5[/bold red]. Salir"
    )
    console.print(Panel(menu_texto, title="[bold]crud DE miembros SENA[/bold]", subtitle="Seleccione una opción", border_style="green"))

def main():
    """Función principal que ejecuta el bucle del menú."""
    archivo_seleccionado = elegir_almacenamiento()
    console.print(f"\n👍 Usando el archivo: [bold green]{archivo_seleccionado}[/bold green]")

    while True:
        mostrar_menu_principal()
        opcion = Prompt.ask("Opción", choices=["1", "2", "3", "4", "5"], show_choices=False)

        if opcion == '1':
            menu_crear_miembro(archivo_seleccionado)
        elif opcion == '2':
            menu_leer_miembros(archivo_seleccionado)
        elif opcion == '3':
            menu_actualizar_miembro(archivo_seleccionado)
        elif opcion == '4':
            menu_eliminar_miembro(archivo_seleccionado)
        elif opcion == '5':
            console.print("\n[bold magenta]👋 ¡Hasta luego! Gracias por usar la crud.[/bold magenta]")
            break

# --- Punto de Entrada del Script ---
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Programa interrumpido por el usuario. Adiós.[/bold red]")