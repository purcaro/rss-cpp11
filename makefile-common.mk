UNAME_S := $(shell uname -s)
CPP = g++-4.8
LOCAL_PATH = $(EXT_PATH)/local
CXXFLAGS = -std=c++11 -DZI_USE_OPENMP -fopenmp -Wall
ifeq ($(UNAME_S),Darwin)
    CXXOPT = -O2 -funroll-loops -DNDEBUG --fast-math
else
    CXXOPT = -O2 -march=native -mtune=native -funroll-loops -DNDEBUG --fast-math
endif
CXXOPT += -DBOOST_UBLAS_NDEBUG
CXXDEBUG = -g -gstabs+
BOOST = -isystem$(LOCAL_PATH)/boost/include -L$(LOCAL_PATH)/boost/lib
CPPCMS = -isystem$(LOCAL_PATH)/cppcms/include
ARAMADILLO = -isystem$(LOCAL_PATH)/armadillo/include
ZI = -I$(LOCAL_PATH)/zi_lib
PUGIXML = -I$(LOCAL_PATH)/pugixml/include
BAMTOOLS = -I$(LOCAL_PATH)/bamtools/include/bamtools
LOCALTOOLS = -I$(LOCAL_PATH)
LIBSVM = -I$(LOCAL_PATH)/libsvm
EXTTOOLS = -I$(EXT_PATH)
SRC = -I./src/

LD_FLAGS = -fopenmp -lz
LD_FLAGS += -lxalan-c -lxerces-c

#pugixml
LD_FLAGS += -Wl,-rpath,$(LOCAL_PATH)/pugixml/lib -L$(LOCAL_PATH)/pugixml/lib  \
	-lpugixml
#boost
LD_FLAGS += -Wl,-rpath,$(LOCAL_PATH)/boost/lib -L$(LOCAL_PATH)/boost/lib  \
	-lpthread -lboost_program_options -lboost_system -lboost_thread \
	-lboost_filesystem -lboost_iostreams -lboost_regex -lboost_serialization
#cppcms
LD_FLAGS += -Wl,-rpath,$(LOCAL_PATH)/cppcms/lib -L$(LOCAL_PATH)/cppcms/lib  \
	-lcppcms -lbooster
#armadillo
LD_FLAGS += -Wl,-rpath,$(LOCAL_PATH)/armadillo/lib \
	-L$(LOCAL_PATH)/armadillo/lib  \
	-larmadillo
#curl
LD_FLAGS += -lcurl

#bamtools
LD_FLAGS += -Wl,-rpath,$(LOCAL_PATH)/bamtools/lib/bamtools \
	-L$(LOCAL_PATH)/bamtools/lib/bamtools\
	-lbamtools

ifeq ($(UNAME_S),Darwin)
    LD_FLAGS += -llapack  -lcblas # non-threaded
    LD_FLAGS += -headerpad_max_install_names
else
    LD_FLAGS += -lrt
    LD_FLAGS += -llapack -lblas
endif

ifndef NO_R
	include $(ROOT)/r-makefile-common.mk
endif

COMLIBS = $(LOCALTOOLS) $(PUGIXML) $(BOOST) $(ZI) $(EXTTOOLS) $(CPPCMS) $(ARAMADILLO) $(BAMTOOLS) $(SRC)
COMMON_OPT = $(CXXFLAGS) $(CXXOPT) $(COMLIBS)
COMMON_DEBUG = $(CXXFLAGS) $(CXXDEBUG) $(COMLIBS)

# from http://stackoverflow.com/a/18258352
rwildcard=$(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2) $(filter $(subst *,%,$2),$d))
