#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Nathan Liang

import time
import threading
import logging
from .ssh_connection import SSHConnectionManager
from .exceptions import SSHPromptError, SSHCommandTimeoutError, SSHConnectionError
from .fortigate_device import FortiGateDevice
from typing import Union, List, Optional
import traceback


class CommandExecutor:
    """Executes commands on a FortiGate device via SSH.

    Attributes:
        ssh_manager (SSHConnectionManager): Manages SSH connections to the device.
        retries (int): Number of times to retry a command in case of failure.
        prompt_patterns (Optional[List[str]]): List of regex patterns to identify various prompts.
    """

    def __init__(
        self,
        device: FortiGateDevice,
        logger: Optional[logging.Logger] = None,
        timeout: int = 10,
        log_level: Optional[int] = None,
        log_file: Optional[str] = None,
        retries: int = 3,
        prompt_patterns: Optional[List[str]] = None,
    ):
        """
        Initializes the CommandExecutor with a FortiGate device and configuration options.

        Args:
            device (FortiGateDevice): The FortiGate device to connect to.
            logger (Optional[logging.Logger]): Logger instance for logging messages.
            timeout (int): Timeout for SSH operations in seconds.
            log_level (Optional[int]): Logging level.
            log_file (Optional[str]): Path to the log file.
            retries (int): Number of retries for command execution.
            prompt_patterns (Optional[List[str]]): Patterns to identify SSH prompts.
        """
        # Initialize the SSHConnectionManager
        self.ssh_manager = SSHConnectionManager(
            device,
            logger=logger,
            timeout=timeout,
            log_level=log_level,
            log_file=log_file,
        )
        self.retries = retries
        self.prompt_patterns = prompt_patterns or [
            r".* (?:\(Interim\))?[\$#] ",  # Default prompt
            r".*\(y\/n\)",  # Yes/No prompt
            r"\(Press 'a' to accept\):",  # Press 'a' to accept prompt
            r".* login: ",  # Login prompt
            r"Password: ",  # Password prompt
        ]

    def __enter__(self):
        """Enter the context manager, establishing an SSH connection."""
        self.ssh_manager.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context manager, closing the SSH connection and logging any exceptions."""
        self.ssh_manager.close_connection()
        if exc_type:
            self.ssh_manager.logger.error(
                f"Exception in with block: {exc_type}, {exc_value}"
            )
            formatted_traceback = "".join(traceback.format_tb(traceback))
            self.ssh_manager.logger.error(f"Traceback details:\n{formatted_traceback}")

    def run(
        self,
        commands: Union[str, List[str]],
        delay: int = 0,
        follow_up_command: Optional[str] = None,
        timeout: int = 10,
        retries: int = 1,
        ensure_connection: bool = True,
        wait_for_prompt: bool = True,
    ) -> Optional[str]:
        """
        Executes a command or list of commands on the FortiGate device with options for delay, timeout, retries, and prompt waiting.

        Args:
            commands (Union[str, List[str]]): The command or list of commands to execute.
            delay (int): Delay in seconds before sending a follow-up command, if any.
            follow_up_command (Optional[str]): A command to send immediately after the main command.
            timeout (int): The maximum time to wait for command execution.
            retries (int): Number of times to retry the command if it fails.
            ensure_connection (bool): Whether to ensure the SSH connection is active before executing the command.
            wait_for_prompt (bool): Whether to wait for a prompt after executing the command.

        Returns:
            Optional[str]: The output of the command execution, or None if an error occurred.
        """
        if not isinstance(commands, list):
            commands = [commands]

        # Ensure the connection is established
        if ensure_connection and not self.ssh_manager.is_connected():
            try:
                self.ssh_manager.connect()
                self.ssh_manager.logger.info(
                    f"Connected to port {self.ssh_manager.device.port} successfully"
                )
            except SSHConnectionError as e:
                self.ssh_manager.logger.error(
                    f"Failed to connect to port {self.ssh_manager.device.port}: {e}"
                )
                return None

        output = ""
        for command in commands:
            command = self.__clean_command(command)

            try:
                self.ssh_manager.logger.debug(f"Executing command: {command}")

                # Check if the interaction is initialized
                if not self.ssh_manager.interaction:
                    raise SSHCommandTimeoutError(
                        "SSH connection not initialized. Please check the connection status."
                    )

                self.ssh_manager.interaction.send(command)

                if delay > 0:
                    self.ssh_manager.logger.debug(f"Waiting for {delay} seconds")
                    time.sleep(delay)

                if follow_up_command:
                    follow_up_command = self.__clean_command(follow_up_command)
                    self.ssh_manager.logger.debug(
                        f"Sending follow-up command: {follow_up_command}"
                    )
                    self.ssh_manager.interaction.send(follow_up_command)

                if wait_for_prompt:
                    if timeout > 0:
                        self._execute_with_timeout(
                            self._wait_for_prompt, timeout=timeout, retries=retries
                        )
                    else:
                        self._wait_for_prompt()

                    # Collect and clear the output after command execution if wait_for_prompt is True
                    output = self.__collect_and_clear_output()

            except Exception as e:
                self.ssh_manager.logger.error(
                    f"Exception while running command '{command}': {e}"
                )
                raise SSHCommandTimeoutError(f"Command '{command}' failed due to: {e}")

        return output.strip()

    def __collect_and_clear_output(self) -> str:
        """
        Collects the current accumulated output from the SSH session and clears it.

        Returns:
            str: The current accumulated output.
        """
        # Collect output and reset interaction's current_output_clean
        output = str(self.ssh_manager.interaction.current_output_clean or "").strip()
        self.ssh_manager.interaction.current_output_clean = (
            ""  # Clear the current output
        )
        return output

    def _wait_for_prompt(self, prompt_patterns: Optional[List[str]] = None):
        """
        Waits for and handles the expected prompt on the FortiGate device.

        Args:
            prompt_patterns (Optional[List[str]]): List of regex patterns to identify SSH prompts.
        """
        if prompt_patterns is None:
            prompt_patterns = self.prompt_patterns

        self.ssh_manager.logger.debug(
            f"port {self.ssh_manager.device.port} Waiting for prompt"
        )
        error_count = 0

        while True:
            self.ssh_manager.logger.debug(
                f"Current interaction output: {self.ssh_manager.interaction.current_output}"
            )
            found_index = self.ssh_manager.interaction.expect(
                prompt_patterns, timeout=self.ssh_manager.timeout
            )
            self.ssh_manager.logger.debug(f"Found index: {found_index}")
            if found_index == 0:
                self.ssh_manager.logger.debug(
                    f"port {self.ssh_manager.device.port} Main prompt detected."
                )
                break
            elif found_index in (1, 2):
                responses = ["y", "a"]
                self.ssh_manager.logger.debug(
                    f"port {self.ssh_manager.device.port} Detected special prompt. Sending '{responses[found_index-1]}'."
                )
                self.ssh_manager.interaction.send(responses[found_index - 1])
            elif found_index == 3:
                self.ssh_manager.logger.debug(
                    f"port {self.ssh_manager.device.port} Detected 'login:' prompt. Sending username."
                )
                self.ssh_manager.interaction.send(self.ssh_manager.device.user)
            elif found_index == 4:
                self.ssh_manager.logger.debug(
                    f"port {self.ssh_manager.device.port} Detected 'Password:' prompt. Sending password."
                )
                self.ssh_manager.interaction.send(self.ssh_manager.device.pwd)
            elif found_index == -1:
                error_count += 1
                self.ssh_manager.logger.debug(
                    f"Prompt not detected. Error count: {error_count}"
                )

            if error_count >= 3:
                self.ssh_manager.logger.error(
                    f"port {self.ssh_manager.device.port} Error count reached 3. Exiting."
                )
                raise SSHPromptError("Failed to detect prompt after multiple attempts.")

            time.sleep(1)

    def __clean_command(self, command: str) -> str:
        """
        Cleans the command string by stripping leading/trailing whitespace from each line.

        Args:
            command (str): The command string to clean.

        Returns:
            str: The cleaned command string.
        """
        return "\n".join(line.strip() for line in command.strip().splitlines())

    def _execute_with_timeout(
        self, func, *args, timeout: int, retries: int
    ) -> Optional[str]:
        """
        Executes a function with a timeout and retry mechanism.

        Args:
            func (callable): The function to execute.
            *args: Arguments to pass to the function.
            timeout (int): Maximum time to wait for the function execution in seconds.
            retries (int): Number of times to retry the function if it times out.

        Returns:
            Optional[str]: The result of the function execution or None if it timed out.
        """
        for attempt in range(retries):
            result = [None]

            def target():
                result[0] = func(*args)

            thread = threading.Thread(target=target)
            thread.start()

            thread.join(timeout)
            if thread.is_alive():
                self.ssh_manager.logger.debug(
                    f"Attempt {attempt + 1} timed out. Retrying..."
                )
                if attempt < retries - 1:
                    time.sleep(1)
                else:
                    self.ssh_manager.logger.error(
                        f"Function {func.__name__} timed out after {retries} attempts."
                    )
                    raise SSHCommandTimeoutError(
                        f"Function {func.__name__} timed out after {retries} attempts."
                    )
            else:
                return result[0]
        return None
