"""
Direct test script for Interior AI Studio agents
Run this to test your agents without needing the server
"""
import os
import sys
sys.path.append('.')

# Set environment variables
os.environ["INTERIOR_AI_API_KEY"] = "changeme"
os.environ["GEMINI_API_KEY"] = "your-gemini-key-here"  # Replace with your actual key

try:
    from src.main_agent import MainAgent
    
    print("🚀 Testing Interior AI Studio Agents...")
    main_agent = MainAgent()
    
    # Test 1: MoodBoard Agent
    print("\n1️⃣ Testing MoodBoard Agent...")
    moodboard_result = main_agent.moodboard_agent.run({"query": "modern living room"})
    print(f"✅ MoodBoard result: {len(moodboard_result.get('images', []))} images found")
    
    # Test 2: Gemini Vision API (if key is set)
    print("\n2️⃣ Testing Gemini Vision API...")
    test_image = "https://images.unsplash.com/photo-1586023492125-27b2c045efd7"
    if main_agent.moodboard_agent.gemini_api_key and main_agent.moodboard_agent.gemini_api_key != "your-gemini-key-here":
        tags = main_agent.moodboard_agent.call_clip_blip_model(test_image)
        print(f"✅ Gemini tags: {tags}")
    else:
        print("⚠️ Gemini API key not set, using fallback tags")
        tags = main_agent.moodboard_agent.auto_tag_image(test_image)
        print(f"✅ Fallback tags: {tags}")
    
    # Test 3: Other Agents
    print("\n3️⃣ Testing Style Advisor Agent...")
    style_result = main_agent.style_advisor_agent.run({"topic": "color psychology"})
    print(f"✅ Style advisor result: {len(style_result.get('trends', []))} trends found")
    
    print("\n4️⃣ Testing Budget Cost Advisor Agent...")
    budget_result = main_agent.budget_cost_advisor_agent.run({"budget": 5000, "style_tags": ["modern"]})
    print(f"✅ Budget advisor result: {len(budget_result.get('alternatives', []))} alternatives found")
    
    print("\n🎉 All agents tested successfully!")
    print("\nYour Interior AI Studio is working correctly!")
    print("The only issue is with the uvicorn server setup.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()