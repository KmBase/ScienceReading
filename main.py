
if __name__ == '__main__':
    import sys, os, site
    cwd = os.path.dirname(__file__)
    os.chdir(cwd)
    sys.path.append(os.path.abspath('app'))
    libs = cwd+"\embedded\site-packages"
    sys.path.append(os.path.abspath(libs))
    if os.path.exists(libs):
        site.addsitedir(libs)
    import app
    main_path = os.path.join(cwd,'main.py')
    app.run(main_path)