#pragma once
#include <string>
#include <map>
#include <vector>

class IniHandler {
private:
    std::string iniPath;
    std::map<std::string, std::map<std::string, std::string>> sections;
    
public:
    IniHandler(const std::string& path);
    
    bool load();
    bool save();
    
    void setValue(const std::string& section, const std::string& key, const std::string& value);
    std::string getValue(const std::string& section, const std::string& key, const std::string& defaultValue = "");
    void removeKey(const std::string& section, const std::string& key);
    void removeSection(const std::string& section);
    
    bool sectionExists(const std::string& section);
    bool keyExists(const std::string& section, const std::string& key);
};