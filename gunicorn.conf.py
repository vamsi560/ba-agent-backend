# Azure App Service Configuration
# Gunicorn configuration for production deployment

bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
capture_output = True
enable_stdio_inheritance = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "ba-agent-backend"

# Worker timeout
timeout = 120
graceful_timeout = 30

# Memory management
max_requests = 1000
max_requests_jitter = 50

# Security
limit_request_line = 0
limit_request_fields = 100
limit_request_field_size = 8190