import sys

if sys.argv[0] is not None and len(sys.argv[0]) > 0:
    with open(sys.argv[0]) as f:
        if "import ayw as nb" in f.read():
            print("ayw NB")
        else:
            print("nb")
else:
    print("ayw NB!!!")
