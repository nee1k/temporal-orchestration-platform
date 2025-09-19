#!/bin/bash

# Render CLI Deployment Script for Temporal Orchestration Platform
# This script helps deploy using the Render CLI from your local machine

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Temporal Orchestration Platform - Render CLI Deployment${NC}"
echo "=============================================================="

# Check if render CLI is installed
if ! command -v render &> /dev/null; then
    echo -e "${YELLOW}⚠️  Render CLI not found. Installing...${NC}"
    
    # Detect OS
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)
    
    case $ARCH in
        x86_64)
            ARCH="amd64"
            ;;
        arm64|aarch64)
            ARCH="arm64"
            ;;
        *)
            echo -e "${RED}❌ Unsupported architecture: $ARCH${NC}"
            exit 1
            ;;
    esac
    
    # Download and install Render CLI
    case $OS in
        linux)
            echo -e "${BLUE}📥 Downloading Render CLI for Linux...${NC}"
            curl -fsSL https://cli.render.com/install | sh
            ;;
        darwin)
            echo -e "${BLUE}📥 Downloading Render CLI for macOS...${NC}"
            curl -fsSL https://cli.render.com/install | sh
            ;;
        *)
            echo -e "${RED}❌ Unsupported OS: $OS${NC}"
            echo -e "${YELLOW}Please install Render CLI manually: https://render.com/docs/cli${NC}"
            exit 1
            ;;
    esac
    
    # Add to PATH if needed
    if [[ ! -f ~/.local/bin/render ]]; then
        echo -e "${YELLOW}⚠️  Please add ~/.local/bin to your PATH or restart your terminal${NC}"
    fi
fi

# Check if user is logged in
echo -e "${BLUE}🔐 Checking authentication...${NC}"
if ! render auth whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  Please log in to Render CLI:${NC}"
    render auth login
fi

# Get current user info
USER_INFO=$(render auth whoami)
echo -e "${GREEN}✅ Logged in as: $USER_INFO${NC}"

# Check if blueprint file exists
BLUEPRINT_FILE="render.yaml"
if [[ ! -f "$BLUEPRINT_FILE" ]]; then
    echo -e "${RED}❌ Blueprint file $BLUEPRINT_FILE not found${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Deployment Options:${NC}"
echo "1. Deploy using Blueprint (Recommended)"
echo "2. Validate Blueprint only"
echo "3. Show current services"
echo "4. Update existing deployment"

read -p "Select option (1-4): " choice

case $choice in
    1)
        echo -e "${BLUE}🔧 Deploying using Blueprint...${NC}"
        
        # Validate blueprint first
        echo -e "${YELLOW}🔍 Validating blueprint...${NC}"
        if render blueprint validate --file "$BLUEPRINT_FILE"; then
            echo -e "${GREEN}✅ Blueprint validation passed${NC}"
        else
            echo -e "${RED}❌ Blueprint validation failed${NC}"
            exit 1
        fi
        
        # Deploy using blueprint
        echo -e "${YELLOW}📤 Deploying blueprint to Render...${NC}"
        render blueprint deploy --file "$BLUEPRINT_FILE" --name "temporal-orchestration-platform"
        
        echo -e "${GREEN}✅ Blueprint deployment initiated${NC}"
        echo -e "${BLUE}📊 Monitor deployment at: https://dashboard.render.com${NC}"
        ;;
        
    2)
        echo -e "${BLUE}🔍 Validating Blueprint...${NC}"
        if render blueprint validate --file "$BLUEPRINT_FILE"; then
            echo -e "${GREEN}✅ Blueprint validation passed${NC}"
            echo -e "${BLUE}📋 Blueprint is ready for deployment${NC}"
        else
            echo -e "${RED}❌ Blueprint validation failed${NC}"
            echo -e "${YELLOW}Please fix the issues above before deploying${NC}"
        fi
        ;;
        
    3)
        echo -e "${BLUE}📊 Current Services:${NC}"
        echo "=================="
        render services list
        ;;
        
    4)
        echo -e "${BLUE}🔄 Updating existing deployment...${NC}"
        
        # Get list of services
        echo -e "${YELLOW}📋 Current services:${NC}"
        render services list
        
        read -p "Enter service name to update: " service_name
        
        if [[ -n "$service_name" ]]; then
            echo -e "${YELLOW}🔄 Updating service: $service_name${NC}"
            render services update "$service_name" --file "$BLUEPRINT_FILE"
            echo -e "${GREEN}✅ Service updated${NC}"
        fi
        ;;
        
    *)
        echo -e "${RED}❌ Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Operation completed!${NC}"
echo ""
echo -e "${BLUE}📚 Next Steps:${NC}"
echo "1. Monitor deployment in Render dashboard"
echo "2. Check Temporal UI for workflow execution"
echo "3. Test with: python -m app.cli <url1> <url2>"
echo "4. Review logs for any issues"
echo ""
echo -e "${BLUE}📖 Documentation:${NC}"
echo "- Architecture Overview: ARCHITECTURE_OVERVIEW.md"
echo "- Quick Reference: RENDER_QUICK_REFERENCE.md"
echo "- Workflow Docs: docs/WORKFLOWS.md"
