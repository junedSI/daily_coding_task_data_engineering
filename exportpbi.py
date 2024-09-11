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
# from enum import Enum
# from uuid import UUID

# class FileFormat(Enum):
#     PNG = "PNG"

# class PowerBIExporter:
#     def __init__(self, access_token, base_url="https://api.powerbi.com/v1.0/myorg"):
#         self.access_token = access_token
#         self.base_url = base_url
#         self.headers = {
#             "Authorization": f"Bearer {self.access_token}",
#             "Content-Type": "application/json"
#         }

#     async def get_pages(self, group_id: UUID, report_id: UUID):
#         url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages"
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=self.headers) as response:
#                 response.raise_for_status()
#                 result = await response.json()
#                 return result.get('value', [])

#     async def get_visuals(self, group_id: UUID, report_id: UUID, page_name: str):
#         url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages/{page_name}/visuals"
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=self.headers) as response:
#                 response.raise_for_status()
#                 result = await response.json()
#                 return result.get('value', [])

#     async def export_visual(self, group_id: UUID, report_id: UUID, page_name: str, visual_name: str):
#         url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages/{page_name}/visuals/{visual_name}/export"
#         data = {"format": FileFormat.PNG.value}
        
#         async with aiohttp.ClientSession() as session:
#             async with session.post(url, headers=self.headers, json=data) as response:
#                 response.raise_for_status()
#                 return await response.read()

#     async def update_visual_layout(self, group_id: UUID, report_id: UUID, page_name: str, visual_name: str, layout):
#         url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages/{page_name}/visuals/{visual_name}/layout"
#         async with aiohttp.ClientSession() as session:
#             async with session.patch(url, headers=self.headers, json=layout) as response:
#                 response.raise_for_status()
#                 return await response.json()

#     async def get_visual_layout(self, group_id: UUID, report_id: UUID, page_name: str, visual_name: str):
#         url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages/{page_name}/visuals/{visual_name}/layout"
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=self.headers) as response:
#                 response.raise_for_status()
#                 return await response.json()

# async def main():
#     access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyIsImtpZCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvYThlNWQ1NzEtNDNlOC00YzNjLTk2YmUtMzQ0MTU2Y2Y2ODg3LyIsImlhdCI6MTcyNTg4MTM2NywibmJmIjoxNzI1ODgxMzY3LCJleHAiOjE3MjU4ODY3OTksImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBWlFBYS84WEFBQUFoMkE5cEZtMkMvM3hWcUpwYm1LL2lqemhnOTVHVW5NNU9lUWVkYnlpL1BkMkc0QWhiZXQyS2pCeUNuOExWOGFLWW05cXY5c3UvTFVQME5EdlhmRzl5N09TSGY3TWk4ZU5ib1NRMzU5ZzgxQ3o4V2xpU0hpTVZEajFWRjZHZ29YMS93dUhJdkU5TzdGQmdOVEdUdGtRTExtK3BIOEFjS21MOU1tZkRZRGxrTFlIM3JzT1puTkdJYzh3YUF6RUlvWGoiLCJhbXIiOlsicnNhIiwibWZhIl0sImFwcGlkIjoiODcxYzAxMGYtNWU2MS00ZmIxLTgzYWMtOTg2MTBhN2U5MTEwIiwiYXBwaWRhY3IiOiIwIiwiZGV2aWNlaWQiOiI0YWRiMDVhYS00YWQ5LTQ2MjAtYTAzZi0zYjYxOWIxM2FkYzciLCJmYW1pbHlfbmFtZSI6IkluYW1kYXIiLCJnaXZlbl9uYW1lIjoiSnVuZWQgU2hhYmJpciIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjEwMy42OC44LjIzNCIsIm5hbWUiOiJKdW5lZCBTaGFiYmlyIEluYW1kYXIiLCJvaWQiOiJmNWFlNmVhOC1kODY3LTQ5NDktYmRjMS1lOGE5ODFiMTVmMjgiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtMTI4MDAwNjAyNi0yODU0MDk1ODc5LTM2MDI2MDA3NzctMjU5NjkiLCJwdWlkIjoiMTAwMzIwMDI2QjUxRkM1OSIsInJoIjoiMC5BUklBY2RYbHFPaERQRXlXdmpSQlZzOW9od2tBQUFBQUFBQUF3QUFBQUFBQUFBRFdBSGcuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic2lnbmluX3N0YXRlIjpbImR2Y19tbmdkIiwiZHZjX2NtcCIsImttc2kiXSwic3ViIjoiT2FaSFVtVGZod21UQnhCSnItZm5KeTIyRGZ5d1dEcVppUDZNOWJfa1pRUSIsInRpZCI6ImE4ZTVkNTcxLTQzZTgtNGMzYy05NmJlLTM0NDE1NmNmNjg4NyIsInVuaXF1ZV9uYW1lIjoiSnVuZWQuaW5hbWRhckBpbGluay1zeXN0ZW1zLmNvbSIsInVwbiI6Ikp1bmVkLmluYW1kYXJAaWxpbmstc3lzdGVtcy5jb20iLCJ1dGkiOiJuU2I4dkFHclUwdXNKUTVQWG1PUkFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2lkcmVsIjoiMSAxNCJ9.M_lTJS0XtQ6yfCU_Df7Jco5dFmSZpA5KxV_GrH37btnI07GX5QCqEdgWGUXTEhC8H_fn_WzLj2COlnmJgjCF6NkwQRI8SmauNXR9Pa6q4jFInTtcIGRrL1XNTEGIUx6EbHBmkwgY-ooko_IZTZw2LQUsx5TzHdkWMynqZ7r2btO-UEg8c1a3yK5A7AGth_FYCSeydSoYVJvaij71JySMgOSm_VS0KZgfQ9KUxvx0lTTKoPrL954_FapkELdg-q8PVLI6dCF9277O5g5xFFumsEqEP3_ffrHmnBz5ORsb3nnVR0iFD9HtO9yHRRlv9-C-CxmBvX754XYginQCgpYZ1Q"
#     group_id = UUID("04302e5f-5a67-42bc-af5f-a04a254768ed")
#     report_id = UUID("0d9c09c3-97b4-46c5-82e1-95600eb35610")  
    
