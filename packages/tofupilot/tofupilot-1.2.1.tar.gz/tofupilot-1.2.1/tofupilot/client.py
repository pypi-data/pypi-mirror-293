import logging
import os
from datetime import timedelta
from importlib.metadata import version
from typing import Dict, List, Optional

import requests

from .constants import (
    ENDPOINT,
    FILE_MAX_SIZE,
    CLIENT_MAX_ATTACHMENTS,
    SECONDS_BEFORE_TIMEOUT,
)
from .models import SubUnit, UnitUnderTest, Step
from .utils import (
    check_latest_version,
    handle_attachments,
    parse_error_message,
    setup_logger,
    timedelta_to_iso,
    datetime_to_iso,
    validate_attachments,
)


class TofuPilotClient:
    def __init__(self, api_key: Optional[str] = None, base_url: str = ENDPOINT):
        self._current_version = version("tofupilot")
        print_version_banner(self._current_version)  # Print the version banner
        self._api_key = api_key
        self._base_url = f"{base_url}/api/v1"
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        self._logger = setup_logger(logging.INFO)
        self._max_attachments = CLIENT_MAX_ATTACHMENTS
        self._max_file_size = FILE_MAX_SIZE
        check_latest_version(self._logger, self._current_version, "tofupilot")
        if api_key is None:
            api_key = os.environ.get("TOFUPILOT_API_KEY")
        if api_key is None:
            error = "Please provide an API key or set TOFUPILOT_API_KEY environment variable. For more information on how to find or generate a valid API key, visit https://docs.tofupilot.com/user-management#api-key."
            self._logger.error(error)
            raise Exception(error)

    def create_run(
        self,
        procedure_id: str,
        unit_under_test: UnitUnderTest,
        run_passed: bool,
        steps: Optional[List[Step]] = None,
        duration: timedelta = None,
        sub_units: Optional[List[SubUnit]] = None,
        report_variables: Optional[Dict[str, str]] = None,
        attachments: Optional[List[str]] = None,
    ) -> dict:
        """
        Creates a test run with the specified parameters and uploads it to the TofuPilot platform.
        [See API reference](https://docs.tofupilot.com/runs).

        Args:
            procedure_id (str): The unique identifier of the procedure to which the test run belongs.
            unit_under_test (UnitUnderTest): The unit being tested.
            run_passed (bool): Boolean indicating whether the test run was successful.
            duration (timedelta, optional): The duration of the test run. Default is None.
            steps (Optional[List[Step]], optional): [A list of steps included in the test run](https://docs.tofupilot.com/steps). Default is None.
            sub_units (Optional[List[SubUnit]], optional): [A list of sub-units included in the test run](https://docs.tofupilot.com/sub-units). Default is None.
            report_variables (Optional[Dict[str, str]], optional): [A dictionary of key values that will replace the procedure's {{report_variables}}](https://docs.tofupilot.com/report). Default is None.
            attachments (Optional[List[str]], optional): [A list of file paths for attachments to include with the test run](https://docs.tofupilot.com/attachments). Default is None.

        Returns:
            dict: A dictionary containing the following keys:
                - success (bool): Whether the test run creation was successful.
                - message (Optional[dict]): Contains URL if successful.
                - status_code (Optional[int]): HTTP status code of the response.
                - error (Optional[dict]): Error message if any.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
            requests.RequestException: If a network error occurred.
            Exception: For any other exceptions that might occur.

        """
        self._logger.info("Run creation started...")

        if attachments is not None:
            validate_attachments(
                self._logger,
                attachments,
                self._max_attachments,
                self._max_file_size,
            )

        payload = {
            "procedure_id": procedure_id,
            "unit_under_test": unit_under_test,
            "run_passed": run_passed,
            "client": "Python",
            "client_version": self._current_version,
        }

        if steps is not None:
            for step in steps:
                if step["duration"] is not None:
                    step["duration"] = timedelta_to_iso(step["duration"])
                if step["started_at"] is not None:
                    step["started_at"] = datetime_to_iso(step["started_at"])
            payload["steps"] = steps

        if duration is not None:
            payload["duration"] = timedelta_to_iso(duration)

        if sub_units is not None:
            payload["sub_units"] = sub_units

        if report_variables is not None:
            payload["report_variables"] = report_variables

        try:
            response = requests.post(
                f"{self._base_url}/runs",
                json=payload,
                headers=self._headers,
                timeout=SECONDS_BEFORE_TIMEOUT,
            )
            response.raise_for_status()
            json_response = response.json()

            warnings: Optional[List[str]] = json_response.get("warnings")
            if warnings:
                for warning in warnings:
                    self._logger.warning(warning)

            message = json_response.get("message")
            self._logger.success(message)

            run_id = json_response.get("id")

            try:
                if attachments:
                    handle_attachments(
                        self._logger, self._headers, self._base_url, attachments, run_id
                    )
            except Exception as e:
                self._logger.error(e)
                return {
                    "success": False,
                    "message": None,
                    "status_code": None,
                    "error": {"message": str(e)},
                }
            return {
                "success": True,
                "message": message,
                "status_code": response.status_code,
                "error": None,
            }
        except requests.exceptions.HTTPError as http_err:
            error_message = parse_error_message(http_err.response)
            self._logger.error(error_message)
            return {
                "success": False,
                "message": None,
                "status_code": http_err.response.status_code,
                "error": {"message": error_message},
            }
        except requests.RequestException as e:
            self._logger.error("Network error: %s", e)
            return {
                "success": False,
                "message": None,
                "status_code": None,
                "error": {"message": str(e)},
            }
        except Exception as e:
            error_message = f"Failed to create test run: {e}"
            self._logger.error(error_message)
            return {
                "success": False,
                "message": None,
                "status_code": None,
                "error": {"message": error_message},
            }


def print_version_banner(current_version: str):
    """Prints current version of client"""
    banner = f"""
    TofuPilot Python Client {current_version}
    """
    print(banner.strip())
