import yaml
from src.log import setup_logger

class LLMParser:
    def __init__(self):
        self.logger = setup_logger()

    def load_code(self, response_text: str, language: str):
        response_text = response_text.rstrip("` \n")
        response_text = response_text.removeprefix(f'```{language}').rstrip('`')
        return response_text

    def load_yaml(self, response_text: str, keys_fix_yaml: list = []) -> dict:
        response_text = response_text.rstrip("` \n")
        response_text = response_text.removeprefix('```yaml').rstrip('`')
        try:
            data = yaml.safe_load(response_text)
        except yaml.YAMLError as e:
            data = self._try_fix_yaml(response_text, keys_fix_yaml=keys_fix_yaml)
            if not data:
                self.logger.info(f"Failed to parse AI YAML prediction: {e}")
        return data

    def _try_fix_yaml(self, response_text: str, keys_fix_yaml: list = []) -> dict:
        response_text_lines = response_text.split('\n')
        keys = keys_fix_yaml
        response_text_lines_copy = response_text_lines.copy()
        for i in range(0, len(response_text_lines_copy)):
            for key in keys:
                if response_text_lines_copy[i].strip().startswith(key) and not '|' in response_text_lines_copy[i]:
                    response_text_lines_copy[i] = response_text_lines_copy[i].replace(f'{key}',
                                                                                    f'{key} |-\n        ')
        try:
            data = yaml.safe_load('\n'.join(response_text_lines_copy))
            self.logger.info(f"Successfully parsed AI prediction after adding |-\n")
            return data
        except yaml.YAMLError as e:
            self.logger.error(f"yaml parsing error\n")
            raise ValueError("yaml parsing error")