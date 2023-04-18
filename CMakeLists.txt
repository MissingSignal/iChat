# Copyright: (C) Robotics Brain and Cognitive Sciences (RBCS) - Istituto Italiano di Tecnologia
# Authors: Luca Garello
# CopyPolicy: Released under the terms of the GNU GPL v2.0.

cmake_minimum_required(VERSION 3.12)
project(iChat)


#we need ICUBcontrib and YARP
find_package(ICUBcontrib REQUIRED)
find_package(YARP REQUIRED)

list(APPEND CMAKE_MODULE_PATH ${ICUBCONTRIB_MODULE_PATH})

include(ICUBcontribHelpers)
include(ICUBcontribOptions)
icubcontrib_set_default_prefix()

add_subdirectory(modules)
add_subdirectory(app)

icubcontrib_add_uninstall_target()  



#print all env variables
# get_cmake_property(_variableNames VARIABLES)
# list (SORT _variableNames)
# foreach (_variableName ${_variableNames})
#     message(STATUS "${_variableName}=${${_variableName}}")
# endforeach()

