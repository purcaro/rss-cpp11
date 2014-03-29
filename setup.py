#!/usr/bin/python

# by purcaro@gmail.com

import subprocess, sys, os, argparse
from scripts.utils import Utils
from collections import namedtuple

BuildPaths = namedtuple("BuildPaths", 'url build_dir build_sub_dir local_dir')

def shellquote(s):
    # from http://stackoverflow.com/a/35857
    return "'" + s.replace("'", "'\\''") + "'"

def isMac():
    return sys.platform == "darwin"

class Paths():
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "external"))
        self.ext_tars = os.path.join(self.base_dir, "tarballs")
        self.ext_build = os.path.join(self.base_dir, "build")
        self.install_dir = os.path.join(self.base_dir, "local")
        Utils.mkdir(self.ext_tars)
        Utils.mkdir(self.ext_build)
        self.paths = {}
        self.paths["zi_lib"] = self.__zi_lib()
        self.paths["cppitertools"] = self.__cppitertools()
        self.paths["boost"] = self.__boost()
        self.paths["cppcms"] = self.__cppcms()
        self.paths["pugixml"] = self.__pugixml()

    def path(self, name):
        if name in self.paths:
            return self.paths[name]
        raise Exception(name + " not found in paths")

    def __zi_lib(self):
        url = 'https://github.com/weng-lab/zi_lib.git'
        local_dir = os.path.join(self.install_dir, "zi_lib")
        return BuildPaths(url, '', '', local_dir)

    def __bamtools(self):
        url = 'https://github.com/pezmaster31/bamtools.git'
        name = "bamtools"
        build_dir = os.path.join(self.ext_build, name)
        fn = os.path.basename(url)
        fn_noex = fn.replace(".git", "")
        build_sub_dir = os.path.join(build_dir, fn_noex)
        local_dir = os.path.join(self.install_dir, name)
        return BuildPaths(url, build_dir, build_sub_dir, local_dir)

    def __cppitertools(self):
        url = 'https://github.com/ryanhaining/cppitertools.git'
        local_dir = os.path.join(self.install_dir, "cppitertools")
        return BuildPaths(url, '', '', local_dir)

    def __Rdevel(self):
        url = "ftp://ftp.stat.math.ethz.ch/Software/R/R-devel.tar.gz"
        return self.__package_dirs(url, "R-devel")

    def __boost(self):
        url = "http://downloads.sourceforge.net/project/boost/boost/1.55.0/boost_1_55_0.tar.gz"
        return self.__package_dirs(url, "boost")

    def __pugixml(self):
        url = "http://github.com/zeux/pugixml/releases/download/v1.4/pugixml-1.4.tar.gz"
        return self.__package_dirs(url, "pugixml")

    def __armadillo(self):
        url = "http://freefr.dl.sourceforge.net/project/arma/armadillo-4.000.2.tar.gz"
        return self.__package_dirs(url, "armadillo")

    def __mlpack(self):
        url = "http://www.mlpack.org/files/mlpack-1.0.8.tar.gz"
        return self.__package_dirs(url, "mlpack")

    def __liblinear(self):
        url = "http://www.csie.ntu.edu.tw/~cjlin/liblinear/liblinear-1.94.tar.gz"
        return self.__package_dirs(url, "liblinear")

    def __libsvm(self):
        url = "http://www.csie.ntu.edu.tw/~cjlin/libsvm/libsvm-3.17.tar.gz"
        return self.__package_dirs(url, "libsvm")

    def __cppcms(self):
        url = "http://freefr.dl.sourceforge.net/project/cppcms/cppcms/1.0.4/cppcms-1.0.4.tar.bz2"
        return self.__package_dirs(url, "cppcms")

    def __mathgl(self):
        url = "http://freefr.dl.sourceforge.net/project/mathgl/mathgl/mathgl%202.2.1/mathgl-2.2.1.tar.gz"
        return self.__package_dirs(url, "mathgl")

    def __package_dirs(self, url, name):
        build_dir = os.path.join(self.ext_build, name)
        fn = os.path.basename(url)
        fn_noex = fn.replace(".tar.gz", "").replace(".tar.bz2", "")
        build_sub_dir = os.path.join(build_dir, fn_noex)
        local_dir = os.path.join(self.install_dir, name)
        return BuildPaths(url, build_dir, build_sub_dir, local_dir)

