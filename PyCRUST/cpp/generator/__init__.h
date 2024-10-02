#pragma once
#include "PyCRUST.h"
#include "generator/CRYPrimaryGeneratorAction.hh"

void module_register_generator(py::module generator){
  REGISTER_G4GENERATOR(CRYPrimaryGeneratorAction, "CRYPrimaryGeneratorAction");
}
