import os
import sys
print("Starting application...")
try:
    from app import app
    print("Successfully imported app")
except Exception as e:
    print(f"Error importing app: {str(e)}")
    sys.exit(1)

if __name__ == '__main__':
    print("Setting up environment...")
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    print("Starting server on http://localhost:5000")
    try:
        app.run(debug=True, port=5000)
    except Exception as e:
        print(f"Error running server: {str(e)}")
        sys.exit(1) 