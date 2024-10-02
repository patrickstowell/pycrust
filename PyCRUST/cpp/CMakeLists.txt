cmake_minimum_required(VERSION 2.6 FATAL_ERROR)
project(PyCRUST)

find_package(Geant4 REQUIRED ui_all vis_all)
find_package(PythonLibs REQUIRED)

include(${Geant4_USE_FILE})
include_directories(${PYTHON_INCLUDE_DIRS})
include_directories(${PROJECT_SOURCE_DIR}/)
include_directories(/usr/local/include)

find_package(pybind11)

SET(LIBRARY_OUTPUT_PATH "..")

pybind11_add_module(_PyCRUST SHARED PyCRUSTModule.cxx)
target_link_libraries(_PyCRUST PRIVATE ${Geant4_LIBRARIES} pybind11::embed)
set_target_properties(_PyCRUST PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
target_include_directories(_PyCRUST PRIVATE ${Geant4_INCLUDES} ${PYTHON_INCLUDE_DIRS})

install(TARGETS _PyCRUST
    LIBRARY DESTINATION ../)

