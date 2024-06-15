import requests

# Define the URL of your Flask API
api_url = "http://192.168.18.19:5000/check"  # Replace with your actual IP address and port number

# Function to send a test request to the API
def test_api():
    # Example image file to send to the API
    image_file = "/home/kiq/Documents/ia_project/new_project/istockphoto-166678331-1024x1024.jpg"  # Replace with the path to your image file

    # Open the image file
    with open(image_file, "rb") as file:
        # Prepare the request data
        files = {"file": file}

        # Send a POST request to the API
        response = requests.post(api_url, files=files)

        # Print the response
        print("Response:")
        print(response.text)

# Run the test function
if __name__ == "__main__":
    test_api()
