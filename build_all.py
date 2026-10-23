import runpy
from pathlib import Path

HERE = Path(__file__).parent
runpy.run_path(str(HERE / "make_custom_icons.py"))
for f in sorted(HERE.glob("fig*.py")):
    runpy.run_path(str(f), run_name="__main__")
