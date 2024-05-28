# CROSS COMPILER SETTING
#SET(CMAKE_SYSTEM_NAME Generic)
#CMAKE_MINIMUM_REQUIRED (VERSION 3.10.0)

SET(SdkRootDirPath .)

#literal is ok
include(miniflags.cmake)

#
include(${SdkRootDirPath}/flags.cmake)
