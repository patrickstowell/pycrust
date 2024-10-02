#pragma once
#include <map>
#include <string>

#include <map>
#include <string>
#include "G4UserRunAction.hh"
#include "G4Event.hh"
#include "G4Run.hh"

// #include "G4CsvAnalysisManager.hh"
#include "G4CsvAnalysisManager.hh"
// #include "g4csv_defs.hh"
// using namespace G4Csv; //using namespace G4Xml; //using namespace G4Csv;

namespace SIGNAL {
bool ALL(const std::map<std::string, bool>& flags,
            const std::map<std::string, double>& variables) {
    return true;
}

bool AND(const std::map<std::string, bool>& flags,
        const std::map<std::string, double>& variables) {
    for (auto const & [s,b] : flags){
        if (!b) return false;
    }
    return true;
}

bool OR(const std::map<std::string, bool>& flags,
        const std::map<std::string, double>& variables) {
    for (auto const & [s,b] : flags){
        if (b) return true;
    }
    return false;
}

}

class Analysis {
public:
    // Deleted copy constructor and copy assignment operator to prevent duplication
    // Analysis(const Analysis&) = delete;
    Analysis& operator=(const Analysis&) = delete;

    static Analysis& Instance() {
        static Analysis instance; // Guaranteed to be initialized only once
        return instance;
    }

    int CreateNtupleIColumn(std::string label) {
        auto manl = G4CsvAnalysisManager::Instance();
        int index = manl->CreateNtupleIColumn(label);
        _register(label, index, 1);
        committed=false;
        return index;
    }

    int CreateNtupleFColumn(std::string label) {
        auto manl = G4CsvAnalysisManager::Instance();
        int index = manl->CreateNtupleFColumn(label);
        _register(label, index, 2);
        committed=false;

        return index;
    }

    int CreateNtupleDColumn(std::string label) {
        auto manl = G4CsvAnalysisManager::Instance();
        int index = manl->CreateNtupleDColumn(label);
        _register(label, index, 3);
        committed=false;

        return index;
    }

    void AddNTupleRow() {
        auto manl = G4CsvAnalysisManager::Instance();
        if (is_signal()) {
            manl->AddNtupleRow();
        }

        // Reset
        reset_signal();
        // for (size_t i = 0; i < column.size(); i++) {
        //     if (type[i] == 1) manl->FillNtupleIColumn(index[i], -999);
        //     if (type[i] == 2) manl->FillNtupleFColumn(index[i], -999.0);
        //     if (type[i] == 3) manl->FillNtupleDColumn(index[i], -999.0);
        // }
    }

    int GetColumn(std::string label){
        for (size_t i = 0; i < column.size(); i++) {
            if (column[i] == label) return index[i];
        }
        std::cerr << "FAILED TO FIND COLUMN" << std::endl;
        throw;
    }

    void FillNtupleDColumn(std::string label, double val){
        auto manl = G4CsvAnalysisManager::Instance();
        int i = GetColumn(label);
        manl->FillNtupleDColumn(i, val);
    }

    void FillNtupleIColumn(std::string label, double val){
        auto manl = G4CsvAnalysisManager::Instance();
        int i = GetColumn(label);
        manl->FillNtupleIColumn(i, val);
    }

    void FillNtupleFColumn(std::string label, double val){
        auto manl = G4CsvAnalysisManager::Instance();
        int i = GetColumn(label);
        manl->FillNtupleFColumn(i, val);
    }

    void commit(){
        auto manl = G4CsvAnalysisManager::Instance();
        manl->FinishNtuple();
        committed = true;
    }
    // Signal Definitions
    bool is_signal() {
        return signal_definition(trigger_flags, trigger_variables);
    }

    std::function<bool(const std::map<std::string, bool>& flags,
                    const std::map<std::string, double>& variables)> signal_definition;


    void set_signal_flag(std::string name, bool f = true) {
        trigger_flags[name] = f;
    }
    void set_signal_variable(std::string name, double v) {
        trigger_variables[name] = v;

    }
    void reset_signal() {
        for (auto const& [l, b] : trigger_flags) {
            trigger_flags[l] = false;
        }
        for (auto const& [l, v] : trigger_variables) {
            trigger_variables[l] = -999.9;
        }
    }

    void OpenFile(std::string filename) {
        man->FinishNtuple();
        man->OpenFile(filename);
    }

