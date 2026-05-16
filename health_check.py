#!/usr/bin/env python3
import time
from datetime import datetime
from anthropic import Anthropic

def health_check():
    try:
        start_time = time.time()
        timestamp = datetime.now().isoformat()

        client = Anthropic()
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=10,
            messages=[
                {"role": "user", "content": "ping"}
            ]
        )

        response_time = time.time() - start_time
        status = "OK"

    except Exception as e:
        timestamp = datetime.now().isoformat()
        response_time = None
        status = "FAILED"
        print(f"[{timestamp}] Health check: FAILED ({str(e)})")
        return

    print(f"[{timestamp}] Health check: {status} (response time: {response_time:.2f}s)")

if __name__ == "__main__":
    health_check()
