import sys
import subprocess


class Tools:
    def __init__(self, paths):
        self.root = paths.ROOT_PATH

    def unique_id(self, session):
        # TODO - do we need the WMI service check on Windows?
        if sys.platform == 'win32':
            exe_path = f"{self.root}\\tools\\faf-uid.exe"
        else:
            exe_path = f"{self.root}\\tools\\faf-uid"
        try:
            uid_p = subprocess.Popen([exe_path, session],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            out, err = uid_p.communicate()
            if uid_p.returncode != 0:
                return None
            else:
                return out.decode('utf-8')
        except OSError:
            return None
