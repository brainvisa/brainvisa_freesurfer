cmake_minimum_required( VERSION 2.6 )
find_package( brainvisa-cmake REQUIRED )
BRAINVISA_PROJECT()

BRAINVISA_FIND_PACKAGE( soma-base REQUIRED )
BRAINVISA_FIND_PACKAGE( axon REQUIRED )

find_package( PyQt${DESIRED_QT_VERSION} REQUIRED )
find_package( python REQUIRED )

BRAINVISA_DEPENDENCY( RUN DEPENDS "axon" RUN ">= ${axon_VERSION_MAJOR}.${axon_VERSION_MINOR}" )
BRAINVISA_DEPENDENCY( RUN DEPENDS "morphologist-gpl" RUN "= ${anatomist-gpl_VERSION}" )

BRAINVISA_COPY_PYTHON_DIRECTORY( "${CMAKE_CURRENT_SOURCE_DIR}/python"
                                 ${PROJECT_NAME} )
BRAINVISA_COPY_PYTHON_DIRECTORY( "${CMAKE_CURRENT_SOURCE_DIR}/brainvisa"
                                 ${PROJECT_NAME} )

BRAINVISA_COPY_DIRECTORY( "${CMAKE_CURRENT_SOURCE_DIR}/scripts"
                          scripts
                          ${PROJECT_NAME} )


# BRAINVISA_CREATE_CMAKE_CONFIG_FILES()


