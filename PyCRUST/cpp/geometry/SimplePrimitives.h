#pragma once 

#include "deps/json.hpp"
#include "deps/json_schema.hpp"


using namespace nlohmann;
#include <iostream>
#include <string>
#include <vector>

#include "G4Box.hh"
#include "G4VSolid.hh"
#include "G4NistManager.hh"
#include "G4VoxelNavigation.hh"
#include "G4OpticalSurface.hh"
#include "G4LogicalBorderSurface.hh"
#include "G4LogicalBorderSurface.hh"
#include "G4PhysicalVolumeStore.hh"


void AddPropertyToMaterial(G4Material* mat, 
    std::string key,
    std::vector<double>& x,
    std::vector<double>& y){
      auto tab = mat->GetMaterialPropertiesTable();
      if (!tab) tab = new G4MaterialPropertiesTable();
      tab->AddProperty(key.c_str(), &x[0], &y[0], x.size());
      mat->SetMaterialPropertiesTable(tab);
    }

void AddConstPropertyToMaterial(G4Material* mat, 
    std::string key,
    double val){
      auto tab = mat->GetMaterialPropertiesTable();
      if (!tab) tab = new G4MaterialPropertiesTable();
      tab->AddConstProperty(key.c_str(), val);
      mat->SetMaterialPropertiesTable(tab);
    }

void DumpMaterialPropertiesTable(G4Material* mat){
  auto tab = mat->GetMaterialPropertiesTable();
  if (!tab) tab = new G4MaterialPropertiesTable();
  tab->DumpTable();
}

G4Material* GetMaterial(std::string name){
  G4NistManager* nist = G4NistManager::Instance();
  return nist->FindOrBuildMaterial(name);
}

G4Element* GetElement(std::string name){
  G4NistManager* nist = G4NistManager::Instance();
  return nist->FindOrBuildElement(name);
}

void AddPropertiesToMaterialFromJson(G4Material* mat, const json &cfg){

    std::vector<std::string> const_keys = {
        "YIELDRATIO",
        "RESOLUTIONSCALE",
        "SCINTILLATIONYIELD",
        "SCINTILLATIONTIMECONSTANT1",
        "SCINTILLATIONTIMECONSTANT2",
        "FASTTIMECONSTANT",
        "SLOWTIMECONSTANT",
        "MIEHG_FORWARD_RATIO",
        "WLSTIMECONSTANT"
    };

    for (auto const& k : const_keys) {
        if (cfg.contains(k)) {
            AddConstPropertyToMaterial(mat,
            k, cfg[k].as<double>());
        }
    }

    std::vector<std::string> vector_keys = {
        "SCINTILLATIONCOMPONENT1",
        "SCINTILLATIONCOMPONENT2",
        "WLSABSLENGTH",
        "WLSCOMPONENT",
        "ABSLENGTH",
        "RINDEX",
        "RAYLEIGH",
        "MIEHG"
    };

    for (auto const& k : vector_keys) {
        std::string kx = k + "_X";
        std::string ky = k + "_Y";
        if (cfg.contains(kx)) {
            std::cout << "CONFIG Contains " << kx << std::endl;
            std::vector<double> vx = cfg[kx].as<std::vector<double>>();
            std::vector<double> vy = cfg[ky].as<std::vector<double>>();

            AddPropertyToMaterial(mat,
                k, vx, vy);
        }
    }
}

#include "G4TriangularFacet.hh"
#include "G4TessellatedSolid.hh"
#include "G4VoxelLimits.hh"
#include "G4AffineTransform.hh"
#include "G4VSolid.hh"
std::vector<double> GetVertices(G4VSolid* solid, int axis){
    std::vector<double> vertices;

    // Create a G4Box solid
    auto poly = solid->GetPolyhedron();
    for (int i = 0; i < poly->GetNoVertices(); i++) {
        vertices.push_back(poly->GetVertex(i+1)[axis]);
    }
    return vertices;

}

std::vector<int> GetNFacets(G4VSolid* solid){
    G4int n;
    G4int facet_edges[20];
    std::vector<int> nf;
    auto poly = solid->GetPolyhedron();
    for (int i = 0; i < poly->GetNoFacets(); i++) {
        poly->GetFacet(i+1, n, facet_edges);
        nf.push_back(n);
    }
    return nf;
}

std::vector<int> GetFacets(G4VSolid* solid, int i){
    std::vector<int> vertices;

    // Create a G4Box solid
    G4int n;
    G4int facet_edges[20];
    auto poly = solid->GetPolyhedron();
    poly->GetFacet(i+1, n, facet_edges);
    std::vector<int> nf;

    for (int i = 0; i < n; i++){
        nf.push_back( facet_edges[i] );
    }
    return nf;
}


