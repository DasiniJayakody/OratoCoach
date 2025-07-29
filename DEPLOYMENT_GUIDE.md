# OratoCoach Deployment Guide

## Overview

OratoCoach is a Flask-based AI presentation analysis system that analyzes face, hands, and pose data using computer vision. This guide provides step-by-step instructions for deploying the application to make it accessible to users worldwide.

## Prerequisites

- Python 3.11+
- Git installed
- A code editor
- Webcam access (for local testing)

## Deployment Options

### Option 1: Heroku (Recommended for Beginners)

#### Step 1: Prepare Your Application

1. Ensure all files are committed to Git:

   ```bash
   git add .
   git commit -m "Prepare for deployment"
   ```

2. Install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli

#### Step 2: Deploy to Heroku

1. Login to Heroku:

   ```bash
   heroku login
   ```

2. Create a new Heroku app:

   ```bash
   heroku create oratocoach-app
   ```

3. Add buildpacks for OpenCV and MediaPipe:

   ```bash
   heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt
   heroku buildpacks:add heroku/python
   ```

4. Create `Aptfile` in your project root:

   ```
   libgl1-mesa-glx
   libglib2.0-0
   libsm6
   libxext6
   libxrender-dev
   libgomp1
   ```

5. Deploy your application:

   ```bash
   git push heroku main
   ```

6. Open your application:
   ```bash
   heroku open
   ```

### Option 2: Railway (Alternative Cloud Platform)

#### Step 1: Setup Railway

1. Go to https://railway.app/
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your OratoCoach repository

#### Step 2: Configure Environment

1. Add environment variables in Railway dashboard:
   - `FLASK_DEBUG=False`
   - `PORT=5000`

#### Step 3: Deploy

1. Railway will automatically detect your Flask app
2. Deploy and get your public URL

### Option 3: DigitalOcean App Platform

#### Step 1: Prepare for DigitalOcean

1. Create a `do-app.yaml` file:
   ```yaml
   name: oratocoach
   services:
     - name: web
       source_dir: /
       github:
         repo: your-username/OratoCoach
         branch: main
       run_command: gunicorn app:app
       environment_slug: python
       instance_count: 1
       instance_size_slug: basic-xxs
   ```

#### Step 2: Deploy

1. Go to DigitalOcean App Platform
2. Create new app from GitHub
3. Select your repository
4. Configure as shown above
5. Deploy

### Option 4: VPS Deployment (Advanced)

#### Step 1: Rent a VPS

- Recommended: DigitalOcean, Linode, or Vultr
- Minimum specs: 2GB RAM, 1 CPU, 20GB SSD

#### Step 2: Server Setup

1. Connect to your VPS via SSH
2. Update system:

   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. Install Python and dependencies:

   ```bash
   sudo apt install python3 python3-pip python3-venv nginx
   ```

4. Install system dependencies for OpenCV:
   ```bash
   sudo apt install libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
   ```

#### Step 3: Deploy Application

1. Clone your repository:

   ```bash
   git clone https://github.com/your-username/OratoCoach.git
   cd OratoCoach
   ```

2. Create virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create systemd service:

   ```bash
   sudo nano /etc/systemd/system/oratocoach.service
   ```

   Add this content:

   ```ini
   [Unit]
   Description=OratoCoach Flask App
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/OratoCoach
   Environment="PATH=/home/ubuntu/OratoCoach/venv/bin"
   ExecStart=/home/ubuntu/OratoCoach/venv/bin/gunicorn app:app -b 0.0.0.0:5000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

4. Start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start oratocoach
   sudo systemctl enable oratocoach
   ```

#### Step 4: Configure Nginx

1. Create Nginx configuration:

   ```bash
   sudo nano /etc/nginx/sites-available/oratocoach
   ```

   Add this content:

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

2. Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/oratocoach /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Option 5: Docker Deployment

#### Step 1: Create Dockerfile

Create a `Dockerfile` in your project root:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
```

#### Step 2: Deploy with Docker

1. Build the image:

   ```bash
   docker build -t oratocoach .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 oratocoach
   ```

## Post-Deployment Steps

### 1. Domain Configuration

- Purchase a domain (e.g., from Namecheap, GoDaddy)
- Point DNS to your hosting provider
- Configure SSL certificate (Let's Encrypt for free)

### 2. Environment Variables

Set these in your hosting platform:

- `FLASK_DEBUG=False`
- `SECRET_KEY=your-secret-key-here`

### 3. Monitoring and Logs

- Set up application monitoring
- Configure log rotation
- Set up alerts for downtime

### 4. Backup Strategy

- Regular database backups (if applicable)
- Code repository backups
- Configuration backups

## Troubleshooting

### Common Issues:

1. **OpenCV/MediaPipe installation errors**: Ensure system dependencies are installed
2. **Port conflicts**: Check if port 5000 is available
3. **Memory issues**: Increase server RAM for video processing
4. **Webcam access**: Ensure proper permissions on server

### Performance Optimization:

1. Use a CDN for static files
2. Implement caching strategies
3. Optimize image processing algorithms
4. Use background workers for heavy processing

## Security Considerations

1. **HTTPS**: Always use SSL/TLS encryption
2. **Input validation**: Validate all user inputs
3. **Rate limiting**: Prevent abuse
4. **File upload security**: Validate uploaded files
5. **Environment variables**: Never commit secrets to code

## Cost Estimation

- **Heroku**: $7-25/month (depending on dyno size)
- **Railway**: $5-20/month
- **DigitalOcean**: $5-12/month
- **VPS**: $5-20/month
- **Domain**: $10-15/year

## Next Steps

1. Choose your preferred hosting option
2. Follow the specific deployment steps
3. Test thoroughly before going live
4. Set up monitoring and backups
5. Share your application URL with users!

## Support

If you encounter issues during deployment:

1. Check the hosting platform's documentation
2. Review application logs
3. Test locally first
4. Consider using a simpler deployment option initially

Good luck with your deployment! 🚀
