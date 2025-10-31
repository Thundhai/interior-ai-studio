#!/usr/bin/env python3
"""
Deployment Testing Script
Tests both Railway and Google Cloud Run deployments
"""
import requests
import json
import time

def test_deployment(base_url, platform_name):
    """Test a deployed Interior AI Studio instance"""
    print(f"\n🧪 Testing {platform_name} deployment: {base_url}")
    
    # Test basic connectivity
    try:
        response = requests.get(f"{base_url}/agents", timeout=10)
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ {platform_name}: {len(agents)} agents detected")
            return True
        else:
            print(f"❌ {platform_name}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {platform_name}: Connection failed - {e}")
        return False

def comprehensive_test(base_url, platform_name):
    """Run comprehensive tests on deployment"""
    print(f"\n🔬 Comprehensive testing for {platform_name}")
    
    endpoints_to_test = [
        ("/agents", "Agent list"),
        ("/docs", "API documentation"),
        ("/openapi.json", "OpenAPI specification")
    ]
    
    results = {}
    for endpoint, description in endpoints_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
            results[description] = status
            print(f"  {description}: {status}")
        except Exception as e:
            results[description] = f"❌ ERROR: {e}"
            print(f"  {description}: ❌ ERROR")
    
    return results

def main():
    """Test both deployments"""
    print("🚀 Interior AI Studio Deployment Tester")
    print("=" * 50)
    
    # URLs will be updated once deployments are complete
    railway_url = "https://interior-ai-studio-production.railway.app"
    gcloud_url = "https://interior-ai-studio-prod-xyz.run.app"
    
    print("📝 TESTING INSTRUCTIONS:")
    print("1. Replace URLs below with your actual deployment URLs")
    print("2. Run this script to verify both deployments")
    print("3. Use successful URLs in client presentations")
    
    print(f"\n🌊 Railway URL to test: {railway_url}")
    print(f"☁️ Google Cloud URL to test: {gcloud_url}")
    
    # Uncomment these lines once you have your actual URLs:
    # railway_success = test_deployment(railway_url, "Railway")
    # gcloud_success = test_deployment(gcloud_url, "Google Cloud")
    
    # if railway_success:
    #     comprehensive_test(railway_url, "Railway")
    
    # if gcloud_success:
    #     comprehensive_test(gcloud_url, "Google Cloud")

if __name__ == "__main__":
    main()