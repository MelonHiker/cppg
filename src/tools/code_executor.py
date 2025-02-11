# code_executor.py
import subprocess
import os
import tempfile

class CodeExecutor:
    """
    Base class for executing code strings in different languages using subprocess.
    """
    def __init__(self, language_name, file_extension, execute_command_template):
        """
        Initialize the CodeExecutor.

        Args:
            language_name (str): The name of the programming language (e.g., "Python", "C++").
            file_extension (str): The file extension for the language's source code files (e.g., ".py", ".cpp").
            execute_command_template (list): A template for the subprocess command to execute the code.
                                             It should contain placeholders like '{executable_path}' for
                                             the path to the executable file.
        """
        self.language_name = language_name
        self.file_extension = file_extension
        self.execute_command_template = execute_command_template

    def execute_code(self, code_string, stdin_input=None): # Added stdin_input parameter
        """
        Executes the given code string using subprocess.

        Args:
            code_string (str): The code string to execute.
            stdin_input (str, optional):  Input string to be passed to the standard input of the executed program.
                                         Defaults to None, meaning no stdin input.

        Returns:
            dict: A dictionary containing execution output and error messages.
                  Keys: 'execution_output', 'error_message'.
        """
        execution_output = ""
        error_message = ""
        temp_file_path = ""

        try:
            # 1. Create a temporary file to store the code
            with tempfile.NamedTemporaryFile(suffix=self.file_extension, mode="w", delete=False) as tmp_file:
                temp_file_path = tmp_file.name
                tmp_file.write(code_string) # Write code string to the temporary file

            # 2. Execute the code using subprocess
            execute_command = [cmd.format(executable_path=temp_file_path) for cmd in self.execute_command_template] # Format command with file path
            subprocess_args = {
                'command': execute_command,
                'capture_output': True,
                'text': True,
                'check': True
            }
            if stdin_input is not None: # If stdin_input is provided
                subprocess_args['input'] = stdin_input.encode('utf-8') # Encode stdin input to bytes

            execute_result = subprocess.run(**subprocess_args) # Pass args dictionary to subprocess.run
            execution_output = execute_result.stdout
            execute_error = execute_result.stderr

            if execute_error: # If there's error output during execution
                error_message += f"Execution Error ({self.language_name}):\n{execute_error}\n"
                return {
                    "execution_output": execution_output,
                    "error_message": error_message
                }

        except subprocess.CalledProcessError as e:
            # Capture subprocess execution errors
            error_message += f"Subprocess Error ({self.language_name}):\n{e}\n"
            error_message += f"Standard Error Output:\n{e.stderr}\n" # Include detailed error info
            return {
                "execution_output": execution_output,
                "error_message": error_message
            }
        except Exception as e:
            # Capture other exceptions
            error_message += f"Exception occurred ({self.language_name}):\n{e}\n"
            return {
                "execution_output": execution_output,
                "error_message": error_message
            }
        finally:
            # 3. Clean up temporary file (delete it regardless of success or failure)
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        return {
            "execution_output": execution_output,
            "error_message": error_message
        }