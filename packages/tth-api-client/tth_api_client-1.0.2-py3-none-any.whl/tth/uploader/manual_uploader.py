import getopt
import logging
import os
import sys

from tth.uploader.settings import mandatory_options_provided
from tth.uploader.utils import parse_report_tags
from tth.uploader.report_handler import retrieve_allure_history, merge_allure_results, generate_allure_report, \
    generate_allure_results, send_report, get_report_summary, copy_allure_report, \
    clean_temp_files

log = logging.getLogger()


def manual_upload():
    if not mandatory_options_provided():
        raise Exception("Typhoon Test Hub mandatory environment variables not defined - "
                        "please define TTH_URL and TTH_API_KEY")

    allure_temp_results, allure_temp_report, allure_results_dir = None, None, ""
    allure_results_directory, allure_report_directory, report_tags, merge_results = __get_config_arguments()
    try:
        if allure_results_directory is not None and merge_results:
            allure_temp_results, history_destination, allure_results_dir = \
                merge_allure_results(allure_results_directory)
            retrieve_allure_history(history_destination, report_tags)
            allure_temp_report = generate_allure_report(allure_results_dir, os.path.dirname(allure_temp_results))
        elif allure_results_directory is not None and not merge_results:
            allure_temp_results = generate_allure_results(allure_results_directory)
            retrieve_allure_history(allure_temp_results, report_tags)
            allure_temp_report = generate_allure_report("\"" + allure_temp_results + "\"",
                                                        os.path.dirname(allure_temp_results))
        elif allure_report_directory is not None:
            allure_temp_report = copy_allure_report(allure_report_directory)
        else:
            raise Exception("Invalid parameter choice")

        started_at, ended_at, failed, broken, passed, skipped, unknown = get_report_summary(allure_temp_report)

        logging.info('Sending report to Typhoon Test Hub...')
        from tth.uploader.settings import EXECUTION
        successful_upload, report_id = send_report(allure_temp_report, report_tags, started_at, ended_at,
                                                   failed, broken, passed, skipped, unknown, execution_id=EXECUTION)
        if successful_upload:
            log.info('Report is sent to Typhoon Test Hub')
    except Exception as e:
        log.fatal(e)
        raise Exception("Error encountered when uploading report")
    finally:
        clean_temp_files([allure_temp_results, allure_temp_report])


def __get_config_arguments():
    allure_results_directory, allure_report_directory, report_tags, merge_results = None, None, None, False
    help_text = 'Uploading report that is already generated: \n' \
                'python -m tth-upload \n' + \
                '--report-path=<directory_with_allure_report> \n' + \
                '--report-tags=<report_tag>. \n\n' + \
                'Generating report based on obtained results and uploading generated report: \n' \
                'python -m tth-upload \n' + \
                '--results-path=<directory_with_allure_results> \n' + \
                '--report-tags=<report_tag>. \n\n' + \
                'Either results-path or report-path parameter should be defined. ' \
                'Defining both parameters would result in Exception so only one of them should be defined. ' \
                'Parameter report-tags, is optional.\n' + \
                'By adding --merge-results parameter, <directory_with_allure_results> parameter should point to ' + \
                'a directory with multiple allure-results directory. This would result in generating merged Allure ' \
                'report consisting of multiple allure-results.'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm", ["results-path=", "results=", "report-path=", "report=",
                                                        "report-tags=", "rt=", "merge-results"])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_text)
            sys.exit()
        if opt in ("-m", "--merge-results"):
            merge_results = True
        elif opt in ("--results", "--results-path"):
            allure_results_directory = arg
        elif opt in ("--report", "--report-path"):
            allure_report_directory = arg
        elif opt in ("--rt", "--report-tags"):
            report_tags = arg

    if allure_results_directory is None and allure_report_directory is None:
        raise Exception("Either results-path or report-path should be defined - neither is defined")

    if allure_results_directory is not None and allure_report_directory is not None:
        raise Exception("Either results-path or report-path should be defined - both are defined")

    if allure_results_directory is not None and not os.path.isdir(allure_results_directory):
        raise Exception("Provided directory path with allure results is invalid")

    if allure_report_directory is not None and not os.path.isdir(allure_report_directory):
        raise Exception("Provided directory path with allure results is invalid")

    report_tags = parse_report_tags(report_tags) if report_tags is not None else None

    return allure_results_directory, allure_report_directory, report_tags, merge_results
