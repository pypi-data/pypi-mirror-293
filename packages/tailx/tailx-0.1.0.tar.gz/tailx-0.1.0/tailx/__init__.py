import time
from rich import print as print_rich
from rich.panel import Panel
import sys


def tail_f(filepath, n=5, *, nocolor=False):
    """
    【彩色版】tail -f

    filepath: 文件路径
    n: 默认展示行数
    color: 是否使用颜色，默认为 true
    """
    with open(filepath, "rb") as file:
        for _ in range(10):
            try:
                size = file.seek(0, 2)
                if size > 1000 * n:
                    offset = -1000 * n
                    file.seek(offset, 2)
                    lines = file.readlines()[1:]
                else:
                    file.seek(0, 0)
                    lines = file.readlines()
                for line in lines[-n:]:
                    if not nocolor:
                        line = (
                            line.decode()
                            .replace("INFO", "[b]INFO[/]")
                            .replace("SUCCESS", "[green b]SUCCESS[/]")
                            .replace("ERROR", "[red b]ERROR[/]")
                            .replace("CRITICAL", "[white on red b]CRITICAL[/]")
                            .replace("WARNING", "[khaki1 b]WARNING[/]")
                            .replace("DEBUG", "[dodger_blue1 b]DEBUG[/]")
                        )
                        print_rich(line, end="")
                    else:
                        print(line.decode(), end="")
                break
            except Exception:
                continue
        while True:
            try:
                line = file.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                if not nocolor:
                    line = (
                        line.decode()
                        .replace("INFO", "[b]INFO[/]")
                        .replace("SUCCESS", "[green b]SUCCESS[/]")
                        .replace("ERROR", "[red b]ERROR[/]")
                        .replace("CRITICAL", "[white on red b]CRITICAL[/]")
                        .replace("WARNING", "[khaki1 b]WARNING[/]")
                        .replace("DEBUG", "[dodger_blue1 b]DEBUG[/]")
                    )
                    print_rich(line, end="")
                else:
                    print(line.decode(), end="")
            except KeyboardInterrupt:
                break


def main():
    args = sys.argv
    if "--nocolor" in args:
        nocolor = True
        args.remove("--nocolor")
    elif "-no" in args:
        nocolor = True
        args.remove("-no")
    else:
        nocolor = False
    if "-n" in args:
        n = int(args[args.index("-n") + 1])
        args.remove("-n")
        args.remove(str(n))
    else:
        n = 5
    filepath = args[1] if len(args) > 1 else None

    help_string = """[b red]【tailx】(彩色版 tail -f)[/]

用例: tailx [FILEPATH] [-h] [--nocolor] [-n NUM]

参数:
  
  [green]FILEPATH[/]              文件路径
  [green]-no --nocolor[/]         关闭颜色
  [green]-h, --help[/]            帮助信息
  [green]-n NUM[/]                默认行数
  """
    if filepath is None or "--help" in args or "-h" in args:
        print_rich(Panel(help_string, expand=False))
    else:
        tail_f(filepath, n=n, nocolor=nocolor)
