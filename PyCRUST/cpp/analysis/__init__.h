#pragma once
#include "PyCRUST.h"
#include "PandasAnalysisManager.h"
#include "pybind11/stl_bind.h"

void module_register_analysis(py::module analysis) {

  py::class_<Analysis>(analysis, "Manager")\
    .def(py::init<>(), py::return_value_policy::reference_internal)\
    .def("CreateNtupleIColumn", &Analysis::CreateNtupleIColumn)\
    .def("CreateNtupleFColumn", &Analysis::CreateNtupleFColumn)\
    .def("CreateNtupleDColumn", &Analysis::CreateNtupleDColumn)\
    .def("AddNTupleRow", &Analysis::AddNTupleRow)\
    .def("OpenFile", &Analysis::OpenFile)\
    .def("OpenRun", &Analysis::OpenRun)\
    .def("CloseFile", &Analysis::CloseFile)\
    .def("CloseRun", &Analysis::CloseRun)\
    .def("add_int", &Analysis::add_int)\
    .def("add_float", &Analysis::add_float)\
    .def("add_double", &Analysis::add_double)\
    .def("fill_int", &Analysis::fill_int)\
    .def("fill_float", &Analysis::fill_float)\
    .def("fill_double", &Analysis::fill_double)\
    .def("save_row", &Analysis::save_row)\
    .def("open_file", &Analysis::open_file)\
    .def("open_run", &Analysis::open_run)\
    .def_readwrite("run_name", &Analysis::run_name)\
    .def_readwrite("run_number", &Analysis::run_number)\
    .def("close_file", &Analysis::close_file)\
    .def("close_run", &Analysis::close_run)\
    .def("commit", &Analysis::commit)\
    .def("is_signal", &Analysis::is_signal)\
    .def_readwrite("signal_definition", &Analysis::signal_definition)\
    .def("set_signal_flag", &Analysis::set_signal_flag)\
    .def("set_signal_variable", &Analysis::set_signal_variable)\
    .def("reset_signal", &Analysis::reset_signal)\
    .def_static("__new__", [](py::object) {return Analysis::Instance();},
        py::return_value_policy::reference_internal);

  py::class_<AnalysisRunAction, G4UserRunAction>(analysis, "AnalysisRunAction")\
    .def(py::init<>(), py::return_value_policy::reference_internal);

// Start of Run Action
// Start of Event Action
// End of Event Action
// End of Run Action

}
