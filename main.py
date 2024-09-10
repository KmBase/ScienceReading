if __name__ == '__main__':
    import sys
    import os
    cwd = os.path.dirname(__file__)
    print(cwd)
    os.chdir(cwd)
    sys.path.append(os.path.abspath('src'))
    import entry
    main_path = os.path.join(cwd,'embedded',".main")
    entry.main(main_path)