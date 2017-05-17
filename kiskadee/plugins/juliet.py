import kiskadee
import urllib.request
import shutil
import os.path


class Plugin(kiskadee.plugins.Plugin):
    def get_sources(self, name, version, *args, **kwargs):
        juliet_url = 'https://samate.nist.gov/SRD/testsuites/juliet/Juliet_Test_Suite_v1.2_for_C_Cpp.zip'
        zipfile_name = os.path.basename(juliet_url)
        # TODO: set proper temp dir for compressed file in conf file
        zipfile_path = os.path.join('/tmp/', zipfile_name)

        with urllib.request.urlopen(juliet_url) as response, open(zipfile_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return zipfile_path

    def watch(self):
        """SAMATE does not provide a proper API to inspect new Juliet versions.
        It should not matter, since Juliet does not receive updates frequently.
        """
        pass
