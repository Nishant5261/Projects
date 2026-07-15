import runpy
from pathlib import Path

app_path = Path(__file__).resolve().parents[1] / "Lekh-AI powered Text humanizer" / "app.py"
runpy.run_path(str(app_path), run_name="__main__")
