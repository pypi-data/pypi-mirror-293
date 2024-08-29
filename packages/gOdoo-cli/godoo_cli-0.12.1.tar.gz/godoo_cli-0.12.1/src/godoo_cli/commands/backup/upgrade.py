import logging
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Literal

import typer
from typing_extensions import Annotated

from ...cli_common import CommonCLI
from ...helpers.system import typer_ask_overwrite_path

LOGGER = logging.getLogger(__name__)
CLI = CommonCLI()


@CLI.arg_annotator
def run_upgrade(
    dump_path: Annotated[
        Path, typer.Argument(..., help="Path to SQL Dump", file_okay=True, dir_okay=False, exists=True)
    ],
    enterprise_subcode: Annotated[
        str, typer.Option(help="Odoo.com Enterprise Subcode", envvar="ODOO_ENTERPRISE_SUBCODE")
    ],
    target_version: Annotated[str, typer.Option(help="Target Odoo Version", envvar="ODOO_UPGRADE_TARGET_VERSION")],
    db_host=CLI.database.db_host,
    db_port=CLI.database.db_port,
    db_name=CLI.database.db_name,
    db_user=CLI.database.db_user,
    db_password=CLI.database.db_password,
    upgrade_mode: Annotated[Literal["test", "prod"], typer.Option("test", help="Odoo.com Upgrade Mode")] = "test",
):
    """Send SQL Dump to upgrade.odoo.com"""
    upgrade_zip_path = dump_path.parent / "upgrade.zip"

    if typer_ask_overwrite_path(upgrade_zip_path):
        backup_caches(upgrade_zip_path)
        run_upgrade_online(
            sql_dump_path=dump_path,
            enterprise_subcode=enterprise_subcode,
            target_version=target_version,
            upgrade_mode=upgrade_mode,
        )

    if not upgrade_zip_path.exists():
        LOGGER.error("Upgrade Failed: No upgrade.zip found")
        raise typer.Exit(1)

    LOGGER.info("Restoring Upgrade. Change Date: %s", upgrade_zip_path.stat().st_mtime)

    LOGGER.info("Extracting Upgrade Zip")
    ex_cache_path = upgrade_zip_path.parent / "upgrade_extract"
    with zipfile.ZipFile(upgrade_zip_path, "r") as zip_ref:
        zip_ref.extractall(ex_cache_path)

    LOGGER.info("Ensuring DB Dump is pg_custom format for rapid loading")


def run_upgrade_online(sql_dump_path: Path, enterprise_subcode: str, target_version: str, upgrade_mode: str):
    """Runs sql dump against upgrade.odoo.com"""
    command = f"python <(curl -s https://upgrade.odoo.com/upgrade) {upgrade_mode} -i {sql_dump_path.absolute()} -t {target_version} -x -c {enterprise_subcode}"
    LOGGER.info("Running Upgrade Command: %s", command)
    ret = subprocess.run(command, shell=True)
    if ret.returncode != 0:
        LOGGER.error("Upgrade Failed: %s", ret)
        raise typer.Exit(ret.returncode)


def backup_caches(upgrade_zip_path):
    if upgrade_zip_path.exists():
        LOGGER.info("Found existing upgrade.zip, backing up and Deleting")
        shutil.move(upgrade_zip_path, upgrade_zip_path.with_suffix(".old.zip"))
    log_path = upgrade_zip_path.parent / "upgrade.log"
    if log_path.exists():
        shutil.move(log_path, log_path.with_suffix(".old.log"))
    report_path = upgrade_zip_path.parent / "upgrade-report.html"
    if report_path.exists():
        shutil.move(report_path, report_path.with_suffix(".old.html"))
