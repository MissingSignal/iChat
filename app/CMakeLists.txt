# Copyright: (C) Robotics Brain and Cognitive Sciences (RBCS) - Istituto Italiano di Tecnologia
# Authors: Luca Garello
# CopyPolicy: Released under the terms of the GNU GPL v2.0.

cmake_minimum_required(VERSION 3.12)


file(GLOB scripts  ${CMAKE_CURRENT_SOURCE_DIR}/scripts/*.template)
file(GLOB conf_ini ${CMAKE_CURRENT_SOURCE_DIR}/conf/*.ini)


yarp_install(FILES ${conf_ini} DESTINATION ${ICUBCONTRIB_CONTEXTS_INSTALL_DIR}/${PROJECTNAME})
yarp_install(FILES ${scripts}  DESTINATION ${ICUBCONTRIB_APPLICATIONS_TEMPLATES_INSTALL_DIR})

# yarp_install(FILES ${conf} DESTINATION ${ICUBCONTRIB_CONTEXTS_INSTALL_DIR}/${appname})
# yarp_install(FILES ${joint_files} DESTINATION ${ICUBCONTRIB_CONTEXTS_INSTALL_DIR}/${appname})

# # in theory,  you should install the template, then customize it 
# yarp_install(FILES ${scripts} DESTINATION ${ICUBCONTRIB_APPLICATIONS_TEMPLATES_INSTALL_DIR})

# # in practice, you can directly use the template 
# yarp_install(FILES ${scripts} DESTINATION ${ICUBCONTRIB_APPLICATIONS_INSTALL_DIR})

