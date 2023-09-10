import os, sys

if __name__ == "__main__":
    init_path = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(init_path, "src/")
    os.chdir(init_path)
    sys.path.insert(0, src_path)

    import src
    src.Game()
