import getopt
import sys

cmd_str = "test -h -o file --help --output = out file1 file2"
# 只能解析命令行的字符串
opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output="])

if __name__ == "__main__":
    print(opts)    # [('-h', ''), ('-o', 'file'), ('--help', ''), ('--output', '=')]
    print(args)    # ['out', 'file1', 'file2']