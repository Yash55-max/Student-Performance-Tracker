# Render/Railway Deployment Guide

## Quick Deploy to Render.com (Recommended)

### Option 1: One-Click Deploy via Dashboard

1. **Go to Render**: [https://render.com](https://render.com)
2. **Sign up/Login** with GitHub
3. **Click "New +"** → **"Web Service"**
4. **Connect Repository**: `Yash55-max/Student-Performance-Tracker`
5. **Configure**:
   - **Name**: `student-performance-tracker`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. **Click "Create Web Service"**
7. **Wait 2-3 minutes** for deployment

### Option 2: Using render.yaml (Automatic)

The repository includes a `render.yaml` file that automatically configures everything.

1. Go to [render.com](https://render.com)
2. Click "New +" → "Blueprint"
3. Connect your repository
4. Render will detect `render.yaml` and configure automatically
5. Click "Apply"

## Deploy to Railway.app (Alternative)

1. **Go to Railway**: [https://railway.app](https://railway.app)
2. **Sign up/Login** with GitHub
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose**: `Yash55-max/Student-Performance-Tracker`
6. Railway will automatically:
   - Detect it's a Python app
   - Install dependencies from `requirements.txt`
   - Start with `gunicorn app:app`
7. **Wait 2-3 minutes** for deployment

## Why Render/Railway?

### ✅ Advantages

- **Persistent Storage**: SQLite database persists across deployments
- **No Data Loss**: Students and grades are saved permanently
- **Export Works**: Export functionality works correctly
- **Free Tier**: Both offer free tiers for small projects
- **Easy Setup**: Minimal configuration required

### ❌ Vercel Issues (Why We're Moving)

- **Ephemeral Storage**: Database resets randomly
- **Data Loss**: Students disappear between requests
- **Export Fails**: Empty exports despite having data
- **Not Suitable**: For SQLite-based applications

## After Deployment

### Testing Your App

Once deployed, you'll get a URL like:
- Render: `https://student-performance-tracker.onrender.com`
- Railway: `https://student-performance-tracker.up.railway.app`

Test these features:
- ✅ Add students
- ✅ Add grades
- ✅ View student details
- ✅ Export data (should now work!)
- ✅ Subject toppers
- ✅ Class averages
- ✅ **Refresh the page** - data should persist!

### Important Notes

1. **Free Tier Limitations**:
   - Render: Service may sleep after 15 minutes of inactivity
   - Railway: 500 hours/month free tier
   
2. **First Request**: May take 30-60 seconds (cold start)

3. **Database Location**: 
   - Data stored in persistent disk
   - Survives deployments and restarts

## Troubleshooting

### Build Fails

Check that `requirements.txt` includes:
```
Flask==3.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

### App Won't Start

Ensure start command is: `gunicorn app:app`

### Port Issues

Render/Railway automatically set the PORT environment variable. The app should bind to `0.0.0.0:$PORT`.

## Keeping Both Deployments

You can keep both Vercel and Render deployments:
- **Vercel**: For testing serverless deployment
- **Render**: For actual production use with data persistence

## Next Steps

After successful deployment:
1. Test all features thoroughly
2. Add students and grades
3. Verify data persists after refresh
4. Test export functionality
5. Share your production URL!
