import subprocess
from src.log import setup_logger
import subprocess
import os
import tempfile

class CodeRunner:
    def __init__(self):
        self.logger = setup_logger()

    def run_sample_tests(self, code: str, language: str, sampleIO: list):
        for i in range(len(sampleIO)):
            sample_input = sampleIO[i]["input"]
            sample_output = sampleIO[i]["output"]

            try:
                result = subprocess.run(
                    ["python3", "-c", code], 
                    input=sample_input,
                    capture_output=True,
                    text=True,
                    timeout=2
                )
            except subprocess.TimeoutExpired:
                return "Timeout"
            except Exception as e:
                return f"Runtime Error: {e}"

            if result.returncode != 0:
                return result.stderr
            
            generated_output = [line.rstrip() for line in result.stdout.splitlines() if line.strip()]
            expected_output = [line.rstrip() for line in sample_output.splitlines() if line.strip()]

            if (generated_output != expected_output):
                msg = "Wrong Answer\n"
                msg += f"input:\n{sample_input}\n"
                msg += f"generated_output:\n{"\n".join(generated_output)}\n"
                msg += f"expected_output:\n{"\n".join(expected_output)}\n"
                return msg

        return "Accept"