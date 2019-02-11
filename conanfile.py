from conans import ConanFile, CMake, tools
import os

class H5cppConan(ConanFile):
    name = "h5cpp"
    version = "0.1.0"
    license = "https://raw.githubusercontent.com/ess-dmsc/h5cpp/master/LICENSE"
    author = "KudzuRunner"
    url = "https://github.com/kudzurunner/conan-h5cpp"
    description = "C++ wrapper for the HDF5 C-library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    requires = (
        "cmake_findboost_modular/1.66.0@bincrafters/stable",
        "boost_system/1.69.0@bincrafters/stable",
        "boost_filesystem/1.69.0@bincrafters/stable",
        "hdf5/1.10.4@kudzurunner/stable",
        "zlib/1.2.11@conan/stable",
        "bzip2/1.0.6@conan/stable")

    source_name = "{}-{}".format(name, version)

    def configure(self):
        self.options["boost_system"].shared = True
        self.options["boost_filesystem"].shared = True
        self.options["hdf5"].shared = True
        self.options["zlib"].shared = True

    def source(self):
        archive_name = "v{}.tar.gz".format(self.version)
        url = "https://github.com/ess-dmsc/h5cpp/archive/{}".format(archive_name)

        tools.download(url, filename=archive_name)
        tools.untargz(filename=archive_name)
        os.remove(archive_name)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.package_folder
        cmake.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
        cmake.configure(source_folder=self.source_name)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.name)

    def package_info(self):
        self.cpp_info.libs = ["h5cpp"]

