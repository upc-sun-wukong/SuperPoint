#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import os
import sys
from threading import Timer
from contextlib import contextmanager

def flush():
    """Try to flush all stdio buffers, both from Python and from C."""
    try:
        sys.stdout.flush()
        sys.stderr.flush()
    except (AttributeError, ValueError, IOError):
        pass  # unsupported


@contextmanager
def capture_outputs(filename):
    """Capture stdout and stderr to a file and still output to console."""
    # Open the log file in append mode
    with open(filename, 'a+') as target:
        # Save the original stdout and stderr file descriptors
        original_stdout_fd = sys.stdout
        original_stderr_fd = sys.stderr

        # Redirect stdout and stderr to both console and file
        class TeeOutput:
            def __init__(self, stream1, stream2):
                self.stream1 = stream1  # Console
                self.stream2 = stream2  # File

            def write(self, data):
                self.stream1.write(data)  # Write to console
                self.stream2.write(data)  # Write to file

            def flush(self):
                self.stream1.flush()
                self.stream2.flush()

        sys.stdout = TeeOutput(original_stdout_fd, target)
        sys.stderr = TeeOutput(original_stderr_fd, target)

        try:
            yield
        finally:
            flush()  # Ensure all buffers are flushed

            # Restore original stdout and stderr
            sys.stdout = original_stdout_fd
            sys.stderr = original_stderr_fd

            # Close the target file
            target.close()
