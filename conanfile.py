from conans import *
import subprocess

class GoogleMockConan(ConanFile):
    name = 'googlemock'
    version = '1.7.0'
    settings = ['os', 'compiler', 'build_type']
    generators = ['cmake']
    exports = subprocess.check_output(['git', 'ls-files']).split()
    options = {
        'BUILD_SHARED_LIBS':      ['ON', 'OFF'], # Build shared libraries (DLLs).
        'gmock_build_tests':      ['ON', 'OFF'], # Build all of Google Mock's own tests.
        'gtest_disable_pthreads': ['ON', 'OFF'], # Disable uses of pthreads in gtest.

        # Set this to 0 if your project already uses a tuple library, and GTest should use that library
        # Set this to 1 if GTest should use its own tuple library
        'GTEST_USE_OWN_TR1_TUPLE': [None, '0', '1'],

        # Set this to 0 if GTest should not use tuple at all. All tuple features will be disabled
        'GTEST_HAS_TR1_TUPLE': [None, '0'],

        # If GTest incorrectly detects whether or not the pthread library exists on your system, you can force it
        # by setting this option value to:
        #   1 - if pthread does actually exist
        #   0 - if pthread does not actually exist
        'GTEST_HAS_PTHREAD': [None, '0', '1']
    }
    default_options = (
                        'BUILD_SHARED_LIBS=OFF',
                        'gmock_build_tests=OFF',
                        'gtest_disable_pthreads=OFF',
                        'GTEST_USE_OWN_TR1_TUPLE=None',
                        'GTEST_HAS_TR1_TUPLE=None',
                        'GTEST_HAS_PTHREAD=None'
                      )

    build_dir = 'build'

    def requirements(self):
        # We no longer pass through options to googletest as the API for this function has changed.
        # See history for this file
        self.requires('googletest/1.7.0@azriel91/testing')

    def build(self):
        option_defines = ' '.join("-D%s=%s" % (opt, val) for (opt, val) in self.options.iteritems() if val is not None)
        self.run("cmake . -B{build_dir} {defines}".format(build_dir=self.build_dir, defines=option_defines))
        self.run("cmake --build {build_dir}".format(build_dir=self.build_dir))

    def package(self):
        self.copy('*', dst='cmake', src='cmake')
        self.copy('*', dst='include', src='include')
        self.copy('CMakeLists.txt', dst='.', src='.')

        # Meta files
        self.copy('CHANGES', dst='.', src='.')
        self.copy('CONTRIBUTORS', dst='.', src='.')
        self.copy('LICENSE', dst='.', src='.')
        self.copy('README', dst='.', src='.')

        # Built artifacts
        lib_dir = "{build_dir}/lib".format(build_dir=self.build_dir)
        if self.options['BUILD_SHARED_LIBS'] == 'ON':
            self.copy('libgmock.so', dst='lib', src=lib_dir)
            self.copy('libgmock_main.so', dst='lib', src=lib_dir)
        else:
            self.copy('libgmock.a', dst='lib', src=lib_dir)
            self.copy('libgmock_main.a', dst='lib', src=lib_dir)

        # IDE sample files
        # self.copy('*', dst='make', src='make')
        # self.copy('*', dst='msvc', src='msvc')

        # Autoconf/Automake
        # self.copy('configure.ac', dst='configure.ac', src='.')
        # self.copy('Makefile.am', dst='Makefile.am', src='.')

        # Files not used by downstream
        # self.copy('*', dst='build-aux', src='build-aux')
        # self.copy('*', dst='scripts', src='scripts')
        # self.copy('*', dst='src', src='src')
        # self.copy('*', dst='test', src='test')

    def package_info(self):
        self.cpp_info.libs.append('gmock')
