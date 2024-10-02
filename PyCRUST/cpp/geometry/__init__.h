#pragma once
#include "PyCRUST.h"
#include "util/GeometryUtils.h"

void module_register_util(py::module util){
  REGISTER_G4UTIL(GetDensityAtPosition, "GetDensityAtPosition");
  REGISTER_G4UTIL(InitializeScoring, "InitializeScoring");
}
