#include "PyCRUST.h"
#include "actions/ExampleUserSteppingAction.h"

void module_register_stepping(py::module stepping){
  REGISTER_G4STEPPING(pc::ExampleUserSteppingAction, "ExampleUserSteppingAction");
}
