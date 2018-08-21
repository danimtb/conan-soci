import os
from conans import ConanFile, CMake, tools


class SociConan(ConanFile):
    name = "soci"
    version = "3.2.3"
    license = "Boost Software License"
    url = "https://github.com/SOCI/soci"
    description = "Originally, SOCI was developed by Maciej Sobczak at CERN as abstraction layer for Oracle, a " \
                  "Simple Oracle Call Interface. Later, several database backends have been developed for SOCI, " \
                  "thus the long name has lost its practicality. Currently, if you like, SOCI may stand for " \
                  "Simple Open (Database) Call Interface or something similar."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    source_subfolder = "source_subfolder"

    def source(self):
        tools.get("https://github.com/SOCI/%s/archive/%s.zip" % (self.name, self.version))
        os.rename("soci-3.2.3", self.source_subfolder)
        tools.replace_in_file("%s/src/CMakeLists.txt" % self.source_subfolder, "project(SOCI)", """project(SOCI)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["SOCI_SHARED"] = self.options.shared
        cmake.definitions["SOCI_STATIC"] = not self.options.shared
        cmake.definitions["WITH_BOOST"] = False
        cmake.definitions["WITH_ORACLE"] = False
        cmake.configure(source_folder="%s/src" % self.source_subfolder)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)