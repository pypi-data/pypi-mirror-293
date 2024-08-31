#!/usr/bin/python3
# -*- coding: utf-8 -*-
from app.aws import upload_report_to_s3_bucket
from app.core import SensorControler, CannotReadScanData, BadManifestSyntax
from app import VERSION
from rich import print
from typing import NoReturn, Union

import typer
import sys


ERRNO = 1
app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True, add_completion=False, help=""
                                                                                                        "SensorMiddlware: Manage scans for aws cloud sensors.\n"
                                                                                                        f"Version: {VERSION}")

sensor_controler: Union[None, SensorControler] = None


@app.command(short_help="Run cloud scan, specify where the scan data is stored (envvar/...)")
def runscan() -> NoReturn:
    print('[bold green] Starting scan ... [/bold green]')

    try:
        scontrol = SensorControler()
    except (CannotReadScanData, RuntimeError, BadManifestSyntax) as e:
        print('[bold red] Error: [/bold red]', e)
        SensorControler.fail_scan(str(e))
        sys.exit(ERRNO) # noqa

    # Todo: Retry ?
    is_scan_started, errmsg = scontrol.start_scan()
    if not is_scan_started:
        print('[bold red] Error: [/bold red] Scan could not be started. Reason:', errmsg)
        SensorControler.fail_scan(str(errmsg))
        sys.exit(ERRNO) # noqa

    print('[bold green] Waiting for scan to finish ... [/bold green]')
    is_scan_finished_with_success = scontrol.wait_scan()
    if not is_scan_finished_with_success:
        print('[bold red] Scan finished with error. [/bold red]')
        SensorControler.fail_scan(str(errmsg))
        sys.exit(ERRNO) # noqa

    print('[bold green] Scan finished successfully. [/bold green]')
    print('[bold green] Getting scan results ... [/bold green]')

    # Todo: Retry ?
    gotfindings, scan_report, errmsg = scontrol.get_report()
    if not gotfindings:
        print('[bold red] Error: [/bold red] Could not get scan findings.')
        SensorControler.fail_scan(str(errmsg))
        sys.exit(ERRNO) # noqa

    # UPLOAD REPORT TO S3 BUCKET
    upload_report_to_s3_bucket(scan_report)

    print('[bold green] Scan findings uploaded to s3 bucket. [/bold green]') # noqa
    SensorControler.finish_scan()


@app.command(short_help="Stop the current running scan.")
def stopscan(scan_id: str) -> NoReturn:
    raise NotImplementedError


def scontroler_main():
    app()
