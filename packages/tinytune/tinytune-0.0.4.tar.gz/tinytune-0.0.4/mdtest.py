from markdownify import markdownify
import sys

with open(sys.argv[1]) as fp:
    print(markdownify(fp.read()))