    void OpenRun() {

        std::string filename = run_name +
            "_" + std::to_string(run_number);
        std::cout << "OPENING " << filename << std::endl;

        OpenFile(filename);
    }

    void CloseFile() {
        man->Write();
        man->CloseFile();

        run_number++;
        std::cout << "CLOSING RUN NUM " << run_number << std::endl;
    }

    void CloseRun() {
        CloseFile();
    }

    // Short Hands
    int add_int(std::string label) {
        return CreateNtupleIColumn(label);
    }

    int add_float(std::string label) {
        return CreateNtupleFColumn(label);
    }

    int add_double(std::string label) {
        return CreateNtupleDColumn(label);
    }

    void fill_int(std::string label, int val) {
        FillNtupleIColumn(label, val);
    }

    void fill_float(std::string label, float val) {
        FillNtupleFColumn(label, val);
    }

    void fill_double(std::string label, double val) {
        FillNtupleDColumn(label, val);
    }

    int save_row() {
        AddNTupleRow();
    }

    void open_file(std::string filename) {
        OpenFile(filename);
    }

    void open_run() {
        OpenRun();
    }

    void close_run() {
        CloseRun();
    }

    void close_file() {
        CloseFile();
    }



    Analysis() {
        std::cout << "ANALYSIS CONSTRUCTOR " << std::endl;
        man = G4CsvAnalysisManager::Instance();
        man->SetVerboseLevel(0);
        man->SetFirstNtupleId(0);
        man->SetFirstHistoId(0);
        man->CreateNtuple("events", "Dynamic Detector Saved Information");
        run_number = 0;
        committed = false;
        signal_definition = SIGNAL::ALL;
        run_name = "pcdetsim";
    }

    bool committed;
    std::vector<std::string> column;
    std::vector<int> index;
    std::vector<int> type;
    int run_number;
    std::string run_name;
    std::string tag;

    std::map<std::string, bool>   trigger_flags;
    std::map<std::string, double> trigger_variables;

    G4CsvAnalysisManager* man;

    void _register(std::string label, int i, int t) {
        column.push_back(label);
        index.push_back(i);
        type.push_back(t);
    }
};



// class Analysis {
// public:

//     std::map<std::string> column;
//     std::map<int> index;
//     std::map<int> type;

//     G4CsvAnalysisManager* man;

//     _register(std::string label, int i, int t) {
//         column.push_back(label);
//         index.push_back(i);
//         type.push_back(t);
//     }

//     Analysis() {
//         man = G4CsvAnalysisManager::Instance();
//     }

//     int CreateNtupleIColumn(std::string label) {
//         int index = man->CreateNtupleIColumn(label);
//         _register(label, index, 1);
//         return index;
//     }

//     int CreateNtupleFColumn(std::string label) {
//         int index = man->CreateNtupleFColumn(label);
//         _register(label, index, 2);
//         return index;
//     }

//     int CreateNtupleDColumn(std::string label) {
//         int index = man->CreateNtupleDColumn(label);
//         _register(label, index, 3);
//         return index;
//     }

//     void AddNTupleRow() {
//         man->AddNTupleRow();
//         // Reset
//         for (size_t i = 0; i < column.size(); i++) {
//             if (type[i] == 1) man->FillNtupleIColumn(index[i], -999);
//             if (type[i] == 2) man->FillNtupleFColumn(index[i], -999.0);
//             if (type[i] == 3) man->FillNtupleDColumn(index[i], -999.0);
//         }
//     }

// }

// class PandasAnalysis : Analysis {

//     PandasAnalysisManager(){
//     }



// }


class AnalysisRun : public G4Run {
    public:
     void 	RecordEvent (const G4Event * ev){

        // if (ev->GetEventID() % 10000 == 0){
            // std::cout << ev->GetEventID() << std::endl;
        // }
        auto ana = Analysis::Instance();
        // ana.fill_int("evt", ev->GetEventID());
        // ana.save_row();
        return;
    }
};


class AnalysisRunAction : public G4UserRunAction {
    public:

    void BeginOfRunAction (const G4Run *run){
        auto ana = Analysis::Instance();
        ana.add_int("evt");
        ana.commit();
            
        // ana.open_run();

    }

    void EndOfRunAction (const G4Run *run){
        auto ana = Analysis::Instance();
        // ana.close_run();
    }

    G4Run* GenerateRun(){
        return new AnalysisRun();
    }

};
