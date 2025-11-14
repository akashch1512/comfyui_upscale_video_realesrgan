import requests
import os

def upload_to_api(file_path):
    """
    Uploads a single file to the Uguu.se API.
    """

    API_ENDPOINT = "https://uguu.se/upload"
    headers = {}

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    try:
        with open(file_path, 'rb') as f:
            files = {
                'files[]': (os.path.basename(file_path), f)
            }

            print(f"Uploading {file_path} to {API_ENDPOINT}...")
            response = requests.post(API_ENDPOINT, headers=headers, files=files)
            response.raise_for_status()

            response_data = response.json()
            print(f"Response Data: {response_data}")

            # ✅ Correct extraction for Uguu.se response
            if (
                "files" in response_data
                and isinstance(response_data["files"], list)
                and len(response_data["files"]) > 0
                and "url" in response_data["files"][0]
            ):
                return response_data["files"][0]["url"]
            else:
                print(f"Error: Could not extract URL. Response was: {response_data}")
                return None

    except requests.exceptions.RequestException as e:
        print(f"Error during file upload: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
