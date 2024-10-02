#include "G4UserSteppingAction.hh"
#include <iostream>

namespace pc {
class ExampleUserSteppingAction : public G4UserSteppingAction {
public:
  void UserSteppingAction(const G4Step* step) override {
    std::cout << "Calling Example UserSteppingAction" << std::endl;
  }
};
}
