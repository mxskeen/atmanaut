#!/bin/bash

# Script to switch between testing mode (no Clerk) and production mode

if [ "$1" == "test" ]; then
    echo "🔧 Switching to TESTING mode (no Clerk authentication)..."
    
    # Backup original files
    [ -f middleware.js ] && cp middleware.js middleware.production.js
    [ -f app/layout.js ] && cp app/layout.js app/layout.production.js
    [ -f .env.local ] && cp .env.local .env.local.backup
    
    # Use testing files
    cp middleware.testing.js middleware.js
    cp app/layout.testing.js app/layout.js
    cp .env.local.testing .env.local
    
    echo "✅ Testing mode enabled! You can now test without Clerk authentication."
    echo "🚀 Run: npm run dev"
    
elif [ "$1" == "prod" ]; then
    echo "🔄 Switching to PRODUCTION mode (with Clerk authentication)..."
    
    # Restore original files
    [ -f middleware.production.js ] && mv middleware.production.js middleware.js
    [ -f app/layout.production.js ] && mv app/layout.production.js app/layout.js
    [ -f .env.local.backup ] && mv .env.local.backup .env.local
    
    echo "✅ Production mode enabled!"
    echo "⚠️  Make sure your Clerk keys are configured in .env.local"
    
else
    echo "Usage: $0 [test|prod]"
    echo "  test - Enable testing mode without Clerk"
    echo "  prod - Enable production mode with Clerk"
fi
