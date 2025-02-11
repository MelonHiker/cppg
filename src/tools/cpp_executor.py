import subprocess
import tempfile
import os

class CppCodeExecutor:
    def execute_code(self, code: str, stdin_input: str = "") -> dict:
        # Write C++ code to a temporary file.
        with tempfile.NamedTemporaryFile("w", suffix=".cpp", delete=False) as source_file:
            source_file.write(code)
            source_file_path = source_file.name

        # Determine the executable path
        executable_path = source_file_path.replace(".cpp", "")
        try:
            # Compile the C++ code with g++
            compile_result = subprocess.run(
                ["g++", source_file_path, "-o", executable_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if compile_result.returncode != 0:
                return {
                    "execution_output": "",
                    "error_message": compile_result.stderr.decode("utf-8"),
                }
            # Run the compiled executable
            run_result = subprocess.run(
                [executable_path],
                input=stdin_input.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5,
            )
            return {
                "execution_output": run_result.stdout.decode("utf-8"),
                "error_message": run_result.stderr.decode("utf-8"),
            }
        except subprocess.TimeoutExpired as exc:
            return {
                "execution_output": "",
                "error_message": "TimeoutExpired: " + str(exc),
            }
        finally:
            if os.path.exists(source_file_path):
                os.remove(source_file_path)
            if os.path.exists(executable_path):
                os.remove(executable_path)