#     exporter = PowerBIExporter(access_token)
    
#     try:
#         print(f"Fetching report details for report ID: {report_id}")
        
#         # Get pages
#         pages = await exporter.get_pages(group_id, report_id)
#         print(f"Number of pages found: {len(pages)}")
#         if not pages:
#             print("No pages found in the report.")
#             return

#         for page in pages:
#             print(f"Page: {page['displayName']} (ID: {page['name']})")
            
#             try:
#                 # Get visuals for each page
#                 visuals = await exporter.get_visuals(group_id, report_id, page['name'])
#                 print(f"  Number of visuals found: {len(visuals)}")
                
#                 for visual in visuals:
#                     print(f"  Visual: {visual.get('name', 'Unnamed')} (ID: {visual.get('name', 'Unknown')}, Type: {visual.get('type', 'Unknown')})")
                    
#                     # Get the current layout of the visual
#                     current_layout = await exporter.get_visual_layout(group_id, report_id, page['name'], visual['name'])
#                     print(f"  Current layout: {current_layout}")
                    
#                     # Example: Update the visual's position (move it 10 units to the right and 5 units down)
#                     new_layout = {
#                         "x": current_layout["x"] + 10,
#                         "y": current_layout["y"] + 5,
#                         "z": current_layout["z"],
#                         "width": current_layout["width"],
#                         "height": current_layout["height"],
#                         "displayState": current_layout["displayState"]
#                     }
                    
#                     # Update the visual's layout
#                     updated_layout = await exporter.update_visual_layout(group_id, report_id, page['name'], visual['name'], new_layout)
#                     print(f"  Updated layout: {updated_layout}")
                
#                 # Try to export the first visual of each page
#                 if visuals:
#                     first_visual = visuals[0]
#                     print(f"\nAttempting to export visual: {first_visual.get('name', 'Unnamed')} from page {page['displayName']}")
                    
#                     image_data = await exporter.export_visual(group_id, report_id, page['name'], first_visual['name'])
#                     if image_data:
#                         filename = f"{page['displayName']}_{first_visual['name']}.png"
#                         with open(filename, 'wb') as f:
#                             f.write(image_data)
#                         print(f"Visual exported successfully as {filename}")
#                     else:
#                         print("Failed to export visual.")
                
#             except Exception as e:
#                 print(f"  Error processing page {page['displayName']}: {str(e)}")

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         import traceback
#         traceback.print_exc()

