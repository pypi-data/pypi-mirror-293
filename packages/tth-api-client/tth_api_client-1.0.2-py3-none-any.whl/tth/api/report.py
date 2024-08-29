import os
import requests

from tth.uploader import report_handler
from tth.utils.exception import *


class ReportAPI:
    """
    Class that allows for interacting with reports via API.

    Attributes:
        client (object): client for sending requests to Typhoon Test Hub API
    """

    def __init__(self, client):
        self.client = client

    def get_info(self, report_id):
        """
        Obtain details of the Report with the provided report identifier.

        Args:
            report_id (int): Identifier of report

        Returns:
            data (dict): Report information

        Raises:
            APIException: Response status code not 200
        """
        response = requests.get(f"{self.client.url}/api/reports/status/{str(report_id)}",
                                headers=self.client.get_request_headers())
        if response.status_code == 200:
            return response.json()
        else:
            raise APIException(response)

    def upload_report(self, report_path, report_type="allure", report_tags=None, execution_id=None, summary=None,
                      summary_json=None, test_results=None, test_results_json=None):
        """
        Upload a report to Typhoon Test Hub.

        Args:
            report_path (str): Path to directory or file containing report
            report_type (str, optional): Type of report; can be one of the following values:

                - allure - requires for report_path value to be an Allure report
                - html - requires for report_path value to be a directory with html page
                - pdf - requires for report_path value to be a pdf file
                - custom - requires for report_path value to be a file or a directory that will be saved as a zip
                    archive

            report_tags (list, optional): List of report tags where each tag is a string value
            execution_id (int, optional): Identifier of the Execution to which the report should be assigned
            summary (dict, optional): Summary of report; dict with the following structure:

                ```
                {
                    "started_at": datetime_instance,
                    "ended_at": datetime_instance,
                    "failed": number_of_failed_tests,
                    "broken": number_of_broken_tests,
                    "passed": number_of_passed_tests,
                    "skipped": number_of_skipped_tests,
                    "unknown": number_of_unknown_tests
                }
                ```

                each of the keys is optional - for started_at and ended_at the default value is the current datetime,
                and for numbered parameters the default value is 0
            summary_json (str, optional): Path to JSON file containing summary; if summary parameter is defined,
                this parameter is ignored; if the started_at or ended_at parameters are provided, they should be dates
                in ISO 8601 format (the default value is the current datetime) while the numbered parameters
                if provided should be positive non-negative integers (the default value is 0)
            test_results (list, optional): List that contains results of all executed tests. Each element of the list
                should be a dictionary that represents a test suite with following three keys:

                - name (mandatory) - unique suite name
                - uid (optional) - suite identifier
                - tests (mandatory) - list of test results.

                Each element of test results (tests collection for each suite) should be a dictionary that represents
                a test with following three keys:

                - name (mandatory) - unique test name inside the suite
                - uid (optional) - test identifier
                - status (mandatory) - status of test; can be one of the following values (case-insensitive):
                    PASSED, FAILED, BROKEN, SKIPPED, UNKNOWN (default value)

                Example of the results object:

                ```
                [
                    {
                        "name": "suite_1",
                        "uid": "s1",
                        "tests": [
                            {
                                "name": "test_a",
                                "uid": "t_a",
                                "status": "PASSED"
                            },
                            {
                                "name": "test_b",
                                "uid": "t_b",
                                "status": "FAILED"
                            }
                        ]
                    },
                    {
                        "name": "suite_2",
                        "uid": "s2",
                        "tests": [
                            {
                                "name": "test_c",
                                "uid": "t_c",
                                "status": "BROKEN"
                            }
                        ]
                    }
                ]
                ```

            test_results_json (str, optional): Path to JSON file containing results; if results parameter is defined,
                this parameter is ignored

        Returns:
            result (int): Identifier of created report

        Raises:
            APIException: Response status code not 201
            UnsupportedReportTypeException: Invalid report type
            InvalidPathException: Invalid report path provided
            InvalidDataException: Invalid data provided
        """
        report_types = ["allure", "html", "pdf", "custom"]
        if report_type not in report_types:
            raise UnsupportedReportTypeException(report_type)

        report = os.path.abspath(str(report_path))
        if not os.path.exists(report):
            raise InvalidPathException(f"unknown path for {report_type} report")

        if summary_json is None:
            summary_json_path = None
        else:
            summary_json_path = os.path.abspath(summary_json)
            if not os.path.exists(summary_json_path) or not os.path.isfile(summary_json_path):
                raise InvalidPathException(f"unknown path of summary json file")

        if report_type == "allure":
            if not os.path.isdir(report_path):
                raise InvalidPathException(f"report path for {report_type} report should be directory")
        elif report_type == "html":
            if not os.path.isdir(report_path):
                raise InvalidPathException(f"report path for {report_type} report should be directory")
            home_pages = ["index.html", "report.html", "start.html", "home.html", "homepage.html"]
            home_page = None
            for page in home_pages:
                if os.path.exists(os.path.join(report, page)):
                    home_page = page
                    break
            if home_page is None:
                raise InvalidPathException(f"one of following HTML pages should be present"
                                           f"in html report: {', '.join(home_pages)}")
        elif report_type == "pdf":
            if not os.path.isfile(report_path):
                raise InvalidPathException(f"report path for {report_type} report should be file")

        if report_tags is None:
            report_tags = []
        else:
            report_tags = [str(tag) for tag in report_tags]

        started_at, ended_at, failed, broken, passed, skipped, unknown = \
            report_handler.generate_report_summary(report_path, report_type, summary, summary_json_path)

        test_results_data = report_handler.generate_test_results(test_results, test_results_json) \
            if test_results is not None or test_results_json is not None else None

        result = report_handler.send_report(report_path, report_tags, started_at, ended_at, failed, broken, passed,
                                            skipped, unknown, execution_id=execution_id, client=self.client,
                                            report_type=report_type, test_results=test_results_data)
        return result[1]

    def generate_and_upload_report(self, results_dir, merge_results=False, report_tags=None, execution_id=None):
        """
        Generate an Allure report based on Allure results

        Args:
            results_dir (string): Path to directory containing Allure results
            merge_results (bool, optional): Indicator whether results_dir points to directory with
                multiple Allure results which requires merging multiple Allure results into single Allure report
            report_tags (list, optional): List of report tags where each tag is a string value
            execution_id (int, optional): Identifier of execution to which report should be assigned

        Returns:
            status (int): Identifier of created report

        Raises:
            APIException: Response status code not 201
            InvalidPathException: Invalid report path provided
        """
        allure_results_directory = os.path.abspath(str(results_dir))
        if not os.path.exists(allure_results_directory):
            raise InvalidPathException(f"unknown path {results_dir}")

        if not os.path.isdir(allure_results_directory):
            raise InvalidPathException(f"{results_dir} should be directory")

        if report_tags is None:
            report_tags = []
        else:
            report_tags = [str(tag) for tag in report_tags]

        if merge_results:
            allure_temp_results, history_destination, allure_results_dir = \
                report_handler.merge_allure_results(allure_results_directory)
            report_handler.retrieve_allure_history(history_destination, report_tags)
            allure_temp_report = report_handler.generate_allure_report("\"" + allure_results_dir + "\"",
                                                                       os.path.dirname(allure_temp_results))
        else:
            allure_temp_results = report_handler.generate_allure_results(allure_results_directory)
            report_handler.retrieve_allure_history(allure_temp_results, report_tags)
            allure_temp_report = report_handler.generate_allure_report("\"" + allure_temp_results + "\"",
                                                                       os.path.dirname(allure_temp_results))

        started_at, ended_at, failed, broken, passed, skipped, unknown = \
            report_handler.get_report_summary(allure_temp_report)

        if execution_id is not None:
            execution_id = int(execution_id)

        result = report_handler.send_report(allure_temp_report, report_tags, started_at, ended_at, failed, broken,
                                            passed, skipped, unknown, execution_id=execution_id, client=self.client)

        report_handler.clean_temp_files([allure_temp_results, allure_temp_report])
        return result[1]
