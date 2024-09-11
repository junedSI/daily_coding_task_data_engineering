# import requests

# def export_visual(group_id, report_id, page_name, visual_id, access_token):
#     url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}/pages/{page_name}/exportToFile"
    
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json',
#     }
    
#     data = {
#         'format': 'PNG',
#         'width': 800,
#         'height': 600,
#     }
    
#     response = requests.post(url, headers=headers, json=data)
    
#     # Print the response status code and content for debugging
#     print(f"Status Code: {response.status_code}")
#     print(f"Response Content: {response.text}")
    
#     try:
#         return response.json()  # Try to return JSON if possible
#     except ValueError:
#         return {"error": "Invalid JSON response"}


# group_id = '04302e5f-5a67-42bc-af5f-a04a254768ed'  # Your workspace (group) ID
# report_id = '0d9c09c3-97b4-46c5-82e1-95600eb35610'  # Your report ID
# page_name = 'Customer'  # Replace with the actual page name, e.g., ReportSection1
# visual_id = '157d75e29c49c8468d27'  # The visual ID
# access_token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyIsImtpZCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvYThlNWQ1NzEtNDNlOC00YzNjLTk2YmUtMzQ0MTU2Y2Y2ODg3LyIsImlhdCI6MTcyNjAzMzcyOCwibmJmIjoxNzI2MDMzNzI4LCJleHAiOjE3MjYwMzkzNjcsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBWlFBYS84WEFBQUFrZmFXbEpvT2ZNOGlvc0JLbW0ySjBqS2ozSVJnWldjbUc3VDl1ME02Yy9aZ2pvTkFuODBiRS81S3RkTnRWL1dmOGplTld5TlhlOHN1Qis4L0pmUjZDR2Z6ampOeUJITlZNaUNHblJ1UVk4N0dFMHF1U3hpbk5uSWk1ZWNJeFVXM3BRL2FDS2dqUUJsQW83Y0J4N1NrZ3ZzN0dqeVdqVjhUYVhSaTFxSDkrTlFkaGFNd1ljNEdaVnNmcWVVNzlqUVgiLCJhbXIiOlsicnNhIiwibWZhIl0sImFwcGlkIjoiODcxYzAxMGYtNWU2MS00ZmIxLTgzYWMtOTg2MTBhN2U5MTEwIiwiYXBwaWRhY3IiOiIwIiwiZGV2aWNlaWQiOiI0YWRiMDVhYS00YWQ5LTQ2MjAtYTAzZi0zYjYxOWIxM2FkYzciLCJmYW1pbHlfbmFtZSI6IkluYW1kYXIiLCJnaXZlbl9uYW1lIjoiSnVuZWQgU2hhYmJpciIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjEwMy42OC44LjIzNCIsIm5hbWUiOiJKdW5lZCBTaGFiYmlyIEluYW1kYXIiLCJvaWQiOiJmNWFlNmVhOC1kODY3LTQ5NDktYmRjMS1lOGE5ODFiMTVmMjgiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtMTI4MDAwNjAyNi0yODU0MDk1ODc5LTM2MDI2MDA3NzctMjU5NjkiLCJwdWlkIjoiMTAwMzIwMDI2QjUxRkM1OSIsInJoIjoiMC5BUklBY2RYbHFPaERQRXlXdmpSQlZzOW9od2tBQUFBQUFBQUF3QUFBQUFBQUFBRFdBSGcuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic2lnbmluX3N0YXRlIjpbImR2Y19tbmdkIiwiZHZjX2NtcCIsImttc2kiXSwic3ViIjoiT2FaSFVtVGZod21UQnhCSnItZm5KeTIyRGZ5d1dEcVppUDZNOWJfa1pRUSIsInRpZCI6ImE4ZTVkNTcxLTQzZTgtNGMzYy05NmJlLTM0NDE1NmNmNjg4NyIsInVuaXF1ZV9uYW1lIjoiSnVuZWQuaW5hbWRhckBpbGluay1zeXN0ZW1zLmNvbSIsInVwbiI6Ikp1bmVkLmluYW1kYXJAaWxpbmstc3lzdGVtcy5jb20iLCJ1dGkiOiJXX1RVbXZ6clVFLVBLeFJWT1lDZ0FBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2lkcmVsIjoiMTAgMSJ9.YpgQGOVsyfi4OivSolRnmubPUvFzy7t4z1wsuBIeCWLeMB8Sv2PDoODJJjYBM4e2u0pfhn8EwjQ1Mk6mdXYrq_IiZruf0KAZVfmcNtadtAsK8Mnso2bsonhJioeUAuE6j9yIl9I0z609qMd7H-eyT_BsH9vYHZReB6ck6FBL_oDwEjCcA0IfokmLJJo3Kh62ln2JmDoY8q4B7rR912wPiNpSF7O2f3CjgUckDIdrl-L_zo3mHDDxxWt5hr8_tVDfrwTOH6RfQPIc73IJbftIXOoUO7EQgnzgh6lnFwAvPmPBh9JJgclsrvT5vcHATWBmIk_YvBzcRWUkgHAFGCa-SA'
# export_response = export_visual(group_id, report_id, page_name, visual_id, access_token)
# print(export_response)


