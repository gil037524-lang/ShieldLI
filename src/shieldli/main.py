import shutil  # file operation tools (need copy)
import sys
from pathlib import Path  # filesystem paths lib


def cmd_list(args):
    """List files in a directory. This was not part of the assignment,
       but helped me test the other functions are working.

    :param args: args[0] is an optional (defaults to current dir(./)).
    """
    if args:
        path = Path(args[0])
    else:
        path = Path(".")
    try:
        for entry in path.iterdir():  # iterdir yields path dir
            print(entry.name)
    except OSError as err:
        print(f"error: {err}", file=sys.stderr)
        sys.exit(1)


def cmd_create(args):
    if len(args) > 2 or len(args) < 1:
        print("usage: shieldli cr <path>/filename", file=sys.stderr)
        sys.exit(1)

    path = Path(args[0])

    if len(args) == 2:
        text = args[1]
    else:
        text = ""

    if path.exists():
        ans = input(f"error: {path} already exists, overwrite?(y/n)")
        if ans.lower() != "y":
            sys.exit(0)

    try:
        path.write_text(text, encoding="utf-8")
        print(f"created file a{path}")
    except OSError as err:
        print(f"error: {err}", file=sys.stderr)
        sys.exit(1)


def cmd_copy(args):
    """copy files and directories

    :param args: must in order src -> dst.
    """
    if len(args) != 2:
        print("usage: shieldli copy <src> <dst>")
        sys.exit(1)

    src = Path(args[0])
    dst = Path(args[1])

    # If dst is a directory, dst file should be dst/src.name
    if dst.is_dir():
        actual_dst = dst / src.name
    else:
        actual_dst = dst

    if src.resolve() == actual_dst.resolve():
        print("error: source and destination resolve to the same file:")
        sys.exit(1)

    try:
        shutil.copy2(src, actual_dst)
        print(f"copied {src} to {actual_dst}")
    except OSError as err:
        print(f"error: {err}", file=sys.stderr)
        sys.exit(1)


def cmd_delete(args):
    """Delete a single file.

    :param args: CLI args; must be [path].
    """
    if len(args) != 1:  # Should only have 1 argument, otherwise throw the usage.
        print("error: delete requires <path>")
        print("usage: shieldli delete <path>")
        sys.exit(1)

    path = Path(args[0])
    try:
        path.unlink()
        print(f"deleted {path}")
    except OSError as err:
        print(f"error: {err}", file=sys.stderr)
        sys.exit(1)


def cmd_merge(args):
    if len(args) != 3:
        print("usage: shieldli merge <input1> <input2> <output>", file=sys.stderr)
        sys.exit(1)

    filenames = [Path(args[0]), Path(args[1])]
    output = Path(args[2])
    # Binary concatenation. Works for text files.
    # Output will probably break for images, etc..
    try:
        with open(output, "wb") as outfile:
            for fname in filenames:
                with open(fname, "rb") as infile:
                    outfile.write(infile.read())
    except OSError as err:
        print(f"error: {err}", file=sys.stderr)
        sys.exit(1)


def usage():
    print(
        "usage: shieldli <command> [args]\n"
        "\n"
        "commands:\n"
        "  ls, list <path>                   list files in path (default: './')\n"
        "  cr, create <path>                 create file\n"
        "  cp, copy <src> <dest>             copy file from src to dest\n"
        "  rm, del, delete <path>            delete a file\n"
        "  merge <input2> <input2> <output>  merge two files\n"
        "  help                              show help options"
    )


def cli():
    if len(sys.argv) < 2:  # if there is less than two arguments, show user cmds
        usage()
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    # tried to do a verbose + unix style aliasing
    if command in ("list", "ls"):
        cmd_list(args)
    elif command in ("cr", "create"):
        cmd_create(args)
    elif command in ("copy", "cp"):
        cmd_copy(args)
    elif command in ("delete", "rm", "del"):
        cmd_delete(args)
    elif command in ("merge"):
        cmd_merge(args)
    elif command in ("-h", "--help", "help"):
        usage()
    else:
        print(f"unknown command: {command}")
        usage()
        sys.exit(1)


if __name__ == "__main__":
    cli()
