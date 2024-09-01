#!/usr/bin/python3
# -*- coding: utf-8 -*-
from app.aws import upload_report_to_s3_bucket
from app.core import SensorControler, CannotReadScanData, BadManifestSyntax
from app import VERSION
from rich import print
from typing import NoReturn, Union

import typer
import os
import signal


ERRNO = 1
GUNICORN_PID_PATH = '/var/run/gunicorn.pid'
app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True, add_completion=False, help=""
                                                                                                        "SensorMiddlware: Manage scans for aws cloud sensors.\n"
                                                                                                        f"Version: {VERSION}")

sensor_controler: Union[None, SensorControler] = None


def full_exit():
    """
        Kill main container process
    :return:
    """
    try:
        with open(GUNICORN_PID_PATH, 'r', newline='\n') as pid:
            pid_str = pid.read()

            try:
                pid_int = int(pid_str)
            except ValueError:
                pass
            else:
                os.kill(pid_int, signal.SIGKILL)

    except (FileNotFoundError, ValueError):
        pass


@app.command(short_help="Run cloud scan, specify where the scan data is stored (envvar/...)")
def runscan() -> NoReturn:
    print('[bold green] Starting scan ... [/bold green]')

    try:
        scontrol = SensorControler()
    except (CannotReadScanData, RuntimeError, BadManifestSyntax) as e:
        print('[bold red] Error: [/bold red]', e)
        SensorControler.fail_scan(str(e))
        full_exit() # noqa

    print('[bold green] Waiting engine to start ... [/bold green]')
    try:
        scontrol.wait_engine()
    except RuntimeError as e:
        print('[bold red] Engine hang-up with error! [/bold red]')
        SensorControler.fail_scan(str(e))
        full_exit() # noqa

    # Todo: Retry ?
    is_scan_started, errmsg = scontrol.start_scan()
    if not is_scan_started:
        print('[bold red] Error: [/bold red] Scan could not be started. Reason:', errmsg)
        SensorControler.fail_scan(str(errmsg))
        full_exit() # noqa

    print('[bold green] Scan started')
    print('[bold green] Waiting for scan to finish ... [/bold green]')
    is_scan_finished_with_success = scontrol.wait_scan()
    if not is_scan_finished_with_success:
        print('[bold red] Scan finished with error. [/bold red]')
        SensorControler.fail_scan(str(errmsg))
        full_exit() # noqa

    print('[bold green] Scan finished successfully. [/bold green]')
    print('[bold green] Getting scan results ... [/bold green]')

    # Todo: Retry ?
    gotfindings, scan_report, errmsg = scontrol.get_report()
    if not gotfindings:
        print('[bold red] Error: [/bold red] Could not get scan findings.')
        SensorControler.fail_scan(str(errmsg))
        full_exit() # noqa

    # UPLOAD REPORT TO S3 BUCKET
    upload_report_to_s3_bucket(scan_report)

    print('[bold green] Scan findings uploaded to s3 bucket. [/bold green]') # noqa
    SensorControler.finish_scan()
    full_exit()


@app.command(short_help="Stop the current running scan.")
def stopscan(scan_id: str) -> NoReturn:
    raise NotImplementedError


def scontroler_main():
    try:
        app()
    except Exception as middleware_error: # noqa
        SensorControler.fail_scan(f'Critical middleware error: {str(middleware_error)}')
        full_exit() # noqa