import requests

def export_page(group_id, report_id, page_name, access_token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}/pages/{page_name}/exportToFile"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'format': 'PDF',  # You can change the format to PNG or PPTX if needed
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    # Check if the response is successful
    if response.status_code == 202:
        return response.json()  # The response will return a job ID for tracking export status
    else:
        return f"Error: {response.status_code} - {response.text}"

group_id = '04302e5f-5a67-42bc-af5f-a04a254768ed'  # Workspace (group) ID
report_id = '0d9c09c3-97b4-46c5-82e1-95600eb35610'  # Report ID
page_name = 'Customer'  # Replace with the actual page name
access_token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyIsImtpZCI6Ikg5bmo1QU9Tc3dNcGhnMVNGeDdqYVYtbEI5dyJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvYThlNWQ1NzEtNDNlOC00YzNjLTk2YmUtMzQ0MTU2Y2Y2ODg3LyIsImlhdCI6MTcyNjAzMzcyOCwibmJmIjoxNzI2MDMzNzI4LCJleHAiOjE3MjYwMzkzNjcsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBWlFBYS84WEFBQUFrZmFXbEpvT2ZNOGlvc0JLbW0ySjBqS2ozSVJnWldjbUc3VDl1ME02Yy9aZ2pvTkFuODBiRS81S3RkTnRWL1dmOGplTld5TlhlOHN1Qis4L0pmUjZDR2Z6ampOeUJITlZNaUNHblJ1UVk4N0dFMHF1U3hpbk5uSWk1ZWNJeFVXM3BRL2FDS2dqUUJsQW83Y0J4N1NrZ3ZzN0dqeVdqVjhUYVhSaTFxSDkrTlFkaGFNd1ljNEdaVnNmcWVVNzlqUVgiLCJhbXIiOlsicnNhIiwibWZhIl0sImFwcGlkIjoiODcxYzAxMGYtNWU2MS00ZmIxLTgzYWMtOTg2MTBhN2U5MTEwIiwiYXBwaWRhY3IiOiIwIiwiZGV2aWNlaWQiOiI0YWRiMDVhYS00YWQ5LTQ2MjAtYTAzZi0zYjYxOWIxM2FkYzciLCJmYW1pbHlfbmFtZSI6IkluYW1kYXIiLCJnaXZlbl9uYW1lIjoiSnVuZWQgU2hhYmJpciIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjEwMy42OC44LjIzNCIsIm5hbWUiOiJKdW5lZCBTaGFiYmlyIEluYW1kYXIiLCJvaWQiOiJmNWFlNmVhOC1kODY3LTQ5NDktYmRjMS1lOGE5ODFiMTVmMjgiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtMTI4MDAwNjAyNi0yODU0MDk1ODc5LTM2MDI2MDA3NzctMjU5NjkiLCJwdWlkIjoiMTAwMzIwMDI2QjUxRkM1OSIsInJoIjoiMC5BUklBY2RYbHFPaERQRXlXdmpSQlZzOW9od2tBQUFBQUFBQUF3QUFBQUFBQUFBRFdBSGcuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic2lnbmluX3N0YXRlIjpbImR2Y19tbmdkIiwiZHZjX2NtcCIsImttc2kiXSwic3ViIjoiT2FaSFVtVGZod21UQnhCSnItZm5KeTIyRGZ5d1dEcVppUDZNOWJfa1pRUSIsInRpZCI6ImE4ZTVkNTcxLTQzZTgtNGMzYy05NmJlLTM0NDE1NmNmNjg4NyIsInVuaXF1ZV9uYW1lIjoiSnVuZWQuaW5hbWRhckBpbGluay1zeXN0ZW1zLmNvbSIsInVwbiI6Ikp1bmVkLmluYW1kYXJAaWxpbmstc3lzdGVtcy5jb20iLCJ1dGkiOiJXX1RVbXZ6clVFLVBLeFJWT1lDZ0FBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2lkcmVsIjoiMTAgMSJ9.YpgQGOVsyfi4OivSolRnmubPUvFzy7t4z1wsuBIeCWLeMB8Sv2PDoODJJjYBM4e2u0pfhn8EwjQ1Mk6mdXYrq_IiZruf0KAZVfmcNtadtAsK8Mnso2bsonhJioeUAuE6j9yIl9I0z609qMd7H-eyT_BsH9vYHZReB6ck6FBL_oDwEjCcA0IfokmLJJo3Kh62ln2JmDoY8q4B7rR912wPiNpSF7O2f3CjgUckDIdrl-L_zo3mHDDxxWt5hr8_tVDfrwTOH6RfQPIc73IJbftIXOoUO7EQgnzgh6lnFwAvPmPBh9JJgclsrvT5vcHATWBmIk_YvBzcRWUkgHAFGCa-SA'


export_response = export_page(group_id, report_id, page_name, access_token)
print(export_response)
