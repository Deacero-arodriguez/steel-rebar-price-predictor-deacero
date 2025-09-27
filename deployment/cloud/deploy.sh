#!/bin/bash

# Steel Rebar Price Predictor - Deployment Script
# This script deploys the application to Google Cloud Platform

set -e

echo "🚀 Starting deployment of Steel Rebar Price Predictor..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo "❌ Not authenticated with gcloud. Please run 'gcloud auth login' first."
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No project ID set. Please run 'gcloud config set project YOUR_PROJECT_ID' first."
    exit 1
fi

echo "📋 Project ID: $PROJECT_ID"

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy using Cloud Build with new structure
echo "🏗️ Building and deploying application with new structure..."
gcloud builds submit --config deployment/cloud/cloudbuild.yaml .

# Get the service URL
SERVICE_URL=$(gcloud run services describe steel-rebar-predictor --region=us-central1 --format="value(status.url)")

echo "✅ Deployment completed successfully!"
echo "🌐 Service URL: $SERVICE_URL"
echo "🔑 API Key: deacero_steel_predictor_2025_key"
echo ""
echo "📖 Usage:"
echo "curl -H 'X-API-Key: deacero_steel_predictor_2025_key' $SERVICE_URL/predict/steel-rebar-price"
echo ""
echo "📊 Health check:"
echo "curl $SERVICE_URL/health"
