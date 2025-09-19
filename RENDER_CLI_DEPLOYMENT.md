# Render CLI Deployment Guide

Since we're in a containerized environment where the Render CLI can't be installed directly, here are the steps to deploy using the Render CLI from your local machine.

## Prerequisites

- Local machine with internet access
- Git repository cloned locally
- Render.com account

## Method 1: Using the Deployment Script

### 1. Copy the Script to Your Local Machine

The `deploy-with-render-cli.sh` script has been created in the repository. Copy it to your local machine:

```bash
# If you have the repo cloned locally:
git pull origin render-deployment
chmod +x deploy-with-render-cli.sh
./deploy-with-render-cli.sh
```

### 2. Follow the Interactive Prompts

The script will:
- Install Render CLI if not present
- Authenticate with Render
- Validate the blueprint
- Deploy the services

## Method 2: Manual CLI Deployment

### 1. Install Render CLI Locally

#### On macOS/Linux:
```bash
curl -fsSL https://cli.render.com/install | sh
```

#### On Windows:
```powershell
# Using Chocolatey
choco install render-cli

# Or download from GitHub releases
```

### 2. Authenticate
```bash
render auth login
```

### 3. Validate Blueprint
```bash
render blueprint validate --file render.yaml
```

### 4. Deploy Blueprint
```bash
render blueprint deploy --file render.yaml --name "temporal-orchestration-platform"
```

## Method 3: Using Docker (Alternative)

If you prefer to use Docker to run the Render CLI:

```bash
# Create a Dockerfile for Render CLI
cat > Dockerfile.render-cli << 'EOF'
FROM alpine:latest
RUN apk add --no-cache curl bash
RUN curl -fsSL https://cli.render.com/install | sh
WORKDIR /workspace
COPY render.yaml .
CMD ["render", "blueprint", "deploy", "--file", "render.yaml", "--name", "temporal-orchestration-platform"]
EOF

# Build and run
docker build -f Dockerfile.render-cli -t render-cli .
docker run -it --rm -v ~/.render:/root/.render render-cli
```

## Verification Steps

### 1. Check Deployment Status
```bash
render services list
```

### 2. Monitor Logs
```bash
render logs <service-name>
```

### 3. Access Temporal UI
- Find the `temporal-ui` service in your Render dashboard
- Open the public URL
- Verify you can see the `default` namespace

### 4. Test Workflow Execution
```bash
# Connect to your worker service and run:
python -m app.cli https://example.com/test1.pdf https://example.com/test2.pdf
```

## Troubleshooting

### Common Issues

#### Authentication Errors
```bash
# Re-authenticate
render auth logout
render auth login
```

#### Blueprint Validation Failures
```bash
# Check YAML syntax
render blueprint validate --file render.yaml --verbose
```

#### Service Creation Failures
```bash
# Check service logs
render logs <service-name>
```

### Getting Help

```bash
# Render CLI help
render --help
render blueprint --help
render services --help
```

## Alternative: Web Dashboard Deployment

If CLI deployment doesn't work, you can still use the Render web dashboard:

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **New → Blueprint**: Create a new blueprint
3. **Connect Repository**: Link your GitHub repository
4. **Select Blueprint**: Choose `render.yaml`
5. **Deploy**: Click deploy and monitor progress

## Post-Deployment

### 1. Set Up Monitoring
- Monitor service health in Render dashboard
- Set up alerts for service failures
- Track resource usage

### 2. Configure Custom Domain (Optional)
- Add custom domain to temporal-ui service
- Set up SSL certificates
- Configure DNS records

### 3. Scale Services
- Increase worker instances for higher throughput
- Upgrade service plans for better performance
- Monitor and adjust based on usage

## Cost Management

### Development Environment
- Use Starter plans for non-critical services
- Single Elasticsearch node
- Minimal resource allocation

### Production Environment
- Use Standard plans for core services
- Consider multi-node Elasticsearch
- Adequate resource allocation for growth

## Security Considerations

### 1. Environment Variables
- Use Render's secret management for sensitive data
- Rotate passwords regularly
- Limit access to production services

### 2. Network Security
- Use private services where possible
- Configure firewall rules
- Enable TLS for production

### 3. Access Control
- Use Render's team management features
- Implement proper RBAC
- Monitor access logs

## Next Steps

1. **Deploy the application** using one of the methods above
2. **Test the workflows** to ensure everything works
3. **Set up monitoring** and alerting
4. **Configure CI/CD** for automated deployments
5. **Scale as needed** based on usage patterns

The fixed `render.yaml` should now deploy successfully without the "cannot unmarshal !!seq into string" error!
