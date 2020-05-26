import sys
import subprocess

from faf.tools import glob

def unique_id(session):
    # TODO - do we need the WMI service check on Windows?
    # TODO - path
    if sys.platform == 'win32':
        exe_path = f"{glob.ROOT_PATH}\\tools\\faf-uid.exe"
    else:
        exe_path = f"{glob.ROOT_PATH}\\tools\\faf-uid"
    try:
        uid_p = subprocess.Popen([exe_path, session], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = uid_p.communicate()
        if uid_p.returncode != 0:
            return None
        else:
            return out.decode('utf-8')
    except OSError:
        return None
