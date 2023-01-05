def download_exploit_file(vulnerability):
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        copyfile(file_path, os.path.expanduser("~") + "/exploit_" + vulnerability.id + vulnerability.get_extension())
        download_msg = "exploit_" + vulnerability.id + vulnerability.get_extension() + " has been downloaded in your home directory"
        return True, download_msg
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return False, error_msg