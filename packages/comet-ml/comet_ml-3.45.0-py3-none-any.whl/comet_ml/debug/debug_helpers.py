# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.com
#  Copyright (C) 2015-2024 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import logging

from comet_ml._logging import _get_comet_logging_config

LOGGER = logging.getLogger(__name__)


def error_mode() -> None:
    """Enables the printing of error tracebacks to the console logger for debugging purposes."""
    try:
        _get_comet_logging_config().enable_console_traceback()
    except Exception:
        LOGGER.warning("Failed to enable console traceback", exc_info=True)
