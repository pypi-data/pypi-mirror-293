
import os
from ._src import mcnparse

def main() -> None:
    dir = os.getcwd()
    mcnparse(dir)

if __name__=="__main__":
    main()
