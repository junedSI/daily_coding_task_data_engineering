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
# import asyncio
# import aiohttp
# import time
# from enum import Enum
# from uuid import UUID
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# class FileFormat(Enum):
#     PDF = "PDF"
#     PNG = "PNG"

# class ExportState(Enum): 
#     SUCCEEDED = "Succeeded"
#     FAILED = "Failed"

# class PowerBIExporter:
#     def __init__(self, access_token, base_url="https://api.powerbi.com/v1.0/myorg"):
#         self.access_token = access_token
#         self.base_url = base_url
#         self.headers = {
#             "Authorization": f"Bearer {self.access_token}",
#             "Content-Type": "application/json"
#         }

#     async def list_reports(self, group_id: UUID):
#         url = f"{self.base_url}/groups/{group_id}/reports"
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=self.headers) as response:
#                 response.raise_for_status()
#                 result = await response.json()
#                 return result.get('value', [])

#     async def get_pages(self, group_id: UUID, report_id: UUID):
#         url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages"
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=self.headers) as response:
#                 response.raise_for_status()
#                 result = await response.json()
#                 return result.get('value', [])

#     async def get_visuals(self, group_id: UUID, report_id: UUID, page_name: str):
#         url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages/{page_name}"
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=self.headers) as response:
#                 response.raise_for_status()
#                 result = await response.json()
#                 return result.get('value', [])

#     async def export_power_bi_visual(self, report_id: UUID, group_id: UUID, page_name: str, visual_name: str, file_format: FileFormat, 
#                                      polling_timeout_minutes: int):
#         max_retries = 3
#         for attempt in range(max_retries):
#             try:
#                 export_id = await self.post_export_request(report_id, group_id, page_name, visual_name, file_format)
#                 export = await self.poll_export_request(report_id, group_id, export_id, polling_timeout_minutes)

#                 if export is None or export['status'] == ExportState.FAILED.value:
#                     if 'retryAfter' in export:
#                         await asyncio.sleep(export['retryAfter'])
#                         continue
#                     return None

#                 if export['status'] == ExportState.SUCCEEDED.value:
#                     return await self.get_exported_file(report_id, group_id, export)

#             except Exception as e:
#                 logging.error(f"Error during export attempt {attempt + 1}: {str(e)}")
#                 if attempt == max_retries - 1:
#                     raise

#         return None

#     async def post_export_request(self, report_id, group_id, page_name, visual_name, file_format):
#         url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages/{page_name}/visuals/{visual_name}/exportTo"
#         data = {
#             "format": file_format.value
#         }

#         async with aiohttp.ClientSession() as session:
#             async with session.post(url, headers=self.headers, json=data) as response:
#                 response.raise_for_status()
#                 result = await response.json()
#                 return result['id']

#     async def poll_export_request(self, report_id, group_id, export_id, polling_timeout_minutes):
#         url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/exports/{export_id}"
#         start_time = time.time()
#         while time.time() - start_time < polling_timeout_minutes * 60:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(url, headers=self.headers) as response:
#                     response.raise_for_status()
#                     result = await response.json()
#                     if result['status'] in [ExportState.SUCCEEDED.value, ExportState.FAILED.value]:
#                         return result
#             await asyncio.sleep(5)
#         return None

#     async def get_exported_file(self, report_id, group_id, export):
#         url = export['resourceLocation']
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=self.headers) as response:
#                 response.raise_for_status()
#                 content = await response.read()
#                 return {
#                     'content': content,
#                     'filename': f"{export['reportName']}_visual.{export['resourceFileExtension']}"
#                 }

