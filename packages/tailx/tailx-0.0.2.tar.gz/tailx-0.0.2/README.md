# tailx

带颜色的 `tail -f`, 更好看的查看日志。

## 安装

```
pip install tailx
```

## 用例

tailx [文件路径] [-no] [--nocolor] [-h] [--help] [-n Num]

## 查看帮助

```bash
tailx -h
tailx --help
```

## 彩色输出示例

```bash
tailx path/to/file.log
```

### 无颜色输出示例

```bash
tailx path/to/file.log -no
tailx path/to/file.log --nocolor
```

## 默认行数

```bash
tailx path/to/file.log -n 10
```
