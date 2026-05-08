import subprocess
import sys


def run_cli(*args):
    # subprocess to simulate using the actual CLI
    # will accept any number of parameters

    result = subprocess.run(
        [sys.executable, "-m", "shieldli.main", *args],
        capture_output=True,
        text=True,
    )  # need to capture output to assert on
    return result.returncode


def test_workflow(tmp_path):
    # trying to simulate a user running through each command

    # creating a file
    res = run_cli("cr", str(tmp_path / "file.txt"), "Boo")
    assert res == 0
    assert (tmp_path / "file.txt").exists()

    # Copys original 'file' into 'copy' and checks the content is the same
    run_cli("cp", str(tmp_path / "file.txt"), str(tmp_path / "copy.txt"))
    assert res == 0
    assert (tmp_path / "copy.txt").exists()

    # merge both file & copy into one file
    run_cli(
        "merge",
        str(tmp_path / "file.txt"),
        str(tmp_path / "copy.txt"),
        str(tmp_path / "output.txt"),
    )

    # print(repr(output.read_bytes()))
    assert (tmp_path / "output.txt").exists()
    assert (tmp_path / "output.txt").read_text() == "BooBoo"

    # Delete original
    run_cli("rm", str(tmp_path / "file.txt"))
    assert not (tmp_path / "file.txt").exists()
