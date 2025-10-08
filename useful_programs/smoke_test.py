#!/usr/bin/env python3
"""Run quick smoke tests for the useful_programs utilities."""
import subprocess
import sys
import json
from pathlib import Path


ROOT = Path(__file__).parent


def run(cmd, input_text=None):
    p = subprocess.run([sys.executable, *cmd], input=input_text, text=True, capture_output=True)
    return p.returncode, p.stdout, p.stderr


def test_calc():
    code, out, err = run([str(ROOT / "cli_calculator.py"), "(2+3)*4"])
    assert code == 0 and out.strip() == "20"


def test_json():
    js = '{"a":1, "b":[1,2]}'
    code, out, err = run([str(ROOT / "json_pretty.py")], input_text=js)
    assert code == 0
    data = json.loads(out)
    assert data["a"] == 1


def test_file_organizer(tmp_dir: Path):
    d = tmp_dir / "test_org"
    d.mkdir(exist_ok=True)
    f = d / "sample.txt"
    f.write_text("hello")
    code, out, err = run([str(ROOT / "file_organizer.py"), str(d)])
    assert code == 0
    assert (d / "txt" / "sample.txt").exists()


def main():
    print("Running smoke tests...")
    test_calc()
    print("calc ok")
    test_json()
    print("json ok")
    # file organizer needs a temp dir; create one in /tmp
    from tempfile import TemporaryDirectory
    from pathlib import Path
    with TemporaryDirectory() as td:
        test_file_organizer(Path(td))
    print("file organizer ok")
    print("All smoke tests passed")


if __name__ == "__main__":
    main()
