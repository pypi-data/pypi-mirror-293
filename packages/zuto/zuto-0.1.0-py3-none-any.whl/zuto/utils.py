import pygetwindow as gw
import psutil


def get_newly_opened_windows(previous_windows, current_windows=None):
    """
    Compare a list of previous windows to the current windows and return a list of newly opened windows.

    Args:
        previous_windows (list): A list of pygetwindow.Window objects representing the previously open windows.
        current_windows (list, optional): A list of pygetwindow.Window objects representing the current windows.
            If not provided, the function will get the current windows using pygetwindow.getAllWindows().

    Returns:
        list: A list of pygetwindow.Window objects representing the newly opened windows.
    """
    if current_windows is None:
        current_windows = gw.getAllWindows()

    previous_hwnds = set(window._hWnd for window in previous_windows)
    newly_opened = [
        window for window in current_windows if window._hWnd not in previous_hwnds
    ]

    return newly_opened


def get_newly_created_processes(previous_processes, current_processes=None):
    """
    Compare a list of previous processes to the current processes and return a list of newly created processes.

    Args:
        previous_processes (list): A list of psutil.Process objects representing the previously existing processes.
        current_processes (list, optional): A list of psutil.Process objects representing the current processes.
            If not provided, the function will get the current processes using psutil.process_iter().

    Returns:
        list: A list of psutil.Process objects representing the newly created processes.
    """
    if current_processes is None:
        current_processes = list(psutil.process_iter())

    previous_pids = set(process.pid for process in previous_processes)
    newly_created = [
        process for process in current_processes if process.pid not in previous_pids
    ]

    return newly_created
