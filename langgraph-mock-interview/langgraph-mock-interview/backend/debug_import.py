# backend/debug_import.py
import importlib, traceback

try:
    importlib.import_module('app.main')
    print("import OK: app.main imported successfully.")
except Exception:
    print("Import failed. Full traceback follows:\n")
    traceback.print_exc()
