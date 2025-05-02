#include <iostream>
#include <sstream>
#include <vector>
#include <fstream>
#include <map>

using namespace std;



void string_split(const std::string &str, const char delimiter, std::vector<std::string> &parts) {
    std::stringstream ss(str);
    std::string part;
    while (getline(ss, part, delimiter)) {
        parts.push_back(std::move(part));
    }
}

void file_read(const std::string &filename, std::vector<std::string> &lines) {
    std::ifstream fin;
    fin.open(filename);
    if (!fin.is_open()) { return; }
    std::string line;
    while (std::getline(fin, line)) {
        lines.push_back(line);
    }
    fin.close();
}

void file_write(const std::string &filename, const std::vector<std::string> &lines) {
    std::ofstream fout;
    fout.open(filename, std::ios::out | std::ios::trunc);
    if (!fout.is_open()) { return; }
    for (const auto& line: lines) {
        fout << line << std::endl;
    }
    fout.close();
}


int main(int argc, char *argv[])
{
    // arguments for each key and token, "" if token wasnt set - always n arguments
    // for now just 2 args- discord token and channel id

    map<string, string> env_variables;
    vector<string> lines;
    file_read("test_env", lines);

    for(string line : lines)
    {
        vector<string> parts;
        string_split(line, '=', parts);
        env_variables[parts[0]] = parts[1];
    }
    
    int i = 1;
    while(argc > i)
    {
        vector<string> parts;
        string_split(argv[i], '=', parts);
        env_variables[parts[0]] = parts[1];
        i++;
    }

    vector<string> new_lines;
    for(pair<string, string> key_val : env_variables)
    {
        string line = key_val.first + '=' + key_val.second;
        new_lines.push_back(line);
    }

    file_write("test_env", new_lines);
    printf("Enviroment variables successfully updated!\n");
    return 0;
}