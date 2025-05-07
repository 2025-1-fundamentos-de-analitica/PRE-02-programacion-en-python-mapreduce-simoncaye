"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os
import string
from itertools import groupby


def load_input(input_directory):
    """Funcion load_input"""
    contenido = []
    archivos = glob.glob(f"{input_directory}/*")
    with fileinput.input(files=archivos) as lineas:
        for linea in lineas:
            contenido.append((fileinput.filename(), linea))
    return contenido


def line_preprocessing(sequence):
    """Line Preprocessing"""
    procesadas = []
    for archivo, linea in sequence:
        limpio = linea.translate(str.maketrans("", "", string.punctuation)).lower()
        procesadas.append((archivo, limpio))
    return procesadas


def mapper(sequence):
    """Mapper"""
    mapeadas = []
    for _, texto in sequence:
        for palabra in texto.split():
            mapeadas.append((palabra, 1))
    return mapeadas


def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    return sorted(sequence, key=lambda tupla: tupla[0])


def reducer(sequence):
    """Reducer"""
    resultado = []
    for palabra, grupo in groupby(sequence, lambda par: par[0]):
        total = sum(valor for _, valor in grupo)
        resultado.append((palabra, total))
    return resultado


def create_ouptput_directory(output_directory):
    """Create Output Directory"""
    if os.path.exists(output_directory):
        archivos = glob.glob(f"{output_directory}/*")
        for archivo in archivos:
            os.remove(archivo)
        os.rmdir(output_directory)
    os.makedirs(output_directory)


def save_output(output_directory, sequence):
    """Save Output"""
    ruta_salida = os.path.join(output_directory, "part-00000")
    with open(ruta_salida, "w", encoding="utf-8") as salida:
        for clave, valor in sequence:
            salida.write(f"{clave}\t{valor}\n")


def create_marker(output_directory):
    """Create Marker"""
    marcador = os.path.join(output_directory, "_SUCCESS")
    with open(marcador, "w", encoding="utf-8") as f:
        f.write("")


def run_job(input_directory, output_directory):
    """Job"""
    datos = load_input(input_directory)
    datos = line_preprocessing(datos)
    datos = mapper(datos)
    datos = shuffle_and_sort(datos)
    datos = reducer(datos)
    create_ouptput_directory(output_directory)
    save_output(output_directory, datos)
    create_marker(output_directory)


if __name__ == "__main__":
    run_job(
        "input",
        "output",
    )
