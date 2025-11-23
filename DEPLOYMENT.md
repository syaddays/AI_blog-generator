# Deployment Guide

## Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python assessment.py

# Visit
http://127.0.0.1:5000
```

## Deploy to Render (Recommended)

### Step 1: Prepare Repository
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository
5. Render auto-detects settings from `render.yaml`
6. Add environment variable:
   - Key: `HUGGINGFACE_API_KEY`
   - Value: Your HuggingFace API key
7. Click "Create Web Service"
8. Wait 2-3 minutes for deployment
9. Visit your app at: `https://your-app-name.onrender.com`

### Render Configuration (Auto-detected)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn assessment:app`
- **Environment**: Python 3
- **Plan**: Free (750 hours/month)

## Deploy to Railway

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

### Step 2: Deploy
```bash
railway login
railway init
railway up
```

### Step 3: Add Environment Variable
```bash
railway variables set HUGGINGFACE_API_KEY=your_key_here
```

### Step 4: Get URL
```bash
railway domain
```

## Deploy to PythonAnywhere

### Step 1: Upload Files
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for free account
3. Go to "Files" tab
4. Upload `assessment.py` and `requirements.txt`

### Step 2: Install Dependencies
1. Go to "Consoles" tab
2. Start a Bash console
3. Run:
```bash
pip3 install --user -r requirements.txt
```

### Step 3: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Set source code path to your `assessment.py`
5. Set WSGI configuration:
```python
import sys
path = '/home/yourusername/'
if path not in sys.path:
    sys.path.append(path)

from assessment import app as application
```

### Step 4: Set Environment Variable
1. In Web tab, scroll to "Environment variables"
2. Add:
   - Name: `HUGGINGFACE_API_KEY`
   - Value: Your API key

### Step 5: Reload
Click "Reload" button

Visit: `https://yourusername.pythonanywhere.com`

## Deploy to Fly.io

### Step 1: Install Fly CLI
```bash
# macOS
brew install flyctl

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login
```bash
fly auth login
```

### Step 3: Create fly.toml
```toml
app = "your-app-name"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

### Step 4: Create Procfile
```
web: gunicorn assessment:app
```

### Step 5: Deploy
```bash
fly launch
fly secrets set HUGGINGFACE_API_KEY=your_key_here
fly deploy
```

Visit: `https://your-app-name.fly.dev`

## Deploy to Vercel (Serverless)

### Step 1: Create vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "assessment.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "assessment.py"
    }
  ]
}
```

### Step 2: Modify assessment.py
Add at the end:
```python
# For Vercel
app = app
```

### Step 3: Deploy
```bash
npm install -g vercel
vercel login
vercel
```

### Step 4: Set Environment Variable
```bash
vercel env add HUGGINGFACE_API_KEY
```

## Environment Variables

All platforms need:
- **HUGGINGFACE_API_KEY**: Your HuggingFace API key

Get your key at: https://huggingface.co/settings/tokens

## Custom Domain (Optional)

### Render
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records as instructed

### Railway
```bash
railway domain add yourdomain.com
```

### Fly.io
```bash
fly certs add yourdomain.com
```

## Monitoring

### Render
- Built-in logs and metrics
- View at: Dashboard → Your Service → Logs

### Railway
```bash
railway logs
```

### Fly.io
```bash
fly logs
```

## Troubleshooting

### Issue: App won't start
**Solution**: Check logs for errors
```bash
# Render: View in dashboard
# Railway: railway logs
# Fly.io: fly logs
```

### Issue: 502 Bad Gateway
**Solution**: 
- Check if gunicorn is installed
- Verify start command is correct
- Check port binding

### Issue: API errors
**Solution**:
- Verify HUGGINGFACE_API_KEY is set
- Check API key is valid
- Check API rate limits

### Issue: Slow cold starts
**Solution**:
- Use paid tier for always-on instances
- Or accept 10-30s cold start on free tier

### Issue: Out of memory
**Solution**:
- Upgrade to paid tier with more RAM
- Optimize code (already optimized)

## Scaling

### Free Tier Limits
- **Render**: 750 hours/month, sleeps after 15min
- **Railway**: $5 credit/month
- **PythonAnywhere**: 100s CPU/day
- **Fly.io**: 3 shared VMs

### Upgrade Options
- **Render**: $7/month for always-on
- **Railway**: Pay-as-you-go
- **Fly.io**: $1.94/month per VM

## Security Checklist

- [ ] Environment variables set (not hardcoded)
- [ ] HTTPS enabled (automatic on all platforms)
- [ ] Rate limiting enabled (3s cooldown)
- [ ] Input validation active
- [ ] No sensitive data in logs

## Backup

### Code Backup
```bash
git push origin main
```

### Environment Variables Backup
Save in password manager:
- HUGGINGFACE_API_KEY=xxx

## Maintenance

### Update Dependencies
```bash
pip install --upgrade Flask openai markdown gunicorn
pip freeze > requirements.txt
git commit -am "Update dependencies"
git push
```

### Monitor Usage
- Check HuggingFace API usage
- Monitor hosting platform usage
- Review error logs weekly

## Support

### Platform Support
- **Render**: https://render.com/docs
- **Railway**: https://docs.railway.app
- **PythonAnywhere**: https://help.pythonanywhere.com
- **Fly.io**: https://fly.io/docs

### API Support
- **HuggingFace**: https://huggingface.co/docs

---

**Recommended**: Start with Render for easiest deployment and best free tier.
