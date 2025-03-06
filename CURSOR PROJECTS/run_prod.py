import os
from waitress import serve
from app import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the application
app = create_app('production')

if __name__ == '__main__':
    try:
        port = int(os.getenv('PORT', 3000))
        print(f"Starting production server...")
        print(f"Server will be available at:")
        print(f"http://127.0.0.1:{port}")
        print(f"http://localhost:{port}")
        print("\nPress Ctrl+C to stop the server")
        serve(app, host='127.0.0.1', port=port)
    except Exception as e:
        print(f"Error starting server: {e}") 