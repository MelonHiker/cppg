import subprocess

def test_code(code: str, sampleIO: list):
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

        if result.returncode != 0:
            return result.stderr
        
        generated_output = [line.rstrip() for line in result.stdout.splitlines() if line.strip()]
        expected_output = [line.rstrip() for line in sample_output.splitlines() if line.strip()]

        if (generated_output != expected_output):
            return "Wrong Answer"

    return "Accept"