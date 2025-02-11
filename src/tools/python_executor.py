import subprocess
import tempfile
import os

class PythonCodeExecutor:
    def execute_code(self, code: str, stdin_input: str = "") -> dict:
        # Write code into a temporary file
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        try:
            result = subprocess.run(
                ["python3", temp_file_path],
                input=stdin_input.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
            return {
                "execution_output": result.stdout.decode("utf-8"),
                "error_message": result.stderr.decode("utf-8"),
            }
        except subprocess.TimeoutExpired as exc:
            return {
                "execution_output": "",
                "error_message": "TimeoutExpired: " + str(exc),
            }
        finally:
            os.remove(temp_file_path)