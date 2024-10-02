#include "PyCRUST.h"
#include "actions/__init__.h"
#include "util/__init__.h"
#include "geometry/__init__.h"
#include "analysis/__init__.h"
#include "physics/__init__.h"

// #include "generator/__init__.h"
// #include "detector/__init__.h"

#include "pybind11/stl.h"
#include "pybind11/pybind11.h"
#include "deps/pybind11_json.hpp"

namespace py = pybind11;

REGISTER_PCMODULE(_PyCRUST, "Main PyCrust Module");

py::bind_vector<std::vector<double>>(m, "VectorDouble");
py::bind_map<std::map<std::string, double>>(m, "MapStringDouble");
py::bind_map<std::map<std::string, bool>>(m, "MapStringBool");

module_register_stepping(stepping);
module_register_util(util);
// module_register_generator(generator);
module_register_geometry(geometry);
module_register_analysis(analysis);
module_register_physics(physics);

FINALIZE_PCMODULE();