class Setup:
    def __init__(self, args):
        self.paths = Paths()
        self.args = args
        self.__processArgs()

    def __processArgs(self):
        dirs = self.args.dirsToDelete
        if not dirs:
            return

        if "all" == dirs[0]:
            dirs = []
            for k, _ in self.paths.paths.iteritems():
                dirs.append(k)

        for e in dirs:
            p = self.__path(e)
            if p.build_dir:
                Utils.rm_rf(p.build_dir)
            if p.local_dir:
                Utils.rm_rf(p.local_dir)

    def __path(self, name):
        return self.paths.path(name)

    def __setup(self, name, builder_f):
        if os.path.exists(self.__path(name).local_dir):
            print name, "found"
        else:
            print name, "NOT found; building..."
            builder_f()

    def setup(self):
        self.__setup("zi_lib", self.zi_lib)
        self.__setup("cppitertools", self.cppitertools)
        self.__setup("boost", self.boost)
        self.__setup("cppcms", self.cppcms)
        self.__setup("pugixml", self.pugixml)

    def num_cores(self):
        c = Utils.num_cores()
        if c > 8:
            return c/2
        if 1 == c:
            return 1
        return c - 1

    def __build(self, i, cmd):
        print "\t getting file..."
        fnp = Utils.get_file_if_size_diff(i.url, self.paths.ext_tars)
        Utils.clear_dir(i.build_dir)
        Utils.untar(fnp, i.build_dir)
        try:
            Utils.run_in_dir(cmd, i.build_sub_dir)
        except:
            Utils.rm_rf(i.local_dir)
            sys.exit(1)

    def boost(self):
        i = self.__path("boost")
        if isMac():
          cmd = """echo "using darwin : 3.2 : /usr/local/bin/g++-3.2 ;  " >> tools/build/v2/user-config.jam && ./bootstrap.sh --prefix={local_dir} && ./b2 -d 2 toolset=darwin-4.8 -j {num_cores} install && install_name_tool -change libboost_system.dylib {local_dir}/lib/libboost_system.dylib {local_dir}/lib/libboost_thread.dylib && install_name_tool -change libboost_system.dylib {local_dir}/lib/libboost_system.dylib {local_dir}/lib/libboost_filesystem.dylib""".format(local_dir=shellquote(i.local_dir).replace(' ', '\ '), num_cores=self.num_cores())
          #cmd = """echo "using gcc : 4.8 : /usr/local/bin/g++-4.8 ; " >> tools/build/v2/user-config.jam &&
          # ./bootstrap.sh --prefix={local_dir} && ./bjam --toolset=gcc-4.8 -j {num_cores} install
          #  """.format(
          #             local_dir=shellquote(i.local_dir).replace(' ', '\ '), num_cores=self.num_cores())
        else:
          cmd = """echo "using gcc : 4.8 : /usr/bin/g++-4.8 ; " >> tools/build/v2/user-config.jam &&./bootstrap.sh --prefix={local_dir} && ./b2 -d 2 toolset=gcc-4.8 -j {num_cores} install""".format(local_dir=shellquote(i.local_dir).replace(' ', '\ '), num_cores=self.num_cores())
        self.__build(i, cmd)
          #cmd = """echo "using gcc : 4.8 : /usr/bin/g++-4.8 ; " >> tools/build/v2/user-config.jam &&
          # ./bootstrap.sh --prefix={local_dir} && ./bjam --toolset=gcc-4.8 -j {num_cores} install
          # """.format(
          #            local_dir=shellquote(i.local_dir).replace(' ', '\ '), num_cores=self.num_cores())
          #self.__build(i, cmd)

    def Rdevel(self):
        i = self.__path("R-devel")
        cmd = ""
        if isMac():
          cmd = """
            ./configure --prefix={local_dir} --enable-R-shlib CC=gcc-4.8 CXX=g++-4.8
            && make -j {num_cores}
            && make install
            && echo 'install.packages(c(\"ape\", \"ggplot2\", \"seqinr\",\"Rcpp\", \"RInside\"), repos=\"http://cran.us.r-project.org\")' | $({local_dir}/R.framework/Resources/bin/R RHOME)/bin/R --slave --vanilla
            """.format(local_dir=shellquote(i.local_dir).replace(' ', '\ '), num_cores=self.num_cores())
        else:
          cmd = """
            ./configure --prefix={local_dir} --enable-R-shlib CC=gcc-4.8 CXX=g++-4.8
            && make -j {num_cores}
            && make install
            && echo 'install.packages(c(\"ape\", \"ggplot2\", \"seqinr\",\"Rcpp\", \"RInside\"), repos=\"http://cran.us.r-project.org\")' | $({local_dir}/lib/R/bin/R RHOME)/bin/R --slave --vanilla
            """.format(local_dir=shellquote(i.local_dir).replace(' ', '\ '), num_cores=self.num_cores())


        cmd = " ".join(cmd.split())
        self.__build(i, cmd)

    def bamtools(self):
        i = self.__path('bamtools')
        cmd = "git clone {url} {d}".format(url=i.url, d=i.build_dir)
        Utils.run(cmd)
        i = self.__path('bamtools')
        cmd = "mkdir -p build && cd build && CC=gcc-4.8 CXX=g++-4.8 cmake -DCMAKE_INSTALL_PREFIX:PATH={local_dir} .. && make -j {num_cores} install".format(
            local_dir=shellquote(i.local_dir), num_cores=self.num_cores())
        Utils.run_in_dir(cmd, i.build_dir)

    def cppcms(self):
        i = self.__path('cppcms')
        if(sys.platform == "darwin"):
            cmd = "mkdir -p build && cd build && CC=gcc-4.8 CXX=g++-4.8 cmake -DCMAKE_INSTALL_PREFIX:PATH={local_dir} .. && make -j {num_cores} install && install_name_tool -change libbooster.0.dylib {local_dir}/lib/libbooster.0.dylib {local_dir}/lib/libcppcms.1.dylib".format(local_dir=shellquote(i.local_dir), num_cores=self.num_cores())
        else:
            cmd = "mkdir -p build && cd build && CC=gcc-4.8 CXX=g++-4.8 cmake -DCMAKE_INSTALL_PREFIX:PATH={local_dir} .. && make -j {num_cores} install ".format(local_dir=shellquote(i.local_dir), num_cores=self.num_cores())

        self.__build(i, cmd)

    def armadillo(self):
        i = self.__path('armadillo')
        cmd = "mkdir -p build && cd build && CC=gcc-4.8 CXX=g++-4.8 cmake -DCMAKE_INSTALL_PREFIX:PATH={local_dir} .. && make -j {num_cores} install".format(
            local_dir=shellquote(i.local_dir), num_cores=self.num_cores())
        self.__build(i, cmd)

    def pugixml(self):
        i = self.__path('pugixml')
        cmd = "cd scripts && CC=gcc-4.8 CXX=g++-4.8 cmake -DCMAKE_INSTALL_PREFIX:PATH={local_dir} CMakeLists.txt && make -j {num_cores} install".format(
            local_dir=shellquote(i.local_dir), num_cores=self.num_cores())
        self.__build(i, cmd)

    def liblinear(self):
        i = self.__path('liblinear')
        cmd = "make && mkdir -p {local_dir} && cp predict train {local_dir}".format(
            local_dir=shellquote(i.local_dir))
        self.__build(i, cmd)

    def libsvm(self):
        i = self.__path('libsvm')
        cmd = "make && make lib && mkdir -p {local_dir} && cp -a * {local_dir}".format(
            local_dir=shellquote(i.local_dir))
        self.__build(i, cmd)

    def mlpack(self):
        i = self.__path('mlpack')
        armadillo_dir = shellquote(i.local_dir).replace("mlpack", "armadillo")
        boost_dir = shellquote(i.local_dir).replace("mlpack", "boost")
        cmd = """
mkdir -p build
&& cd build
&& CC=gcc-4.8 CXX=g++-4.8 cmake -D DEBUG=OFF -D PROFILE=OFF
         -D ARMADILLO_LIBRARY={armadillo_dir}/lib/libarmadillo.so.4.0.2
         -D ARMADILLO_INCLUDE_DIR={armadillo_dir}/include/
         -D CMAKE_INSTALL_PREFIX:PATH={local_dir} ..
&& make -j {num_cores} install
""".format(local_dir=shellquote(i.local_dir), armadillo_dir=armadillo_dir, num_cores=self.num_cores())
        cmd = " ".join(cmd.split('\n'))
        self.__build(i, cmd)

    def mathgl(self):
        i = self.__path('mathgl')
        cmd = "mkdir -p build && cd build && CC=gcc-4.8 CXX=g++-4.8 cmake -DCMAKE_INSTALL_PREFIX:PATH={local_dir} .. && make -j {num_cores} install".format(
            local_dir=shellquote(i.local_dir), num_cores=self.num_cores())
        self.__build(i, cmd)

    def __git(self, i):
        cmd = "git clone {url} {d}".format(url=i.url, d=shellquote(i.local_dir))
        Utils.run(cmd)

    def zi_lib(self):
        self.__git(self.__path('zi_lib'))

    def cppitertools(self):
        self.__git(self.__path('cppitertools'))
        i = self.__path('cppitertools')
        cmd = "cd {d} && git checkout d4f79321842dd584f799a7d51d3e066a2cdb7cac".format(d=shellquote(i.local_dir))
        Utils.run(cmd)

    def ubuntu(self):
        pkgs = """libbz2-dev python2.7-dev cmake libpcre3-dev zlib1g-dev libgcrypt11-dev libicu-dev
python doxygen doxygen-gui auctex xindy graphviz libcurl4-openssl-dev""".split()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dirsToDelete', type=str, nargs='*')
    return parser.parse_args()

def main():
    args = parse_args()
    s = Setup(args)
    s.setup()
main()
