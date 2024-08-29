import logging
import os
import pytest

from tth.uploader.report_handler import get_config_option, retrieve_allure_history, generate_allure_results, \
    generate_allure_report, clean_temp_files, create_zip_archive, send_report, get_report_summary
from tth.uploader.utils import parse_report_tags
from tth.uploader.settings import mandatory_options_provided


log = logging.getLogger()


def pytest_addoption(parser):
    parser.addoption("--tth-upload", action="store_true",
                     help="If defined, uploads Allure report to Typhoon Test Hub")
    parser.addoption("--typhoon-upload", action="store_true",
                     help="If defined, uploads Allure report to Typhoon Test Hub")
    parser.addoption("--report-tags", action="store", default="None",
                     help="Presents tag of report, e.g. --report-tags=TAG_NAMES")


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_sessionfinish(session):
    if session.config.getoption("--tth-upload") or session.config.getoption("--typhoon-upload"):
        if not mandatory_options_provided():
            raise Exception("Typhoon Test Hub mandatory environment variables not defined - "
                            "please define TTH_URL and TTH_API_KEY")
        report_tags = get_config_option(session.config.getoption("--report-tags"), None)
        report_tags = parse_report_tags(report_tags) if report_tags is not None else None
        allure_temp_results, allure_temp_report = None, None
        try:
            allure_dir = session.config.getoption("--alluredir")
            allure_temp_results = generate_allure_results(allure_dir)
            retrieve_allure_history(allure_temp_results, report_tags)
            allure_temp_report = \
                generate_allure_report('"' + allure_temp_results + '"',
                                       os.path.abspath(os.path.dirname(allure_dir)))

            started_at, ended_at, failed, broken, passed, skipped, unknown = \
                get_report_summary(allure_temp_report)

            log.info('Sending report to Typhoon Test Hub...')
            from tth.uploader.settings import EXECUTION
            successful_upload, report_id = send_report(allure_temp_report, report_tags, started_at, ended_at, failed,
                                                       broken, passed, skipped, unknown, execution_id=EXECUTION)
            if successful_upload:
                log.info('Report is sent to Typhoon Test Hub')
        except Exception as e:
            log.fatal(e)
        finally:
            clean_temp_files([allure_temp_results, allure_temp_report])
    yield
