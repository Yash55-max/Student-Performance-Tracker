# Vercel Deployment Guide for Student Performance Tracker

## ⚠️ Important Notice About Data Persistence

**Your application uses SQLite, which has limitations on Vercel:**

- **Data is ephemeral**: The database resets on every deployment
- **Not suitable for production**: Data will be lost when Vercel restarts the serverless function
- **Temporary storage only**: Uses `/tmp` directory which is cleared periodically

### Recommended Solutions

For a production deployment with persistent data, consider:

1. **Migrate to PostgreSQL** using Vercel Postgres
2. **Deploy to alternative platforms**:
   - [Render.com](https://render.com) - Free tier, supports SQLite
   - [Railway.app](https://railway.app) - Free tier, supports SQLite
   - [PythonAnywhere](https://www.pythonanywhere.com) - Free tier available

## Deploying to Vercel (Testing Only)

### Prerequisites

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Create a Vercel account at [vercel.com](https://vercel.com)

### Deployment Steps

1. **Login to Vercel**:
   ```bash
   vercel login
   ```

2. **Deploy from your project directory**:
   ```bash
   vercel
   ```

3. **Follow the prompts**:
   - Set up and deploy: `Y`
   - Which scope: Select your account
   - Link to existing project: `N`
   - Project name: `student-performance-tracker` (or your choice)
   - Directory: `./` (current directory)
   - Override settings: `N`

4. **Production deployment**:
   ```bash
   vercel --prod
   ```

### What Was Changed

1. **Created `api/index.py`**: Vercel entry point for the Flask app
2. **Updated `vercel.json`**: Routes all requests to the API handler
3. **Modified `database.py`**: Uses `/tmp` directory when deployed to Vercel
4. **Updated `requirements.txt`**: Ensures all dependencies are installed

### Testing Your Deployment

After deployment, Vercel will provide a URL like:
```
https://student-performance-tracker-xxx.vercel.app
```

Visit this URL to test your application.

### Known Limitations on Vercel

- ❌ Database resets on each deployment
- ❌ Database resets when serverless function restarts
- ❌ Export feature may not work reliably
- ❌ Not suitable for storing real student data

### Alternative: Deploy to Render (Recommended)

Render supports persistent SQLite databases and is easier for this type of application:

1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add `gunicorn` to requirements.txt first

Would you like me to help you set up deployment for Render instead?

## Troubleshooting

### Error: "FUNCTION_INVOCATION_FAILED"

This error occurs when:
- Missing dependencies in `requirements.txt`
- Python version mismatch
- Database initialization fails

### Error: "500 Internal Server Error"

Check Vercel logs:
```bash
vercel logs
```

### Database Not Persisting

This is expected behavior on Vercel. Use a proper database service or alternative hosting platform.
