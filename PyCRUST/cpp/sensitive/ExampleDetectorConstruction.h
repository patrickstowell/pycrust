#include "G4UserSteppingAction.hh"

class ExampleUserSteppingAction : public G4UserSteppingAction {
public:
  void UserSteppingAction(const G4Step* step) override {
    std::cout << "Calling Example UserSteppingAction" << std::endl;
  }
};
