# Render Deployment - Quick Reference

## 🚀 One-Click Deployment

### Option 1: Blueprint (Recommended)
```bash
# 1. Fork this repository
# 2. Go to Render Dashboard → New → Blueprint
# 3. Connect your repository
# 4. Select render.yaml
# 5. Deploy!
```

### Option 2: CLI Script
```bash
./deploy-to-render.sh
# Follow the interactive prompts
```

## 📋 Service Checklist

### Infrastructure
- [ ] PostgreSQL (private, 10GB disk)
- [ ] PgBouncer (private, connection pooling)
- [ ] Elasticsearch (private, 20GB disk)

### Temporal Services
- [ ] temporal-frontend (private)
- [ ] temporal-history (private)
- [ ] temporal-matching (private)
- [ ] temporal-worker (private)

### Application
- [ ] temporal-ui (public web service)
- [ ] admin-tools (one-time job)
- [ ] app-worker (your application)

## 🔧 Environment Variables

### ✅ Fixed YAML Structure
The `render.yaml` now includes all environment variables inline. No need to create separate groups - the YAML is self-contained and ready to deploy.

**Key Fix**: Removed `envVarGroups` references that caused "cannot unmarshal !!seq into string" errors.

### For Custom App Worker
```bash
APP_TEMPORAL_ADDRESS=<frontend-host>:7233
APP_TASK_QUEUE=doc-pipeline
```

## ✅ Verification Steps

1. **Check Services**: All services show "Live" status
2. **Access UI**: Open temporal-ui web service URL
3. **Test Workflow**: Run `python -m app.cli <url1> <url2>`
4. **Monitor**: Watch workflows in Temporal UI

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| UI can't connect | Check TEMPORAL_ADDRESS points to frontend |
| DB connection errors | Verify PgBouncer is running |
| ES unhealthy | Check disk attachment and single-node config |
| Worker not processing | Verify task queue and connection settings |

## 💰 Cost Estimates

### Development (Starter Plans)
- PostgreSQL: $7/month
- Elasticsearch: $7/month
- Temporal services: $7/month each (4 services)
- UI: $7/month
- **Total: ~$35/month**

### Production (Standard Plans)
- PostgreSQL: $25/month
- Elasticsearch: $25/month
- Temporal services: $25/month each (4 services)
- UI: $7/month
- **Total: ~$130/month**

## 🔗 Useful Links

- [Render Dashboard](https://dashboard.render.com)
- [Temporal UI](https://your-app.onrender.com) (after deployment)
- [Deployment Guide](RENDER_DEPLOYMENT_GUIDE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 📞 Support

- Render Support: [help.render.com](https://help.render.com)
- Temporal Docs: [docs.temporal.io](https://docs.temporal.io)
- Project Issues: Create GitHub issue
