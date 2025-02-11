# language_executors.py
from src.tools.code_executor import CodeExecutor
import subprocess
import tempfile
import os

class PythonCodeExecutor(CodeExecutor):
    """
    Code executor for Python code.
    """
    def __init__(self):
        super().__init__(
            language_name="Python",
            file_extension=".py",
            execute_command_template=["python", "{executable_path}"]
        )

class CppCodeExecutor(CodeExecutor):
    """
    Code executor for C++ code.
    """
    def __init__(self):
        super().__init__(
            language_name="C++",
            file_extension=".cpp",
            execute_command_template=["g++", "{executable_path}", "-o", "{executable_path}.exe"] # Compile command
        )
        self.executable_extension = ".exe" # Extension for compiled executable

    def execute_code(self, cpp_code_string):
        """
        Overrides the execute_code method to include compilation step for C++.
        """
        compile_output = ""
        compile_error = ""
        error_message = ""
        temp_file_path = ""
        executable_path = ""

        try:
            # 1. Create a temporary file for C++ code
            with tempfile.NamedTemporaryFile(suffix=self.file_extension, mode="w", delete=False) as tmp_cpp_file:
                temp_file_path = tmp_cpp_file.name
                tmp_cpp_file.write(cpp_code_string)

            executable_path = tempfile.mktemp() # Create temp path for executable

            # 2. Compile C++ code
            compile_command = [cmd.format(executable_path=temp_file_path) for cmd in self.execute_command_template[:-1]] # Exclude last part of template for compile cmd (output file specifier)
            compile_command.extend([self.execute_command_template[-1].format(executable_path=executable_path)]) # Add output file specifier with executable path
            compile_result = subprocess.run(compile_command, capture_output=True, text=True, check=True)
            compile_output = compile_result.stdout
            compile_error = compile_result.stderr

            if compile_error:
                error_message += f"Compilation Error (C++):\n{compile_error}\n"
                return {
                    "compile_output": compile_output, # Include compile output in result
                    "execution_output": "",
                    "error_message": error_message
                }

            # 3. Execute the compiled executable
            execute_cmd_exe = [executable_path + self.executable_extension] # Path to the actual .exe file
            execute_result = subprocess.run(execute_cmd_exe, capture_output=True, text=True, check=True)
            execution_output = execute_result.stdout
            execute_error = execute_result.stderr

            if execute_error:
                error_message += f"Execution Error (C++):\n{execute_error}\n"
                return {
                    "compile_output": compile_output, # Still include compile output
                    "execution_output": execution_output,
                    "error_message": error_message
                }


        except subprocess.CalledProcessError as e:
            error_message += f"Subprocess Error (C++):\n{e}\n"
            error_message += f"Standard Error Output:\n{e.stderr}\n"
            return {
                "compile_output": compile_output, # Still include compile output
                "execution_output": "",
                "error_message": error_message
            }
        except Exception as e:
            error_message += f"Exception occurred (C++):\n{e}\n"
            return {
                "compile_output": compile_output, # Still include compile output
                "execution_output": "",
                "error_message": error_message
            }
        finally:
            # 4. Clean up temporary files (source and executable)
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if executable_path and os.path.exists(executable_path + self.executable_extension): # Remove .exe
                os.remove(executable_path + self.executable_extension)

        return {
            "compile_output": compile_output, # Include compile output in result
            "execution_output": execution_output,
            "error_message": error_message
        }