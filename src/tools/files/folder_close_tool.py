import pygetwindow as gw
from crewai.tools import tool

@tool("folder_close_tool")
def close_folder_window(title_contains="File Explorer"):
    """
    Close an open folder (File Explorer) window.
    Args:
        title_contains (str): A part of the window title (e.g., 'Desktop', 'Documents').
    """
    windows = gw.getWindowsWithTitle(title_contains)
    if not windows:
        return f"No window found containing '{title_contains}'"
    for win in windows:
        win.close()
    return f"Closed {len(windows)} window(s) containing '{title_contains}'"