//     auto poly = solid->GetPolyhedron();
//     for (int i = 0; i < poly->GetNoFacets()-1; i++) {
        
        
//         if (n == 3){
//             vertices.push_back(facet_edges[axis]);
//         } else {
//             for (size_t j = 1; j < n - 1; ++j) {
//                 if (axis == 0) vertices.push_back(facet_edges[0]);
//                 else if (axis == 1) vertices.push_back(facet_edges[j]);
//                 else if (axis == 2) vertices.push_back(facet_edges[j+1]);
//             }
//         }
//     }
//     return vertices;
// }

namespace pc {

    

    G4MaterialPropertiesTable* SimpleMaterialPropertiesTable(const json &cfg) {

        G4MaterialPropertiesTable* mat = new G4MaterialPropertiesTable();
        
        std::vector<std::string> props;
        props.push_back("WLSTIMECONSTANT");
        props.push_back("BIRKSCONSTANT");
        props.push_back("SCINTILLATIONCOMPONENT1");
        props.push_back("SCINTILLATIONCOMPONENT2");
        props.push_back("SCINTILLATIONCOMPONENT3");
        props.push_back("RINDEX");
        props.push_back("ABSLENGTH");
        props.push_back("SCINTILLATIONYIELD");
        props.push_back("RESOLUTIONSCALE");
        props.push_back("SCINTILLATIONTIMECONSTANT1");
        props.push_back("SCINTILLATIONTIMECONSTANT2");
        props.push_back("SCINTILLATIONTIMECONSTANT3");
        props.push_back("SCINTILLATIONYIELD1");
        props.push_back("SCINTILLATIONYIELD2");
        props.push_back("SCINTILLATIONYIELD3");
        props.push_back("BIRKSCONSTANT");
        props.push_back("REFLECTIVITY");
        props.push_back("EFFICIENCY");
        props.push_back("WLSABSLENGTH");
        props.push_back("WLSCOMPONENT");
        props.push_back("RAYLEIGH");
        props.push_back("MIEHG");
        props.push_back("MIEHG_FORWARD_RATIO");
        props.push_back("MIEHG_FORWARD");
        props.push_back("MIEHG_BACKWARD");
        
        

        for (int i = 0; i < props.size(); i++) {
            std::string depvar = props[i];

            if (cfg.contains(depvar + "_Y")) {
                std::vector<double> dep_x =\
                    cfg[depvar + "_X"].as<std::vector<double>>();

                std::vector<double> dep_y =\
                    cfg[depvar + "_Y"].as<std::vector<double>>();

                mat->AddProperty(depvar.c_str(),
                    &dep_x[0],
                    &dep_y[0],
                    dep_x.size());
            }

            if (cfg.contains(depvar)) {
                mat->AddConstProperty(depvar.c_str(), cfg[depvar].as<double>());
            }
        }

        return mat;
}

    void SetMaterialProperties(G4Material* mat, const json &cfg){
        auto tab = SimpleMaterialPropertiesTable(cfg);
        mat->SetMaterialPropertiesTable(tab);
    }

    G4Element* SimpleElement(const json &cfg,  bool force=true) {
        // json_schema::check(cfg, __FUNCTION__,
            // {"name", "symbol", "atomicnumber", "atomicmass"});

        G4NistManager* nist = G4NistManager::Instance();

        G4Element* mat = nist->FindOrBuildElement(cfg["name"]
            .as<std::string>());
        if (mat && !force) return mat;

        return new G4Element(cfg["name"].as<std::string>(),
            cfg["symbol"].as<std::string>(),
            cfg["atomicnumber"].as<int>(),
            cfg["atomicmass"].as<double>());
    }

