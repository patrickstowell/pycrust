#pragma once
#include "PyCRUST.h"

void module_register_detector(py::module detector){
  REGISTER_G4DETECTOR(ExampleUserDetectorConstruction, "ExampleUserDetectorConstruction");
}