# async def main():
#     access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyIsImtpZCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvYThlNWQ1NzEtNDNlOC00YzNjLTk2YmUtMzQ0MTU2Y2Y2ODg3LyIsImlhdCI6MTcyNTUyOTcyMywibmJmIjoxNzI1NTI5NzIzLCJleHAiOjE3MjU1MzQ3MjEsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBWlFBYS84WEFBQUF2anFuUGN2UFJKcjgvRWdKMkRXOElFMyt0VFlPSzIySS9QTVc3bEhvaWNzWUF2eHhOL21NVkRwcE1HTmJOeU9FNk1FSjZoRVFhWkN6ZWQ3eWhqd0FwMkVISlhTYm15OXRqWFhJM2JSZnlBRFNleG4xRUtFaUQzbVNuNDhlbGIxbVhud1FoR3Q5dTdzeVBFME5vWmQ1VzhSQXpuUlhDdFBjamdlNis3eUI0NW11ejBXUXEySEZrOW1zNkhYTVd1NS8iLCJhbXIiOlsicnNhIiwibWZhIl0sImFwcGlkIjoiODcxYzAxMGYtNWU2MS00ZmIxLTgzYWMtOTg2MTBhN2U5MTEwIiwiYXBwaWRhY3IiOiIwIiwiZGV2aWNlaWQiOiI0YWRiMDVhYS00YWQ5LTQ2MjAtYTAzZi0zYjYxOWIxM2FkYzciLCJmYW1pbHlfbmFtZSI6IkluYW1kYXIiLCJnaXZlbl9uYW1lIjoiSnVuZWQgU2hhYmJpciIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjEwMy42OC44LjIzNCIsIm5hbWUiOiJKdW5lZCBTaGFiYmlyIEluYW1kYXIiLCJvaWQiOiJmNWFlNmVhOC1kODY3LTQ5NDktYmRjMS1lOGE5ODFiMTVmMjgiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtMTI4MDAwNjAyNi0yODU0MDk1ODc5LTM2MDI2MDA3NzctMjU5NjkiLCJwdWlkIjoiMTAwMzIwMDI2QjUxRkM1OSIsInJoIjoiMC5BUklBY2RYbHFPaERQRXlXdmpSQlZzOW9od2tBQUFBQUFBQUF3QUFBQUFBQUFBRFdBSGcuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic2lnbmluX3N0YXRlIjpbImR2Y19tbmdkIiwiZHZjX2NtcCIsImttc2kiXSwic3ViIjoiT2FaSFVtVGZod21UQnhCSnItZm5KeTIyRGZ5d1dEcVppUDZNOWJfa1pRUSIsInRpZCI6ImE4ZTVkNTcxLTQzZTgtNGMzYy05NmJlLTM0NDE1NmNmNjg4NyIsInVuaXF1ZV9uYW1lIjoiSnVuZWQuaW5hbWRhckBpbGluay1zeXN0ZW1zLmNvbSIsInVwbiI6Ikp1bmVkLmluYW1kYXJAaWxpbmstc3lzdGVtcy5jb20iLCJ1dGkiOiJfLUJHS2dfQzhFaXVmWDhnczVyX0FBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2lkcmVsIjoiMSAxNCJ9.aFIpYhCnFiue_xYhMRs57HePxBGsWOESLxBgJYLt1hZkSbzUMXWT2Ux2nVe6GDNfNWG4tmQdsONnGQ-PfJAUXfZHmi1fN2ElB5nIfo3grIj6aY9DPnefKubztBsPIX86EaC8WcB-qlpU0XG5QaTm0G6UX_xG8iD5yMZbSDCqBppgsyVvHGDnD_VPtj9-hdJbjILTIIcURfjp-8w7LGBW11jkQ8qeH-MKiEk5ZFpX3iby5OSs_SGMbHWOZRbKOrKz7m8niklFp2b7zaTsfdFO5Vu2sLU_IAnzi3SBBmtGnODBmeyLMMqDo7K_QuuLLCtbI9meEe7_0FHli85a78IHZA"
#     group_id = UUID("c6b9b541-b534-4aba-9221-1c0dda5284b4")
    
#     exporter = PowerBIExporter(access_token)
    
#     try:
#         # List reports
#         reports = await exporter.list_reports(group_id)
#         logging.info(f"Found {len(reports)} reports:")
#         for report in reports:
#             logging.info(f"ID: {report['id']}, Name: {report['name']}")
    
