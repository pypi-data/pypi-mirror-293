from random import Random
from random import randint as rdi

__all__ = [
    "check",
    "FS"
]

class FS:
    def FS(self):
        return self
    

    def check():
        print("First Package")

_fs = FS()
check = _fs.check
FS = _fs.FS

if __name__ == '__main__':
    print("Hello Aakash")
    print(Random().randint(1, 20))
    print(rdi(8, 60))