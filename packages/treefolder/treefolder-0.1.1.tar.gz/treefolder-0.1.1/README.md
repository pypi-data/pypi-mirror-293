[![English](https://img.shields.io/badge/language-English-blue)](#ENGLISH) 
[![Español](https://img.shields.io/badge/idioma-Español-red)](#ESPAÑOL)
___

# ENGLISH

## Overview

Treefolder is a simple Python program that generates an ASCII representation of a directory tree.
The function takes 2 parameters -i or -n and also the name of any folder that you want to ignore on the representation of the tree.
For example:
 - `python tree.py -i sass images`: This will ignore all the base folders and also sass and images folder.
 - `python tree.py -n .git`: This will ignore only the folder .git

** If installed using pip, the commands are `treefolder -i args` or `treefolder -n args`. **

## Features

- **Directory Tree Generation**: Creates an ASCII tree representation of a specified directory.
- **Ignore Folders**: Option to ignore specific folders or use a predefined list of common folders to ignore.
- **GUI Folder Selection**: Uses a graphical interface to select the folder to generate the tree for.

## How It Works

1. **Folder Selection**: Users select a folder using a graphical file dialog.
2. **Tree Generation**: The program generates an ASCII tree representation of the selected folder, optionally ignoring specified folders.
3. **Output**: The generated tree is printed to the console.

## Setup Instructions

### Prerequisites

- Python 3.x
- Required Python libraries: os, argparse, tkinter

### Installation

1. **Clone the repository**:
   - `git clone https://github.com/Aperezortega/Treefolder.git`
   - `cd treefolder`
   - `pip install -r requirements.txt`

o

2. **Install from PyPI**:
   - `pip install treefolder`

### Usage

1. **Run the script**:
   - `python treefolder.py`
2. **Select a folder**: A file dialog will appear to select the folder.
3. **View the tree**: The ASCII tree representation will be printed in the console.

### Customization

- **Ignored Folders**: Modify the `base_ignored_folders` list in the script to add or remove default ignored folders.
- **Command Line Arguments**: Use `-i` or `--ignore` to specify additional folders to ignore, or `-n` or `--no-ignore` to specify folders to ignore exclusively.

___

# ESPAÑOL

## Descripción General

Treefolder es un programa simple en Python que genera una representación ASCII de un árbol de directorios. La función acepta 2 parámetros -i o -n y también el nombre de cualquier carpeta que desees ignorar en la representación del árbol. 
Por ejemplo:
python tree.py -i sass images: Esto ignorará todas las carpetas base y también las carpetas sass e images.
python tree.py -n .git: Esto ignorará solo la carpeta .git.

** Si se installa usando pip los comandos serían treefolder -i args o treefolder -n args**

## Características

- **Generación de Árbol de Directorios**: Crea una representación en ASCII de un árbol de directorios especificado.
- **Ignorar Carpetas**: Opción para ignorar carpetas específicas o usar una lista predefinida de carpetas comunes para ignorar.
- **Selección de Carpeta con GUI**: Utiliza una interfaz gráfica para seleccionar la carpeta para generar el árbol.

## Cómo Funciona

1. **Selección de Carpeta**: Los usuarios seleccionan una carpeta usando un cuadro de diálogo de archivos gráfico.
2. **Generación de Árbol**: El programa genera una representación en ASCII del árbol de la carpeta seleccionada, ignorando opcionalmente las carpetas especificadas.
3. **Salida**: El árbol generado se imprime en la consola.

## Instrucciones de Configuración

### Requisitos Previos

- Python 3.x
- Bibliotecas de Python requeridas: os, argparse, tkinter

### Instalación

1. **Clone the repository**:
   - `git clone https://github.com/Aperezortega/Treefolder.git`
   - `cd treefolder`
   - `pip install -r requirements.txt`

o

2. **Install from PyPI**:
   - `pip install treefolder`

### Uso

1. **Ejecutar el script**:
   - `python treefolder.py`
2. **Seleccionar una carpeta**: Aparecerá un cuadro de diálogo para seleccionar la carpeta.
3. **Ver el árbol**: La representación en ASCII del árbol se imprimirá en la consola.

### Personalización

- **Carpetas Ignoradas**: Modifique la lista `base_ignored_folders` en el script para agregar o eliminar carpetas ignoradas por defecto.
- **Argumentos de Línea de Comandos**: Use `-i` o `--ignore` para especificar carpetas adicionales a ignorar, o `-n` o `--no-ignore` para especificar carpetas a ignorar exclusivamente.

___