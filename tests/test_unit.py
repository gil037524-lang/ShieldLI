import pytest

from shieldli.main import cli, cmd_copy, cmd_delete, cmd_list

# -------------------
# cmd_list coverage
# -------------------


def test_list_directory(tmp_path, capsys):
    (tmp_path / "test1.txt").write_text("test")
    (tmp_path / "test2.txt").write_text("test")
    cmd_list([str(tmp_path)])
    captured = capsys.readouterr()
    lines = captured.out.strip().splitlines()
    assert sorted(lines) == ["test1.txt", "test2.txt"]


def test_list_current_directory(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)  # change to test tmp directory
    (tmp_path / "test1.txt").write_text("test")
    cmd_list([])
    captured = capsys.readouterr()
    assert "test1.txt" in captured.out


def test_list_bad_path():
    with pytest.raises(SystemExit) as exc:
        cmd_list(["idontexistfolder/"])  # i dont exist yet, should throw raise flag
    assert exc.value.code == 1


def test_cli_ls(monkeypatch, capsys, tmp_path):
    (tmp_path / "test.txt").write_text("test")
    monkeypatch.setattr("sys.argv", ["shieldli", "list", str(tmp_path)])
    cli()
    assert "test.txt" in capsys.readouterr().out


# -------------------
# cmd_cr coverage
# -------------------
def test_cr_bad_args(monkeypatch, tmp_path):
    monkeypatch.setattr("sys.argv", ["shieldli", "cr", "potato", "apple", "eggs"])
    with pytest.raises(SystemExit):
        cli()


def test_cr_with_name(monkeypatch, tmp_path):
    test = tmp_path / "test.txt"
    monkeypatch.setattr("sys.argv", ["shieldli", "cr", str(test), "test"])
    cli()
    assert test.exists()


def test_cr_no_name(monkeypatch, tmp_path):
    test = tmp_path / "test.txt"
    monkeypatch.setattr("sys.argv", ["shieldli", "cr", str(test)])
    cli()
    assert test.exists()


def test_cr_overwrite(monkeypatch, tmp_path):
    (tmp_path / "test.txt").write_text("test")
    test = tmp_path / "test.txt"
    monkeypatch.setattr("sys.argv", ["shieldli", "cr", str(test), "test"])
    monkeypatch.setattr("builtins.input", lambda _: "y")  # trigger the yes option on input
    cli()
    assert test.exists()


def test_cr_overwrite_exit(monkeypatch, tmp_path):
    (tmp_path / "test.txt").write_text("test")
    test = tmp_path / "test.txt"
    monkeypatch.setattr("sys.argv", ["shieldli", "cr", str(test), "test"])
    monkeypatch.setattr("builtins.input", lambda _: "Ditto")  # trigger the no option on input
    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 0  # exit gracefully val


def test_cr_bad_filepath(monkeypatch, tmp_path):
    test = tmp_path / "@$ test@#/.txt"  # inavlid name for path
    monkeypatch.setattr("sys.argv", ["shieldli", "cr", str(test), "test"])
    with pytest.raises(SystemExit):
        cli()


# -------------------
# cmd_copy coverage
# -------------------


def test_copy_file(tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("2319")
    cmd_copy([str(src), str(dst)])

    # checking file exist and contents
    assert dst.exists()
    assert dst.read_text() == "2319"


def test_copy_with_directory(tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"

    src.write_text("test")
    dst.mkdir()

    cmd_copy([str(src), str(dst)])
    copied = dst / "src.txt"
    assert copied.exists()
    assert copied.read_text() == "test"


def test_copy_file_exits(tmp_path):
    src = tmp_path / "test.txt"
    src.write_text("test")

    with pytest.raises(SystemExit):  # this trigger the same name check
        cmd_copy([str(src), str(src)])


def test_copy_file_doesnt_exist(tmp_path, capsys):  # trigger if src/dest dont exist
    src = tmp_path / "src.txt"
    dst = tmp_path / "dest.txt"

    with pytest.raises(SystemExit) as exc:
        cmd_copy([str(src), str(dst)])

    assert exc.value.code == 1
    assert "error:" in capsys.readouterr().err


def test_copy_bad_args():  # 0/empty args
    with pytest.raises(SystemExit):
        cmd_copy([])


def test_cli_cp(monkeypatch, tmp_path):
    src = tmp_path / "test.txt"
    src.write_text("test")
    dst = tmp_path / "dst.txt"
    monkeypatch.setattr("sys.argv", ["shieldli", "copy", str(src), str(dst)])
    cli()

    assert dst.read_text() == "test"


# -------------------
# cmd_delete coverage
# -------------------


def test_delete_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("test")
    cmd_delete([str(file)])

    assert not file.exists()


def test_delete_no_file():
    with pytest.raises(SystemExit):
        cmd_delete(["test.txt"])


def test_delete_bad_args():
    with pytest.raises(SystemExit):
        cmd_delete([])


def test_cli_del(monkeypatch, tmp_path):
    target = tmp_path / "test.txt"
    target.write_text("test")
    monkeypatch.setattr("sys.argv", ["shieldli", "rm", str(target)])
    cli()
    assert not target.exists()


# -------------------
# cli merge coverage
# -------------------
def test_cli_merge_arg_count(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "sys.argv",
        [
            "shieldli",
            "merge",
        ],
    )
    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 1


def test_cli_merge(monkeypatch, tmp_path):
    input1 = tmp_path / "input1"
    input1.write_text("dragon")

    input2 = tmp_path / "input2"
    input2.write_text("ite")

    output = tmp_path / "output.txt"

    monkeypatch.setattr("sys.argv", ["shieldli", "merge", str(input1), str(input2), str(output)])
    cli()
    assert output.read_text() == "dragonite"


def test_cli_merge_bad_arg(monkeypatch, tmp_path):
    input1 = tmp_path / "input1"
    input1.write_text("dragon")

    input2 = tmp_path / "input2"

    output = tmp_path / "output.txt"

    monkeypatch.setattr("sys.argv", ["shieldli", "merge", str(input1), str(input2), str(output)])

    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 1


# -------------------
# cli other options coverage
# -------------------


def test_cli_noargs(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["shieldli"])

    with pytest.raises(SystemExit) as exc:
        cli()
    captured = capsys.readouterr()
    assert exc.value.code == 1
    assert "usage:" in captured.out


def test_cli_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["shieldli", "-h"])
    cli()
    captured = capsys.readouterr()
    assert "usage:" in captured.out


def test_cli_unknown(monkeypatch):
    monkeypatch.setattr("sys.argv", ["shieldli", "unknown"])
    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 1
