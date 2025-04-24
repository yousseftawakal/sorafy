from waitress import serve
print("Starting production server...")
from app import app

if __name__ == '__main__':
    print("Server is running at http://127.0.0.1:5000")
    serve(app, 
          host='127.0.0.1', 
          port=5000)