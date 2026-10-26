import importlib


def test_required_dependencies_are_available():
    importlib.import_module("google.generativeai")
    importlib.import_module("PyPDF2")
    importlib.import_module("docx")