    G4Material* SimpleMaterial(const json &cfg,  bool force=true) {
        // json_schema::check(cfg, __FUNCTION__,
            // {"name", "element_names", "element_fraction", "density"});

        G4NistManager* nist = G4NistManager::Instance();

        auto name = cfg["name"].as<std::string>();
        auto mat = nist->FindOrBuildMaterial(name);
        if (mat && !force) return mat;

        auto elements = cfg["element_names"].as<std::vector<std::string>>();
        auto fractions = cfg["element_fraction"].as<std::vector<double>>();
        auto density  = cfg["density"].as<double>();

        mat = new G4Material(name, density, fractions.size());
        for (uint j = 0; j < fractions.size(); j++) {
            json sub_cfg;
            sub_cfg["name"] = elements[j];
            G4Element* ele = SimpleElement(sub_cfg, false);
            mat->AddElement(ele, fractions[j]);
        }

        mat->SetMaterialPropertiesTable(SimpleMaterialPropertiesTable(cfg));

        return mat;
    }

    
    G4Material* material(const json &cfg) {

        std::cout << "Creating NIST " << std::endl;
        
        G4NistManager* nist = G4NistManager::Instance();

        auto name = cfg["name"].as<std::string>();
        std::cout << "Searching material : " << name << " " << std::endl;
        
        G4Material* mat = nist->FindOrBuildMaterial(name);
        if (mat) {
            std::cout << "Found material : " << name << " " << std::endl;
            return mat;
        } else {
            std::cout << "Building material " << std::endl;
        }

        auto elements = cfg["components"].as<std::vector<std::string>>();
        auto fractions = cfg["fractions"].as<std::vector<double>>();
        auto density  = cfg["density"].as<double>();

        mat = new G4Material(name, density, fractions.size());
        for (uint j = 0; j < fractions.size(); j++) {
            json sub_cfg;
            sub_cfg["name"] = elements[j];
            G4Element* ele = SimpleElement(sub_cfg, false);
            mat->AddElement(ele, fractions[j]);
        }

        // mat->SetMaterialPropertiesTable(SimpleMaterialPropertiesTable(cfg));

        return mat;
    }

    G4Material* SimpleCompound(const json &cfg, bool force=true) {
        json_schema::check(cfg, __FUNCTION__,
            {"name", "names", "fractions", "density"});

        G4NistManager* nist = G4NistManager::Instance();

        auto name = cfg["name"].as<std::string>();
        auto mat = nist->FindOrBuildMaterial(name);
        if (mat && !force) return mat;

        auto elements = cfg["names"].as<std::vector<std::string>>();
        auto fractions = cfg["fractions"].as<std::vector<double>>();
        auto density  = cfg["density"].as<double>();

        mat = new G4Material(name, density, fractions.size());
        for (uint j = 0; j < fractions.size(); j++) {
            json sub_cfg;
            sub_cfg["name"] = elements[j];
            G4Material* ele = SimpleMaterial(sub_cfg, false);
            if (!ele){
                std::cout << "FAILED TO FIND SIMPLE MATERIAL" << std::endl;
            }
            mat->AddMaterial(ele, fractions[j]);
        }

        // AddPropertiesToMaterialFromJson(mat, cfg);
        mat->SetMaterialPropertiesTable(SimpleMaterialPropertiesTable(cfg));

        return mat;
    }

    G4VSolid* SimpleBox(const json &cfg) {
        json_schema::check(cfg, __FUNCTION__, {"name", "x", "y", "z"});
        std::string pName = cfg["name"].as<std::string>();
        double pX = cfg["x"].as<double>();
        double pY = cfg["y"].as<double>();
        double pZ = cfg["z"].as<double>();
        auto solid = new G4Box(pName, pX, pY, pZ);
        return solid;
    }

    G4LogicalVolume* SimpleLogical(const json &cfg) {
        json_schema::check(cfg, __FUNCTION__, {"name", "type", "material"});
        std::string pType = cfg["type"].as<std::string>();

        G4VSolid* solid;
        if (pType == "box")  solid = SimpleBox(cfg);
        if (pType == "tubs") solid = SimpleBox(cfg);

        G4NistManager* nist = G4NistManager::Instance();
        auto mat = nist->FindOrBuildMaterial(cfg["material"].as<std::string>());

        return new G4LogicalVolume(solid, mat, cfg["name"]);
    }

    void AddOpticalSurface(const json &cfg){

        std::string name = cfg["name"].as<std::string>();
        std::string inner_name = cfg["inner"].as<std::string>();
        std::string outer_name = cfg["outer"].as<std::string>();

        G4OpticalSurface* wrapper  = new G4OpticalSurface(name);
        G4VPhysicalVolume* outer_log = G4PhysicalVolumeStore::GetInstance()->GetVolume(inner_name, 1);
        G4VPhysicalVolume* inner_log = G4PhysicalVolumeStore::GetInstance()->GetVolume(outer_name, 1);
        wrapper->SetType(dielectric_LUT);
        wrapper->SetModel(LUT);
    
        std::string surface_model = cfg["model"].as<std::string>();
        if (surface_model == "polishedlumirrorair") wrapper->SetFinish(polishedlumirrorair);
        else if (surface_model == "polishedlumirrorglue") wrapper->SetFinish(polishedlumirrorglue);
        else if (surface_model == "polishedair") wrapper->SetFinish(polishedair);
        else if (surface_model == "polishedteflonair") wrapper->SetFinish(polishedteflonair);
        else if (surface_model == "polishedtioair") wrapper->SetFinish(polishedtioair);
        else if (surface_model == "polishedtyvekair") wrapper->SetFinish(polishedtyvekair);

        new G4LogicalBorderSurface(name, inner_log, outer_log, wrapper);
    } 
    


}