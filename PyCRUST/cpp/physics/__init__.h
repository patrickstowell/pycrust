#pragma once
#include "PyCRUST.h"
#include "pybind11/stl_bind.h"
#include <pybind11/pybind11.h>
#include <vector>
#include <algorithm>
#include "FTFP_BERT.hh"
#include "physics/OpticalPhysics.hh"
#include "G4VModularPhysicsList.hh"
#include "G4VPhysicsConstructor.hh"
#include "G4OpticalPhysics.hh"
// #define ADD_PHYSICS_LIST(plname) \
//   py::class_<plname, G4VModularPhysicsList, G4VUserPhysicsList,\
//   std::unique_ptr<plname,py::nodelete>>(m, #plname)\
//   .def(py::init<>());\
//   AddPhysicsList(#plname);


void AddOpticalPhysics(G4VModularPhysicsList* list){
    
    auto opticalPhysics = new G4OpticalPhysics();
    auto opticalParams = G4OpticalParameters::Instance();
    opticalParams->SetBoundaryInvokeSD(true);
    list->RegisterPhysics(opticalPhysics);
}

void module_register_physics(py::module physics) {

  py::class_<OpticalPhysics,G4VModularPhysicsList>(physics, "OpticalPhysics")
  .def(py::init<>());

    physics.def("AddOpticalPhysics", &AddOpticalPhysics);

}
