# -*- coding: utf-8 -*-
"""
Módulo de Lógica de Negocio.

Contiene todas las funciones para gestionar la agenda de miembros (CRUD).
Este módulo utiliza 'datos' para la persistencia.
"""

from typing import Any, Dict, List, Optional

import datos



def generar_id(miembros: List[Dict[str, Any]]) -> int:
    """
    Genera un nuevo ID autoincremental para un miembro.

    Args:
        miembros (List[Dict[str, Any]]): La lista actual de miembros.
    Returns:
        int: El nuevo ID a asignar.
    """
    if not miembros:
        return 1
    max_id = max(int(ap.get('id', 0)) for ap in miembros)
    return max_id + 1

def crear_miembro(
        filepath: str,
        id_miembro: int,
        tipo_suscripcion: str,
        nombres: str,
) -> Optional[Dict[str, Any]]:
    """
    (CREATE) Agrega un nuevo miembro a la agenda.

    Valida que el número de documento no exista antes de agregarlo.

    Args:
        filepath (str): Ruta al archivo de datos.
        nombres (str): Nombres del miembro.

    Returns:
        Optional[Dict[str, Any]]: El diccionario del miembro creado o None si ya existía.
    """
    miembros = datos.cargar_datos(filepath)
    documento_miembro = str(id_miembro)

    if any(ap.get('documento') == documento_miembro for ap in miembros):
        print(f"\n❌ Error: El documento '{documento_miembro}' ya se encuentra registrado.")
        return None

    nuevo_id = generar_id(miembros)

    nuevo_miembro = {
        'id': str(nuevo_id),
        'id_miembro': documento_miembro,
        'nombres': nombres,
        'tipo_suscripción': tipo_suscripcion,
        
    }

    miembros.append(nuevo_miembro)
    datos.guardar_datos(filepath, miembros)
    return nuevo_miembro

def leer_todos_los_miembros(filepath: str) -> List[Dict[str, Any]]:
    """
    (READ) Obtiene la lista completa de miembros.

    Args:
        filepath (str): Ruta al archivo de datos.

    Returns:
        List[Dict[str, Any]]: La lista de miembros.
    """
    return datos.cargar_datos(filepath)

def buscar_miembro_por_nombre(filepath: str, id_miembro: str) -> Optional[Dict[str, Any]]:
    """
    Busca un miembro específico por su número de documento.

    Args:
        filepath (str): Ruta al archivo de datos.
        id_miembro (str): El documento a buscar.

    Returns:
        Optional[Dict[str, Any]]: El diccionario del miembro si se encuentra, de lo contrario None.
    """
    miembros = datos.cargar_datos(filepath)
    for miembro in miembros:
        if miembro.get('id_miembro') == id_miembro:
            return miembro
    return None

def actualizar_miembro(
        filepath: str,
        nombre: str,
        datos_nuevos: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    (UPDATE) Modifica los datos de un miembro existente.

    Args:
        filepath (str): Ruta al archivo de datos.
        nombre (str): El nombre del miembro a actualizar.
        datos_nuevos (Dict[str, Any]): Un diccionario con los campos a actualizar.

    Returns:
        Optional[Dict[str, Any]]: El diccionario del miembro actualizado, o None si no se encontró.
    """
    miembros = datos.cargar_datos(filepath)
    miembro_encontrado = None
    indice = -1

    for i, miembro in enumerate(miembros):
        if miembro.get('nombre') == nombre:
            miembro_encontrado = miembro
            indice = i
            break

    if miembro_encontrado:
        # Convertimos todos los nuevos valores a string para consistencia
        for key, value in datos_nuevos.items():
            datos_nuevos[key] = str(value)

        miembro_encontrado.update(datos_nuevos)
        miembros[indice] = miembro_encontrado
        datos.guardar_datos(filepath, miembros)
        return miembro_encontrado

    return None

def eliminar_miembro(filepath: str, nombre: str) -> bool:
    """
    (DELETE) Elimina un miembro de la agenda.

    Args:
        filepath (str): Ruta al archivo de datos.
        nombre (str): El nombre del miembro a eliminar.

    Returns:
        bool: True si el miembro fue eliminado, False si no se encontró.
    """
    miembros = datos.cargar_datos(filepath)
    miembro_a_eliminar = None

    for miembro in miembros:
        if miembro.get('nombre') == nombre:
            miembro_a_eliminar = miembro
            break

    if miembro_a_eliminar:
        miembros.remove(miembro_a_eliminar)
        datos.guardar_datos(filepath, miembros)
        return True

    return False

