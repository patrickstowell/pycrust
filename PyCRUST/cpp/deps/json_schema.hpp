#pragma once
#include "deps/json.hpp"

#include <iostream>
#include <stdexcept>

using namespace nlohmann;

namespace json_schema {
bool check(const json& node, std::string id, std::vector<std::string> keys){
    for (auto const & s : keys) {
        if (node.contains(s)) {
            continue;
        } else {
            std::cerr << id << " Failed to find key! [" << s << "] : " << node << std::endl;
            throw std::runtime_error("Failed to find key!");
        }
    }
}
}

// namespace json_tool {

//     template <typename T> T as(const json & js) {
//         return js.template get<T>();
//     }
// }

// template <typename T> T as(const json & js) {
//     return js.template get<T>();
// }