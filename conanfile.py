from conans import ConanFile, CMake, tools
import os
import glob
import shutil


class H5cppConan(ConanFile):
    name = "h5cpp"
    version = "0.1.3"
    license = "https://raw.githubusercontent.com/ess-dmsc/h5cpp/master/LICENSE"
    author = "KudzuRunner"
    url = "https://github.com/kudzurunner/conan-h5cpp"
    description = "C++ wrapper for the HDF5 C-library"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    requires = (
        "hdf5/1.10.5@kudzurunner/stable",
        "boost/1.71.0",
        "zlib/1.2.11",
        "bzip2/1.0.8")

    source_name = "{}-{}".format(name, version)
    suffix = ""


    def configure(self):
        self.options["boost"].shared = True
        self.options["hdf5"].shared = True
        self.options["zlib"].shared = True

    def source(self):
        archive_name = "v{}.tar.gz".format(self.version)
        url = "https://github.com/ess-dmsc/h5cpp/archive/{}".format(archive_name)

        tools.download(url, filename=archive_name)
        tools.untargz(filename=archive_name)
        os.remove(archive_name)

        self.suffix = ("_d" if self.settings.build_type == "Debug" else "")
        tools.replace_in_file(
            "{}/cmake/EnsureBuildType.cmake".format(self.source_name), "endif()",
            '''endif()
            
if(NOT CMAKE_DEBUG_POSTFIX)
  set(CMAKE_DEBUG_POSTFIX {})
endif()'''.format(self.suffix))

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
        self.cpp_info.libs = ["h5cpp"+self.suffix]