# if __name__ == "__main__":
#     asyncio.run(main())

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

    async def get_report_status(self, group_id: UUID, report_id: UUID):
        url = f"{self.base_url}/groups/{group_id}/reports/{report_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                response.raise_for_status()
                return await response.json()

    async def get_active_page(self, group_id: UUID, report_id: UUID):
        url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                response.raise_for_status()
                pages = await response.json()
                # Assuming the first page is the active one
                return pages['value'][0] if pages['value'] else None

    async def get_visuals(self, group_id: UUID, report_id: UUID, page_name: str):
        url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages/{page_name}/visuals"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                response.raise_for_status()
                visuals = await response.json()
                return [
                    {
                        "name": visual.get("name"),
                        "type": visual.get("type"),
                        "title": visual.get("title"),
                        "layout": visual.get("layout")
                    }
                    for visual in visuals.get('value', [])
                ]

    async def export_visual(self, group_id: UUID, report_id: UUID, page_name: str, visual_name: str):
        url = f"{self.base_url}/groups/{group_id}/reports/{report_id}/pages/{page_name}/visuals/{visual_name}/export"
        data = {"format": FileFormat.PNG.value}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as response:
                response.raise_for_status()
                return await response.read()

async def main():
    access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkZEOTBEQkQ4Nzc3OTJGMjY2NjhBMTYyODIyQTkxREY4RTA2QzJBNDAiLCJ4NXQiOiJfWkRiMkhkNUx5Wm1paFlvSXFrZC1PQnNLa0EiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJ3ZXN0dXMucGJpZGVkaWNhdGVkLndpbmRvd3MubmV0IiwiZXhwIjoxNzI2MDM3NjMyLCJuYmYiOjE3MjYwMzM3MjgsIm9yaWdpbmFsQXV0aG9yaXphdGlvbkhlYWRlciI6IkJlYXJlciBleUowZVhBaU9pSktWMVFpTENKaGJHY2lPaUpTVXpJMU5pSXNJbmcxZENJNklrZzVibW8xUVU5VGMzZE5jR2huTVZOR2VEZHFZVll0YkVJNWR5SXNJbXRwWkNJNklrZzVibW8xUVU5VGMzZE5jR2huTVZOR2VEZHFZVll0YkVJNWR5SjkuZXlKaGRXUWlPaUpvZEhSd2N6b3ZMMkZ1WVd4NWMybHpMbmRwYm1SdmQzTXVibVYwTDNCdmQyVnlZbWt2WVhCcElpd2lhWE56SWpvaWFIUjBjSE02THk5emRITXVkMmx1Wkc5M2N5NXVaWFF2WVRobE5XUTFOekV0TkRObE9DMDBZek5qTFRrMlltVXRNelEwTVRVMlkyWTJPRGczTHlJc0ltbGhkQ0k2TVRjeU5qQXpNemN5T0N3aWJtSm1Jam94TnpJMk1ETXpOekk0TENKbGVIQWlPakUzTWpZd016a3pOamNzSW1GalkzUWlPakFzSW1GamNpSTZJakVpTENKaGFXOGlPaUpCV2xGQllTODRXRUZCUVVGclptRlhiRXB2VDJaTk9HbHZjMEpMYlcweVNqQnFTMm96U1ZKbldsZGpiVWMzVkRsMU1FMDJZeTlhWjJwdlRrRnVPREJpUlM4MVMzUmtUblJXTDFkbU9HcGxUbGQ1VGxobE9ITjFRaXM0TDBwbVVqWkRSMlo2YW1wT2VVSklUbFpOYVVOSGJsSjFVVms0TjBkRk1IRjFVM2hwYms1dVNXazFaV05KZUZWWE0zQlJMMkZEUzJkcVVVSnNRVzgzWTBKNE4xTnJaM1p6TjBkcWVWZHFWamhVWVZoU2FURnhTRGtyVGxGa2FHRk5kMWxqTkVkYVZuTm1jV1ZWTnpscVVWZ2lMQ0poYlhJaU9sc2ljbk5oSWl3aWJXWmhJbDBzSW1Gd2NHbGtJam9pT0RjeFl6QXhNR1l0TldVMk1TMDBabUl4TFRnellXTXRPVGcyTVRCaE4yVTVNVEV3SWl3aVlYQndhV1JoWTNJaU9pSXdJaXdpWkdWMmFXTmxhV1FpT2lJMFlXUmlNRFZoWVMwMFlXUTVMVFEyTWpBdFlUQXpaaTB6WWpZeE9XSXhNMkZrWXpjaUxDSm1ZVzFwYkhsZmJtRnRaU0k2SWtsdVlXMWtZWElpTENKbmFYWmxibDl1WVcxbElqb2lTblZ1WldRZ1UyaGhZbUpwY2lJc0ltbGtkSGx3SWpvaWRYTmxjaUlzSW1sd1lXUmtjaUk2SWpFd015NDJPQzQ0TGpJek5DSXNJbTVoYldVaU9pSktkVzVsWkNCVGFHRmlZbWx5SUVsdVlXMWtZWElpTENKdmFXUWlPaUptTldGbE5tVmhPQzFrT0RZM0xUUTVORGt0WW1Sak1TMWxPR0U1T0RGaU1UVm1NamdpTENKdmJuQnlaVzFmYzJsa0lqb2lVeTB4TFRVdE1qRXRNVEk0TURBd05qQXlOaTB5T0RVME1EazFPRGM1TFRNMk1ESTJNREEzTnpjdE1qVTVOamtpTENKd2RXbGtJam9pTVRBd016SXdNREkyUWpVeFJrTTFPU0lzSW5Kb0lqb2lNQzVCVWtsQlkyUlliSEZQYUVSUVJYbFhkbXBTUWxaek9XOW9kMnRCUVVGQlFVRkJRVUYzUVVGQlFVRkJRVUZCUkZkQlNHY3VJaXdpYzJOd0lqb2lkWE5sY2w5cGJYQmxjbk52Ym1GMGFXOXVJaXdpYzJsbmJtbHVYM04wWVhSbElqcGJJbVIyWTE5dGJtZGtJaXdpWkhaalgyTnRjQ0lzSW10dGMya2lYU3dpYzNWaUlqb2lUMkZhU0ZWdFZHWm9kMjFVUW5oQ1NuSXRabTVLZVRJeVJHWjVkMWRFY1ZwcFVEWk5PV0pmYTFwUlVTSXNJblJwWkNJNkltRTRaVFZrTlRjeExUUXpaVGd0TkdNell5MDVObUpsTFRNME5ERTFObU5tTmpnNE55SXNJblZ1YVhGMVpWOXVZVzFsSWpvaVNuVnVaV1F1YVc1aGJXUmhja0JwYkdsdWF5MXplWE4wWlcxekxtTnZiU0lzSW5Wd2JpSTZJa3AxYm1Wa0xtbHVZVzFrWVhKQWFXeHBibXN0YzNsemRHVnRjeTVqYjIwaUxDSjFkR2tpT2lKWFgxUlZiWFo2Y2xWRkxWQkxlRkpXVDFsRFowRkJJaXdpZG1WeUlqb2lNUzR3SWl3aWQybGtjeUk2V3lKaU56bG1ZbVkwWkMwelpXWTVMVFEyT0RrdE9ERTBNeTAzTm1JeE9UUmxPRFUxTURraVhTd2llRzF6WDJsa2NtVnNJam9pTVRBZ01TSjkuWXBnUUdPVnN5Zmk0T2l2U29sUm5tdWJQVXZGenk3dDR6MXdzdUJJZUNXTGVNQjhTdjJQRG9PREpKallCTTRlMnUwcGZobjhFd2pRMU1rNm1kWFlycV9JaVpydWYwS0FaVmZtY050YWR0QXNLOE1uc28yYnNvbmhKaW9lVUF1RTZqOXlJbDlJMHo2MDlxTWQ3SC1leVRfQnNIOXZZSFpSZUI2Y2s2RkJMX29Ed0VqQ2NBMElmb2ttTEpKbzNLaDYybG4ySm1Eb1k4cTRCN3JSOTEyd1BpTnBTRjdPMmYzQ2pnVWNrRElkcmwtTF96bzNtSEREeHhXdDVocjhfdFZEZnJ3VE9INlJmUVBJYzczSUpiZnRJWE9vVU83RVFnbnpnaDZsbkZ3QXZQbVBCaDlKSmdjbHNydlQ1dmNIQVRXQm1Ja19ZdkJ6Y1JXVWtnSEFGR0NhLVNBIiwicm9sbG91dEZxZG4iOiJ3ZXN0dXMucGJpZGVkaWNhdGVkLndpbmRvd3MubmV0IiwidmlydHVhbFNlcnZpY2VPYmplY3RJZCI6IkM2MjcxNEYzLTQxMUEtNDg3My1CQUVELUZEQ0E1MUM4NTM3NiIsIndvcmtsb2FkQ2xhaW1zIjoie1xyXG4gIFwid29ya2xvYWRUeXBlXCI6IFwiTm90ZWJvb2tcIixcclxuICBcIndvcmtzcGFjZU9iamVjdElkXCI6IFwiMDQzMDJlNWYtNWE2Ny00MmJjLWFmNWYtYTA0YTI1NDc2OGVkXCIsXHJcbiAgXCJ0ZW5hbnRJZFwiOiBcImE4ZTVkNTcxLTQzZTgtNGMzYy05NmJlLTM0NDE1NmNmNjg4N1wiLFxyXG4gIFwidXNlck9iamVjdElkXCI6IFwiZjVhZTZlYTgtZDg2Ny00OTQ5LWJkYzEtZThhOTgxYjE1ZjI4XCIsXHJcbiAgXCJ1c2VyUHJpbmNpcGFsTmFtZVwiOiBcIkp1bmVkLmluYW1kYXJAaWxpbmstc3lzdGVtcy5jb21cIixcclxuICBcImFydGlmYWN0c1wiOiBbXHJcbiAgICB7XHJcbiAgICAgIFwiYXJ0aWZhY3RPYmplY3RJZFwiOiBcIjhhODJmNjJjLWQ1MGItNGJmYi1hMzI2LTExNWYyODNjMzE0NlwiLFxyXG4gICAgICBcInBlcm1pc3Npb25zXCI6IDY3LFxyXG4gICAgICBcImV4dGVuZGVkUHJvcGVydGllc1wiOiB7fVxyXG4gICAgfVxyXG4gIF0sXHJcbiAgXCJ3b3Jrc3BhY2VQZXJtaXNzaW9uc1wiOiA5XHJcbn0iLCJ0b2tlblR5cGUiOiJNd2NUb2tlbiIsImN1c3RvbWVyQ2FwYWNpdHlPYmplY3RJZCI6Ijg5M0JDMDMyLUYzQjctNEZCQS04RkZCLTZFNDJBOUM5QUEyOSIsImlhdCI6MTcyNjAzNDAzMn0.NdD_Ny4lHwpVKSkx8fZpbgVnlc79G3l8Mbzq1x18c7e4hHI1ZPwz91ToiqqF-Jto35Hw_Pw43UvK0JJC3bznLAYsBag-Mi72O_pgh83wMxR54srMH5n6OHJNxazlXi1zVEK7yzDmR3DVnfHJnINuIVYs3pVX8JM3qgeJkSBTOC5mYgcGD0VNFIjdRkSt-Wd3L--9MHLXdjp3UPdq48iuGcCt-YHYBS8uNBWb80TLlXITSOyGETtMOghgRSKj_sOaY2orm8VHIK9LGScg0IkLQM0gJKsaV5Xj_c8IOPbT3qALCHIsIenCGWaubG5JtNddm3L5iFRKzVAsx4sDXAx-Jg"
    group_id = UUID("04302e5f-5a67-42bc-af5f-a04a254768ed")
    report_id = UUID("0d9c09c3-97b4-46c5-82e1-95600eb35610")   
    
    exporter = PowerBIExporter(access_token)
    
    try:
        print(f"Checking report status for report ID: {report_id}")
        
        # Check if the report is loaded
        report_status = await exporter.get_report_status(group_id, report_id)
        if report_status.get("status") != "Success":
            print(f"Report is not ready. Current status: {report_status.get('status')}")
            return

        print("Report is loaded. Proceeding to fetch active page and visuals.")

        # Get the active page
        active_page = await exporter.get_active_page(group_id, report_id)
        if not active_page:
            print("No active page found in the report.")
            return

        print(f"Active Page: {active_page['displayName']} (ID: {active_page['name']})")

        # Get visuals for the active page
        visuals = await exporter.get_visuals(group_id, report_id, active_page['name'])
        print(f"Number of visuals found: {len(visuals)}")

        for visual in visuals:
            print(f"Visual: {visual['name']}")
            print(f"  Type: {visual['type']}")
            print(f"  Title: {visual['title']}")
            print(f"  Layout: {visual['layout']}")
            print("---")

        # Try to export the first visual
        if visuals:
            first_visual = visuals[0]
            print(f"\nAttempting to export visual: {first_visual['name']} from page {active_page['displayName']}")
            
            image_data = await exporter.export_visual(group_id, report_id, active_page['name'], first_visual['name'])
            if image_data:
                filename = f"{active_page['displayName']}_{first_visual['name']}.png"
                with open(filename, 'wb') as f:
                    f.write(image_data)
                print(f"Visual exported successfully as {filename}")
            else:
                print("Failed to export visual.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())