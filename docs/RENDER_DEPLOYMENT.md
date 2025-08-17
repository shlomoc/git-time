# Render.com Deployment Guide for GitTime

## Overview
This guide covers deploying the GitTime application to Render.com using their Blueprint (Infrastructure-as-Code) approach.

## Architecture
- **Backend**: FastAPI Web Service (Python)
- **Frontend**: React Static Site (Vite build)
- **Database**: None required (uses temporary git clones)
- **External APIs**: OpenAI GPT-4o

## Pre-Deployment Setup

### 1. Environment Variables Required

#### Backend Service (gittime-backend)
```
OPENAI_API_KEY=sk-your-openai-api-key-here
FRONTEND_URL=https://gittime-frontend.onrender.com  # Optional, for additional CORS
```

#### Frontend Service (gittime-frontend)
```
VITE_API_URL=https://gittime-backend.onrender.com  # Automatically set by render.yaml
```

### 2. Required Files
- `render.yaml` - Blueprint configuration (already created)
- `backend/requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies

## Deployment Steps

### Option 1: Using Render Blueprint (Recommended)

1. **Push to GitHub**: Ensure your code is in a GitHub repository
2. **Connect to Render**: 
   - Go to [render.com](https://render.com)
   - Sign up/login with GitHub
   - Create new "Blueprint"
   - Connect your repository
3. **Configure Environment Variables**:
   - Set `OPENAI_API_KEY` in the backend service settings
   - Render will automatically configure `VITE_API_URL` based on the blueprint
4. **Deploy**: Render will automatically deploy both services

### Option 2: Manual Service Creation

If you prefer to create services manually:

#### Backend Web Service
```
Name: gittime-backend
Environment: Python 3
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### Frontend Static Site
```
Name: gittime-frontend
Environment: Static Site
Build Command: npm install && npm run build
Publish Directory: ./dist
```

## Service URLs
After deployment, your services will be available at:
- Backend: `https://gittime-backend.onrender.com`
- Frontend: `https://gittime-frontend.onrender.com`

## Environment Configuration

### Backend Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o access | Yes |
| `FRONTEND_URL` | Additional frontend URL for CORS | Optional |
| `PORT` | Server port (auto-set by Render) | Auto |

### Frontend Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL (auto-set by blueprint) | Auto |

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure frontend URL is correctly set in backend CORS configuration
   - Check that `VITE_API_URL` points to the correct backend URL

2. **OpenAI API Errors**
   - Verify `OPENAI_API_KEY` is set correctly
   - Ensure your OpenAI account has GPT-4o access

3. **Build Failures**
   - Backend: Check Python version compatibility (3.8+)
   - Frontend: Ensure all npm dependencies are in package.json

4. **Slow Initial Requests**
   - Render free tier services "spin down" after inactivity
   - First request may take 30+ seconds to wake up

### Health Checks
- Backend health endpoint: `https://gittime-backend.onrender.com/health`
- Frontend should load the React application

## Performance Considerations

### Free Tier Limitations
- Services spin down after 15 minutes of inactivity
- 750 hours/month total across all services
- No persistent storage (uses temporary git clones)

### Optimization Tips
- Backend includes smart caching (30 minutes)
- Git operations use shallow cloning for performance
- Consider upgrading to paid tier for production use

## Security Notes
- CORS is configured for specific origins (no wildcards in production)
- OpenAI API key is stored securely in environment variables
- No sensitive data is logged or persisted

## Monitoring
- View logs in Render dashboard
- Backend includes structured logging for debugging
- Health check endpoint for service monitoring