if __name__ == '__main__':
    import sys
    from pppat import app

    # If no command line arguments given, assume EiC mode (DEBUG)
    if len(sys.argv) > 1:
        argv = sys.argv[1:]
    else:
        argv = ['resources/PPATConfig_EiC.xml']

    sys.exit(app.run(argv))
