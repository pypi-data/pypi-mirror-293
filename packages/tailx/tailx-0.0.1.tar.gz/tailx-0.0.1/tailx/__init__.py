import time
from rich import print as print_rich
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
                file.seek(-1000 * n, 2)
                for line in file.readlines()[1:][-n:]:
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
    else:
        nocolor = False
    filepath = sys.argv[1] if len(args) > 1 else None

    help_string = """usage: tailx [FILEPATH] [-h] [--nocolor] 

【彩色版】tail -f

options:
  
  [green]FILEPATH[/]              文件路径
  [green]--nocolor[/]             关闭颜色
  [green]-h, --help[/]            帮助信息"""
    if filepath is None or "--help" in args or "-h" in args:
        print_rich(help_string)
    else:
        tail_f(filepath, nocolor=nocolor)
