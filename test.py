from src.tools.python_executor import PythonCodeExecutor
from src.tools.cpp_executor import CppCodeExecutor

# Execute Python code:
py_executor = PythonCodeExecutor()
python_code = """
name = input("Enter your name: ")
print("Hello, " + name + "!")
"""
result = py_executor.execute_code(python_code, stdin_input="Alice")
print(result["execution_output"])
print(bool(result["error_message"]))

# Execute C++ code:
cpp_executor = CppCodeExecutor()
cpp_code = r'''
#include <iostream>
#include <string>
using namespace std;
int main(){
  string name;
  getline(cin, name);
  cout << "Hello, " << name << "!" << endl
  return 0;
}
'''
result2 = cpp_executor.execute_code(cpp_code, stdin_input="Bob")
print(result2["execution_output"])
print(bool(result2["error_message"]))