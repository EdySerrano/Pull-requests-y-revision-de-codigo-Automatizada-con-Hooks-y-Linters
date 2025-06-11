# tests/test_config_modifier.py

import pytest
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from config_modifier import leer_json, incrementar_version

@pytest.fixture
# Preparamos un archivo temporal para pruebas
def json_de_prueba(tmp_path):
    file_path = tmp_path / "config.json"
    data = {"version": 1.0, "name": "Test App"}
    with open(file_path, 'w') as f:
        json.dump(data, f)
    return file_path

# Preparamos un archivo JSON valido para probar la lectura correcta
def test_leer_json_valido(json_de_prueba):
    contenido = leer_json(json_de_prueba)
    assert contenido["version"] == 1.0
    assert contenido["name"] == "Test App"

# Preparamos un archivo JSON con el campo 'version' valido para probar el incremento de version
def test_incrementar_version(json_de_prueba):
    nueva_version = incrementar_version(json_de_prueba)
    assert nueva_version == 2.0
    with open(json_de_prueba) as f:
        datos = json.load(f)
    assert datos["version"] == 2.0

#Preparamos un archivo  con contenido invalido (no JSON)
def test_leer_json_invalido(tmp_path):
    file_path = tmp_path / "invalido.json"
    file_path.write_text("esto no es json")
    with pytest.raises(ValueError):
        leer_json(file_path)

# Preparamos un archivo JSON con campo 'version' de tipo incorrecto
def test_incrementar_version_tipo_incorrecto(tmp_path):
    file_path = tmp_path / "version_invalida.json"
    with open(file_path, 'w') as f:
        json.dump({"version": "uno"}, f)
    with pytest.raises(TypeError):
        incrementar_version(file_path)