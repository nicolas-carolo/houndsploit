def check_file_existence(filename):
    try:
        f = open(filename)
        f.close()
        return True
    except IOError:
        return False
        