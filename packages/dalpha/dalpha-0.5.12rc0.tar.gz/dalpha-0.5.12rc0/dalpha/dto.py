from dalpha.exception import ExpectedError
from dalpha.logging import logger


class InferenceResult:
    def __init__(self, usage: int, output_json: dict) -> None:
        if not isinstance(usage, int) or usage < 0:
        # validation
            error_message = f"Expected TypeError occured. \033[31musage should not be negative\033[0m\n"
            logger.error(error_message)
            error_json = {"reason": f"TypeError; usage should not be negative"}
            raise ExpectedError(error_json=error_json)

        if not isinstance(output_json, dict):
            error_message = f"Expected TypeError occured. \033[31moutput_json should be dictionary type\033[31m\n"
            logger.error(error_message)
            error_json = {"reason": f"TypeError; output_json should be dictionary type"}
            raise ExpectedError(error_json=error_json)

        self.usage = usage
        self.output_json = output_json

class UpdateResult:
    def __init__(self, usage: int, output_json: dict) -> None:
        # validation
        if not isinstance(usage, int) or usage < 0:
            error_message = f"Expected TypeError occured. \033[31musage should not be negative\033[0m\n"
            logger.error(error_message)
            error_json = {"reason": f"TypeError; usage should not be negative"}
            raise ExpectedError(error_json=error_json)

        if not isinstance(output_json, dict):
            error_message = f"Expected TypeError occured. \033[31moutput_json should be dictionary type\033[31m\n"
            logger.error(error_message)
            error_json = {"reason": f"TypeError; output_json should be dictionary type"}
            raise ExpectedError(error_json=error_json)

        self.usage = usage
        self.output_json = output_json