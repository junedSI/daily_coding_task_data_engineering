"""
    Script to export single visual from Power BI within a specified workspace in PNG format.

    This script retrieves a list of reports from the Power BI workspace (specified by `group_id`) 
    and iteratively exports each report as a PNG file using the Power BI REST API. The exported 
    files are saved locally with unique filenames. The script handles:
    - Authentication with Azure AD.
    - Fetching reports from the workspace.
    - Polling to wait for the export to complete.

    Usage:
    - Ensure you have provided the correct `group_id` (workspace ID).
    - Run the script to automatically download all reports in the workspace.

    Dependencies:
    - asyncio
    - Your custom `exporter` module with the `export_power_bi_report` function.

"""

