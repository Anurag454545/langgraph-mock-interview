# backend/run.py
import pathlib
import importlib.util
import sys

# locate the app/main.py by path
p = pathlib.Path(__file__).parent / "app" / "main.py"

spec = importlib.util.spec_from_file_location("app_main_by_path", str(p))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# get FastAPI app object
app = getattr(mod, "app", None)
if app is None:
    raise RuntimeError("FastAPI 'app' not found in app/main.py — check the file.")

if __name__ == "__main__":
    # start uvicorn programmatically (no command-line module import issues)
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