#         if reports:
#             for report in reports:
#                 report_id = UUID(report['id'])
#                 logging.info(f"\nProcessing report: {report['name']} (ID: {report_id})")

#                 # List pages in the report
#                 pages = await exporter.get_pages(group_id, report_id)
#                 logging.info(f"Found {len(pages)} pages in the report:")
#                 for page in pages:
#                     logging.info(f"Name: {page['name']} - Display Name: {page['displayName']}")

#                 if pages:
#                     for page in pages:
#                         logging.info(f"\nProcessing page: {page['displayName']} (Name: {page['name']})")

#                         # List visuals on the page
#                         visuals = await exporter.get_visuals(group_id, report_id, page['name'])
#                         logging.info(f"Found {len(visuals)} visuals on the page:")
#                         for visual in visuals:
#                             logging.info(f"Name: {visual['name']}, Type: {visual['type']}, Title: {visual.get('title', 'No title')}")

#                         if visuals:
#                             visual = visuals[0]
#                             logging.info(f"\nExporting visual: {visual['name']}")

#                             result = await exporter.export_power_bi_visual(
#                                 report_id, 
#                                 group_id,
#                                 page['name'],
#                                 visual['name'],
#                                 FileFormat.PNG, 
#                                 polling_timeout_minutes=10
#                             )

#                             if result:
#                                 with open(result['filename'], 'wb') as f:
#                                     f.write(result['content'])
#                                 logging.info(f"Visual exported successfully as {result['filename']}")
#                             else:
#                                 logging.warning(f"Failed to export visual: {visual['name']}")
#                         else:
#                             logging.warning(f"No visuals found on page: {page['displayName']}")
#                 else:
#                     logging.warning(f"No pages found in report: {report['name']}")
#         else:
#             logging.warning("No reports found")
#     except Exception as e:
#         logging.error(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#      asyncio.run(main())



import asyncio
import aiohttp
from enum import Enum
from uuid import UUID

class FileFormat(Enum):
    PNG = "PNG"

