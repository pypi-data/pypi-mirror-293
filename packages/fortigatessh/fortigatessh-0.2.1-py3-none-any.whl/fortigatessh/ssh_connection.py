#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Nathan Liang

import atexit
import logging
import paramiko
from paramiko_expect import SSHClientInteraction
from .exceptions import SSHConnectionError
from .fortigate_device import FortiGateDevice
from typing import Optional
import traceback


class SSHConnectionManager:
    """Manages SSH connections to a FortiGate device.

    Attributes:
        device (FortiGateDevice): The device to connect to.
        timeout (int): Timeout for SSH operations in seconds.
        logger (Optional[logging.Logger]): Logger for output, creates a default logger if not provided.
        log_level (Optional[int]): The logging level for the built-in logger. Defaults to INFO if not provided.
        log_file (Optional[str]): File path to record the entire SSH session.
    """

    def __init__(
        self,
        device: FortiGateDevice,
        logger: Optional[logging.Logger] = None,
        timeout: int = 10,
        log_level: Optional[int] = None,
        log_file: Optional[str] = None,
    ):
        """
        Initializes the SSHConnectionManager with a FortiGate device and configuration options.

        Args:
            device (FortiGateDevice): The FortiGate device to connect to.
            logger (Optional[logging.Logger]): Logger instance for logging messages.
            timeout (int): Timeout for SSH operations in seconds.
            log_level (Optional[int]): Logging level for the logger.
            log_file (Optional[str]): Path to the log file for recording the SSH session.
        """
        self.device = device
        self.timeout = timeout
        self.logger = logger or self._create_default_logger(log_level or logging.INFO)

        # Set paramiko logging level to WARNING to reduce unnecessary output
        logging.getLogger("paramiko").setLevel(logging.WARNING)

        # Initialize session log file
        self._session_log_file = open(log_file, "w") if log_file else None

        self._client = None
        self._interaction = None
        atexit.register(self.close_connection)

    def _create_default_logger(self, log_level: int) -> logging.Logger:
        """
        Creates a default logger if none is provided.

        Args:
            log_level (int): The logging level to use for the default logger.

        Returns:
            logging.Logger: A configured logger instance.
        """
        logger = logging.getLogger(__name__)
        if not logger.hasHandlers():  # Only add handler if not already present
            handler = logging.StreamHandler()
            handler.setLevel(log_level)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(log_level)
        return logger

    def __enter__(self):
        """
        Supports the use of the 'with' statement by establishing an SSH connection.

        Returns:
            SSHConnectionManager: The current instance with an active SSH connection.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, tb_obj):
        """
        Ensures that the SSH connection is closed when exiting the 'with' block.

        Handles any exceptions raised within the 'with' block and logs the traceback.

        Args:
            exc_type (Optional[Type[BaseException]]): The exception type, if any.
            exc_value (Optional[BaseException]): The exception instance, if any.
            tb_obj (Optional[TracebackType]): The traceback object, if any.
        """
        if exc_type:
            self.logger.error(f"Exception in with block: {exc_type}, {exc_value}")
            formatted_traceback = "".join(traceback.format_tb(tb_obj))
            self.logger.error(f"Traceback details:\n{formatted_traceback}")
        self.close_connection()

    def connect(self):
        """Establishes an SSH connection to the FortiGate device.

        Raises:
            SSHConnectionError: If there is an authentication error, SSH error, or any unexpected error.
        """
        try:
            self.logger.debug(f"Connecting to {self.device.ip}:{self.device.port}")
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(
                self.device.ip,
                self.device.port,
                self.device.user,
                self.device.pwd,
                timeout=self.timeout,
            )
            self.logger.debug(f"Connected to {self.device.ip}:{self.device.port}")
            self._interaction = SSHClientInteraction(
                self._client,
                timeout=self.timeout,
                output_callback=self._log_output,
                newline="\n",
                display=True,
            )
        except paramiko.AuthenticationException:
            raise SSHConnectionError(
                f"Authentication failed when connecting to {self.device.ip}"
            )
        except paramiko.SSHException as e:
            raise SSHConnectionError(
                f"SSH error occurred when connecting to {self.device.ip}: {e}"
            )
        except Exception as e:
            raise SSHConnectionError(
                f"Unexpected error occurred when connecting to {self.device.ip}: {e}"
            )

    def is_connected(self) -> bool:
        """
        Checks if the SSH connection is still active.

        Returns:
            bool: True if the SSH connection is active, False otherwise.
        """
        return (
            self._client
            and self._client.get_transport()
            and self._client.get_transport().is_active()
        )

    def close_connection(self):
        """Ensures the SSH connection is closed cleanly.

        Raises:
            SSHConnectionError: If an error occurs while closing the connection.
        """
        try:
            if (
                self._client
                and self._client.get_transport()
                and self._client.get_transport().is_active()
            ):
                self._client.close()
                self.logger.debug(
                    f"Connection to {self.device.ip}:{self.device.port} closed."
                )
            if self._session_log_file:
                self._session_log_file.close()
        except Exception as e:
            self.logger.error(f"Failed to close connection: {e}")
            raise SSHConnectionError(f"Error closing connection: {e}")

    def _log_output(self, msg: str) -> None:
        """
        Logs the output from the SSH interaction.

        Args:
            msg (str): The message to log.
        """
        self.logger.debug(msg)
        if self._session_log_file:
            self._session_log_file.write(msg)
            self._session_log_file.flush()
