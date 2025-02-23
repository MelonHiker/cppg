from src.log import setup_logger
from src.tools.python_executor import PythonCodeExecutor
from src.tools.cpp_executor import CppCodeExecutor

class CodeExecutor:
    def __init__(self):
        self.logger = setup_logger()

    def run_code(self, code: str, language: str, stdin_input: str = "") -> dict:
        if language == "python":
            executor = PythonCodeExecutor()
        elif language == "cpp":
            executor = CppCodeExecutor()
        else:
            self.logger.warning("Invalid language")
            raise ValueError("Invalid language")

        return executor.execute_code(code, stdin_input)

    def run_sample_tests(self, code: str, language: str, sampleIO: list):
        for i in range(len(sampleIO)):
            sample_input = sampleIO[i]["input"]
            sample_output = sampleIO[i]["output"]

            if language == "python":
                executor = PythonCodeExecutor()
            elif language == "cpp":
                executor = CppCodeExecutor()
            else:
                self.logger.warning("Invalid language")
                raise ValueError("Invalid language")
            
            result = executor.execute_code(code, sample_input)
            if result["error_message"]:
                return result["error_message"]

            generated_output = [line.rstrip() for line in result["execution_output"].splitlines() if line.strip()]
            expected_output = [line.rstrip() for line in sample_output.splitlines() if line.strip()]
            endl = "\n"
            if (generated_output != expected_output):
                msg = "Wrong Answer\n"
                msg += f"input:{endl}{sample_input}{endl}"
                msg += f'generated_output:{endl}{endl.join(generated_output)}{endl}'
                msg += f'expected_output:{endl}{endl.join(expected_output)}{endl}'
                return msg

        return "Accept"