class PowerBIExporter:
    def __init__(self, access_token, base_url="https://api.powerbi.com/v1.0/myorg"):
        self.access_token = access_token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    async def get_pages(self, group_id: UUID, report_id: UUID):
        url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get('value', [])

    async def get_visuals(self, group_id: UUID, report_id: UUID, page_name: str):
        url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages/{page_name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get('value', [])

    async def export_visual(self, group_id: UUID, report_id: UUID, page_name: str, visual_name: str):
        url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages/{page_name}/visuals/{visual_name}/exportTo"
        data = {"format": FileFormat.PNG.value}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as response:
                response.raise_for_status()
                export_data = await response.json()
                
            export_url = export_data.get('resourceLocation')
            if not export_url:
                print("Failed to get export URL")
                return None
            
            async with session.get(export_url, headers=self.headers) as response:
                response.raise_for_status()
                return await response.read()

async def main():
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyIsImtpZCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvYThlNWQ1NzEtNDNlOC00YzNjLTk2YmUtMzQ0MTU2Y2Y2ODg3LyIsImlhdCI6MTcyNTUyOTcyMywibmJmIjoxNzI1NTI5NzIzLCJleHAiOjE3MjU1MzQ3MjEsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBWlFBYS84WEFBQUF2anFuUGN2UFJKcjgvRWdKMkRXOElFMyt0VFlPSzIySS9QTVc3bEhvaWNzWUF2eHhOL21NVkRwcE1HTmJOeU9FNk1FSjZoRVFhWkN6ZWQ3eWhqd0FwMkVISlhTYm15OXRqWFhJM2JSZnlBRFNleG4xRUtFaUQzbVNuNDhlbGIxbVhud1FoR3Q5dTdzeVBFME5vWmQ1VzhSQXpuUlhDdFBjamdlNis3eUI0NW11ejBXUXEySEZrOW1zNkhYTVd1NS8iLCJhbXIiOlsicnNhIiwibWZhIl0sImFwcGlkIjoiODcxYzAxMGYtNWU2MS00ZmIxLTgzYWMtOTg2MTBhN2U5MTEwIiwiYXBwaWRhY3IiOiIwIiwiZGV2aWNlaWQiOiI0YWRiMDVhYS00YWQ5LTQ2MjAtYTAzZi0zYjYxOWIxM2FkYzciLCJmYW1pbHlfbmFtZSI6IkluYW1kYXIiLCJnaXZlbl9uYW1lIjoiSnVuZWQgU2hhYmJpciIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjEwMy42OC44LjIzNCIsIm5hbWUiOiJKdW5lZCBTaGFiYmlyIEluYW1kYXIiLCJvaWQiOiJmNWFlNmVhOC1kODY3LTQ5NDktYmRjMS1lOGE5ODFiMTVmMjgiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtMTI4MDAwNjAyNi0yODU0MDk1ODc5LTM2MDI2MDA3NzctMjU5NjkiLCJwdWlkIjoiMTAwMzIwMDI2QjUxRkM1OSIsInJoIjoiMC5BUklBY2RYbHFPaERQRXlXdmpSQlZzOW9od2tBQUFBQUFBQUF3QUFBQUFBQUFBRFdBSGcuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic2lnbmluX3N0YXRlIjpbImR2Y19tbmdkIiwiZHZjX2NtcCIsImttc2kiXSwic3ViIjoiT2FaSFVtVGZod21UQnhCSnItZm5KeTIyRGZ5d1dEcVppUDZNOWJfa1pRUSIsInRpZCI6ImE4ZTVkNTcxLTQzZTgtNGMzYy05NmJlLTM0NDE1NmNmNjg4NyIsInVuaXF1ZV9uYW1lIjoiSnVuZWQuaW5hbWRhckBpbGluay1zeXN0ZW1zLmNvbSIsInVwbiI6Ikp1bmVkLmluYW1kYXJAaWxpbmstc3lzdGVtcy5jb20iLCJ1dGkiOiJfLUJHS2dfQzhFaXVmWDhnczVyX0FBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2lkcmVsIjoiMSAxNCJ9.aFIpYhCnFiue_xYhMRs57HePxBGsWOESLxBgJYLt1hZkSbzUMXWT2Ux2nVe6GDNfNWG4tmQdsONnGQ-PfJAUXfZHmi1fN2ElB5nIfo3grIj6aY9DPnefKubztBsPIX86EaC8WcB-qlpU0XG5QaTm0G6UX_xG8iD5yMZbSDCqBppgsyVvHGDnD_VPtj9-hdJbjILTIIcURfjp-8w7LGBW11jkQ8qeH-MKiEk5ZFpX3iby5OSs_SGMbHWOZRbKOrKz7m8niklFp2b7zaTsfdFO5Vu2sLU_IAnzi3SBBmtGnODBmeyLMMqDo7K_QuuLLCtbI9meEe7_0FHli85a78IHZA"
    group_id = UUID("04302e5f-5a67-42bc-af5f-a04a254768ed")
    report_id = UUID("0d9c09c3-97b4-46c5-82e1-95600eb35610")  
    
    exporter = PowerBIExporter(access_token)
    
    try:
        # Get pages
        pages = await exporter.get_pages(group_id, report_id)
        if not pages:
            print("No pages found in the report.")
            return

        # Use the first page
        first_page = pages[0]
        print(f"Using page: {first_page['displayName']} (Name: {first_page['name']})")

        # Get visuals on the first page
        visuals = await exporter.get_visuals(group_id, report_id, first_page['name'])
        if not visuals:
            print("No visuals found on the page.")
            return

        # Use the first visual
        first_visual = visuals[0]
        print(f"Exporting visual: {first_visual['name']}")

        # Export the visual
        image_data = await exporter.export_visual(group_id, report_id, first_page['name'], first_visual['name'])
        if image_data:
            filename = f"{first_visual['name']}.png"
            with open(filename, 'wb') as f:
                f.write(image_data)
            print(f"Visual exported successfully as {filename}")
        else:
            print("Failed to export visual.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())