import kiskadee
import tarfile
import zipfile


class Plugin(kiskadee.plugins.Plugin):
    def get_sources(self):
        #  https://samate.nist.gov/SRD/testsuites/juliet/Juliet_Test_Suite_v1.2_for_C_Cpp.zip
        tarball = None
        return tarball

    def watch(self):
        pass
