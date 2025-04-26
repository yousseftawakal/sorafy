# Sorafy - Image Processing Web Application

Sorafy is a web application that allows users to apply various image processing effects to their images in real-time. Built with a React frontend and Flask backend, it provides an intuitive interface for applying and combining multiple effects.

## Features

- **Real-time Image Processing**: Apply effects and see results instantly
- **Multiple Effects**: Choose from a variety of image processing effects:
  - Blur
  - Salt & Pepper Noise
  - Brightness Adjustment
  - Hue Rotation
  - Sharpening
  - Edge Detection
  - Neon Glow
  - Noise Removal
  - Grayscale Conversion
  - Saturation Adjustment
  - Color Inversion
- **Customizable Parameters**: Each effect comes with adjustable parameters
- **Effect Combination**: Apply multiple effects in sequence
- **Responsive Design**: Works on both desktop and mobile devices

## Tech Stack

### Frontend

- React.js
- Responsive design

### Backend

- Flask (Python)
- Pillow (Image Processing)
- NumPy & SciPy (Scientific Computing)
- Flask-CORS (Cross-Origin Resource Sharing)

## Installation

### Backend Setup

1. Navigate to the server directory:
   ```bash
   cd server
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the client directory:
   ```bash
   cd client
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Development Mode

1. Start the backend server:

   ```bash
   cd server
   python app.py
   ```

2. Start the frontend development server:
   ```bash
   cd client
   npm start
   ```

The application will be available at `http://localhost:3000`

### Production Build

1. Build the frontend:

   ```bash
   cd client
   npm run build
   ```

2. The backend is configured to serve the static files from the build directory.

## API Endpoints

- `POST /process`: Process an image with specified effects
- `GET /effects`: Get list of available effects and their parameters

## Deployment

The application is configured for deployment on Vercel. The `vercel.json` file contains the necessary configuration for serverless deployment.
