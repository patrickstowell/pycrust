#pragma once

#include "G4Includes.hh"

#include "pybind11/stl.h"
#include "pybind11/pybind11.h"

namespace py = pybind11;

#define REGISTER_G4DETECTOR(ClassType, ClassName)\
        py::class_<ClassType, G4VUserDetectorConstruction>(detector, ClassName)\
                .def(py::init<>())\
                .def("UserSteppingAction", &ClassType::UserSteppingAction);

#define REGISTER_G4GEOMETRY(ClassType, ClassName)\
        geometry.def(ClassName, &ClassType);

#define REGISTER_G4PHYSICS(ClassType, ClassName)\
        py::class_<ClassType, G4VUserPhysicsList>(physics, ClassName)\
                .def(py::init<>())\
                .def("UserSteppingAction", &ClassType::UserSteppingAction);

#define REGISTER_G4RUN(ClassType, ClassName)\
        py::class_<ClassType, G4UserRunAction>(run, ClassName)\
                .def(py::init<>())\
                .def("UserSteppingAction", &ClassType::UserSteppingAction)

#define REGISTER_G4GENERATOR(ClassType, ClassName)\
        py::class_<ClassType, G4VUserPrimaryGeneratorAction>(generator, ClassName)\
                .def(py::init<>())\
                .def("UserSteppingAction", &ClassType::UserSteppingAction)

#define REGISTER_G4EVENT(ClassType, ClassName)\
        py::class_<ClassType, G4UserEventAction>(event, ClassName)\
                .def(py::init<>())\
                .def("UserSteppingAction", &ClassType::UserSteppingAction)

#define REGISTER_G4STACKING(ClassType, ClassName)\
        py::class_<ClassType, G4UserStackingAction>(stacking, ClassName)\
                .def(py::init<>())\
                .def("UserSteppingAction", &ClassType::UserSteppingAction)

#define REGISTER_G4TRACKING(ClassType, ClassName)\
        py::class_<ClassType, G4UserTrackingAction>(tracking, ClassName)\
                .def(py::init<>())\
                .def("UserSteppingAction", &ClassType::UserSteppingAction)

#define REGISTER_G4STEPPING(ClassType, ClassName)\
        py::class_<ClassType, G4UserSteppingAction>(stepping, ClassName)\
                .def(py::init<>())\
                .def("UserSteppingAction", &ClassType::UserSteppingAction)

#define REGISTER_G4UTIL(ClassType, ClassName)\
        util.def(ClassName, &ClassType)


#define REGISTER_PCMODULE(ModuleName, Description) \
	PYBIND11_MODULE(ModuleName, m) {\
                m.doc() = Description;\
		m.add_object("geant4", py::module::import("geant4"));\
                auto analysis  = m.def_submodule("analysis", "Detector SubModules");\
                auto util      = m.def_submodule("util", "Detector SubModules");\
                auto detector  = m.def_submodule("detector", "Detector SubModules");\
                auto physics   = m.def_submodule("physics", "Stepping SubModules");\
                auto run       = m.def_submodule("run", "Stepping SubModules");\
		auto generator = m.def_submodule("generator", "Stepping SubModules");\
                auto event     = m.def_submodule("event", "Stepping SubModules");\
                auto stacking  = m.def_submodule("stacking", "Stepping SubModules");\
                auto tracking  = m.def_submodule("tracking", "Stepping SubModules");\
                auto stepping  = m.def_submodule("stepping", "Stepping SubModules");\
                auto geometry  = m.def_submodule("geometry", "Stepping SubModules");\
                auto sensitive  = m.def_submodule("sensitive", "Sensitive SubModules");



#define FINALIZE_PCMODULE() }

