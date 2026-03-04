find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_MODULATOR gnuradio-modulator)

FIND_PATH(
    GR_MODULATOR_INCLUDE_DIRS
    NAMES gnuradio/modulator/api.h
    HINTS $ENV{MODULATOR_DIR}/include
        ${PC_MODULATOR_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_MODULATOR_LIBRARIES
    NAMES gnuradio-modulator
    HINTS $ENV{MODULATOR_DIR}/lib
        ${PC_MODULATOR_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-modulatorTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_MODULATOR DEFAULT_MSG GR_MODULATOR_LIBRARIES GR_MODULATOR_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_MODULATOR_LIBRARIES GR_MODULATOR_INCLUDE_DIRS)
