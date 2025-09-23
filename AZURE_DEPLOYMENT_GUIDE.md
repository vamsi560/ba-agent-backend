# Azure Web App Backend Deployment Guide

## Overview
This folder contains all necessary files for deploying the BA Agent Backend to Azure Web App service. The deployment includes the complete Flask application with all dependencies and Azure-specific configurations.

## Prerequisites
1. **Azure Subscription** with sufficient credits
2. **Azure CLI** installed locally
3. **Git** for deployment (recommended method)
4. **PostgreSQL Database** (already configured: baagent.postgres.database.azure.com)

## Deployment Files Structure
```
backend-azure-deployment/
├── main.py                    # Main Flask application with health endpoints
├── startup.py                 # Azure-specific startup script
├── requirements.txt           # Python dependencies with production packages
├── runtime.txt               # Python version specification
├── web.config                # Azure Web App configuration
├── gunicorn.conf.py          # Production WSGI server configuration
├── azure-env-template.txt    # Environment variables template
├── config.py                 # Application configuration
├── database.py               # Database models and connections
├── auth_system.py            # Authentication system
├── integration_services.py   # External integrations
├── enhanced_document_generator.py  # Document generation
└── [all other supporting files]
```

## Step-by-Step Deployment

### 1. Create Azure Web App
```bash
# Login to Azure
az login

# Create resource group (if not exists)
az group create --name ba-agent-rg --location "East US"

# Create App Service plan
az appservice plan create --name ba-agent-plan --resource-group ba-agent-rg --sku B1 --is-linux

# Create Web App
az webapp create --resource-group ba-agent-rg --plan ba-agent-plan --name ba-agent-backend-prod --runtime "PYTHON|3.11"
```

### 2. Configure Environment Variables
Set the following application settings in Azure Portal or via CLI:

```bash
# Set environment variables
az webapp config appsettings set --resource-group ba-agent-rg --name ba-agent-backend-prod --settings \
    FLASK_ENV=production \
    FLASK_DEBUG=False \
    DATABASE_URL="postgresql+psycopg2://bauser:Valuemomentum123@baagent.postgres.database.azure.com:5432/ba_agent" \
    GEMINI_API_KEY="AIzaSyA5_KnR58T2MTG4oOvBeAqbd8idJCdOlRA" \
    GEMINI_API_URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
    ACS_CONNECTION_STRING="endpoint=https://baagentacs123.india.communication.azure.com/;accesskey=3NFm6rs3wKyuP2B5BljzjkjGlWUC7SXWIilVOiHlF0jlpJQ8PiQ6JQQJ99BIACULyCpAhliiAAAAAZCSEmoo" \
    ACS_SENDER_ADDRESS="DoNotReply@0a996688-51d4-48e5-a65c-ad35a83a9c77.azurecomm.net" \
    BACKEND_BASE_URL="https://ba-agent-backend-prod.azurewebsites.net"
```

### 3. Deploy via Git (Recommended)
```bash
# Initialize git repository in deployment folder
cd backend-azure-deployment
git init
git add .
git commit -m "Initial backend deployment"

# Get deployment credentials
az webapp deployment list-publishing-credentials --name ba-agent-backend-prod --resource-group ba-agent-rg

# Add Azure remote
git remote add azure https://$ba-agent-backend-prod@ba-agent-backend-prod.scm.azurewebsites.net/ba-agent-backend-prod.git

# Deploy to Azure
git push azure main
```

### 4. Alternative: ZIP Deployment
```bash
# Create ZIP file of all deployment files
zip -r backend-deployment.zip .

# Deploy ZIP file
az webapp deployment source config-zip --resource-group ba-agent-rg --name ba-agent-backend-prod --src backend-deployment.zip
```

### 5. Configure Startup Command
Set the startup command in Azure Portal:
- Go to Azure Portal > App Services > ba-agent-backend-prod
- Navigate to Configuration > General Settings
- Set Startup Command: `python main.py`

### 6. Configure CORS (if needed)
```bash
# Allow CORS for frontend domain
az webapp cors add --resource-group ba-agent-rg --name ba-agent-backend-prod --allowed-origins https://your-frontend-domain.azurestaticapps.net
```

## Health Check Endpoints
The deployment includes health check endpoints:
- **Root Health Check**: `https://ba-agent-backend-prod.azurewebsites.net/`
- **API Health Check**: `https://ba-agent-backend-prod.azurewebsites.net/api/health`
- **Test Endpoint**: `https://ba-agent-backend-prod.azurewebsites.net/api/test`

## Environment Variables Configuration
Copy `azure-env-template.txt` and configure all required environment variables in Azure Portal:

1. Go to Azure Portal > App Services > ba-agent-backend-prod
2. Navigate to Configuration > Application settings
3. Add each environment variable from the template
4. Update URLs to match your Azure Web App name

## Database Configuration
The deployment uses the existing Azure PostgreSQL database:
- **Host**: baagent.postgres.database.azure.com
- **Database**: ba_agent
- **User**: bauser
- **Connection**: Already configured in DATABASE_URL

## Monitoring and Logs
1. **Application Insights**: Automatically enabled for monitoring
2. **Log Stream**: Available in Azure Portal > App Services > Log stream
3. **Metrics**: Performance metrics available in Azure Portal

## Testing Deployment
After deployment, test the following endpoints:
```bash
# Health check
curl https://ba-agent-backend-prod.azurewebsites.net/

# API health check
curl https://ba-agent-backend-prod.azurewebsites.net/api/health

# Test endpoint
curl https://ba-agent-backend-prod.azurewebsites.net/api/test
```

## Scaling and Performance
- **App Service Plan**: Currently set to B1 (Basic)
- **Scaling**: Can be upgraded to Standard/Premium for auto-scaling
- **Performance**: Gunicorn configured with 4 workers for production

## Security Considerations
1. **HTTPS**: Automatically enabled on azurewebsites.net
2. **Environment Variables**: Stored securely in Azure App Settings
3. **Database**: Uses SSL connection to Azure PostgreSQL
4. **CORS**: Configure appropriately for frontend domains

## Troubleshooting
1. **Deployment Logs**: Check in Azure Portal > Deployment Center
2. **Application Logs**: Available in Log stream
3. **Dependencies**: Ensure all requirements are in requirements.txt
4. **Environment Variables**: Verify all required settings are configured

## Cost Optimization
- **Basic Plan (B1)**: ~$13/month for development
- **Standard Plan (S1)**: ~$56/month for production with auto-scaling
- **Database**: Shared Azure PostgreSQL instance already configured

## Support and Maintenance
- **Logs**: Monitor via Azure Portal
- **Updates**: Deploy via Git push or ZIP deployment
- **Backup**: Azure provides automatic backups
- **SSL**: Managed automatically by Azure

## Connection Details for Frontend
Update your frontend configuration to point to:
```
BACKEND_URL=https://ba-agent-backend-prod.azurewebsites.net
API_BASE_URL=https://ba-agent-backend-prod.azurewebsites.net/api
```

## Next Steps After Deployment
1. Update frontend configuration with new backend URL
2. Test all API endpoints
3. Configure monitoring and alerts
4. Set up CI/CD pipeline for automated deployments
5. Configure custom domain (optional)