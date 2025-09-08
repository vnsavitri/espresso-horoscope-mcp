#!/usr/bin/env python3
"""
GPT-OSS Helper for Espresso Horoscope

Provides AI-powered text enhancement for horoscope cards.
"""

import os
import sys
import requests
from typing import Optional


def enhance_text_with_gptoss(text: str) -> str:
    """
    Enhance text using local gpt-oss:20b model.
    
    Args:
        text: Original text to enhance
        
    Returns:
        Enhanced text or original text on failure
    """
    base_url = os.getenv("OPENAI_BASE_URL")
    if not base_url:
        print("Warning: OPENAI_BASE_URL not set, skipping gpt-oss enhancement", file=sys.stderr)
        return text
    
    try:
        # Prepare the system prompt for playful horoscope tone
        system_prompt = "Rewrite for playful horoscope tone. Keep all numbers and units unchanged."
        
        response = requests.post(
            f"{base_url}/chat/completions",
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                "temperature": 0.4,
                "max_tokens": 2000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Check for error in response
            if "error" in result:
                print(f"Warning: gpt-oss API error: {result['error']}, using original text", file=sys.stderr)
                return text
            
            # Check if choices exists and has content
            if "choices" not in result or not result["choices"]:
                print("Warning: No choices in gpt-oss response, using original text", file=sys.stderr)
                return text
            
            choice = result["choices"][0]
            message = choice["message"]
            
            # Handle different response formats
            if "content" in message and message["content"]:
                enhanced_text = message["content"].strip()
            elif "reasoning" in message and message["reasoning"]:
                # Use reasoning if content is empty (some models return reasoning instead)
                enhanced_text = message["reasoning"].strip()
            else:
                print("Warning: Empty response from gpt-oss, using original text", file=sys.stderr)
                return text
            
            print("✅ Text enhanced with gpt-oss", file=sys.stderr)
            return enhanced_text
        else:
            print(f"Warning: gpt-oss API error {response.status_code}: {response.text}", file=sys.stderr)
            return text
            
    except requests.exceptions.Timeout:
        print("Warning: gpt-oss request timed out, using original text", file=sys.stderr)
        return text
    except requests.exceptions.ConnectionError:
        print("Warning: Could not connect to gpt-oss, using original text", file=sys.stderr)
        return text
    except Exception as e:
        print(f"Warning: Error calling gpt-oss: {e}, using original text", file=sys.stderr)
        return text


def main():
    """CLI interface for testing the helper."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python cli/gptoss_helper.py <text>", file=sys.stderr)
        sys.exit(1)
    
    text = sys.argv[1]
    enhanced = enhance_text_with_gptoss(text)
    print(enhanced)


if __name__ == "__main__":
    main()
