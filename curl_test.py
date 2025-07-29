import subprocess
import json

def test_with_curl():
    """Test endpoints using curl commands"""
    
    print("🧪 Testing Flask App with Curl")
    print("=" * 50)
    
    tests = [
        {
            'name': 'Health Check',
            'cmd': ['curl', '-s', 'http://localhost:8080/health']
        },
        {
            'name': 'Home Page',
            'cmd': ['curl', '-s', 'http://localhost:8080/']
        },
        {
            'name': 'Webhook Test - Hello',
            'cmd': ['curl', '-s', '-X', 'POST', 
                   'http://localhost:8080/webhook',
                   '-d', 'Body=hello&From=whatsapp:+1234567890']
        },
        {
            'name': 'Webhook Test - Menu',
            'cmd': ['curl', '-s', '-X', 'POST', 
                   'http://localhost:8080/webhook',
                   '-d', 'Body=menu&From=whatsapp:+1234567890']
        }
    ]
    
    for test in tests:
        print(f"\n🔍 {test['name']}:")
        try:
            result = subprocess.run(test['cmd'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Success: {result.stdout[:200]}...")
            else:
                print(f"❌ Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("⏱️ Timeout")
        except FileNotFoundError:
            print("❌ Curl not found - using PowerShell instead")
            # Fallback to PowerShell
            if 'GET' in str(test['cmd']) or len(test['cmd']) <= 3:
                ps_cmd = f"Invoke-WebRequest -Uri {test['cmd'][-1]} -UseBasicParsing"
            else:
                # POST request
                url = test['cmd'][4]
                data = test['cmd'][6]
                ps_cmd = f"Invoke-WebRequest -Uri {url} -Method POST -Body '{data}' -UseBasicParsing"
            
            try:
                result = subprocess.run(['powershell', '-Command', ps_cmd], 
                                      capture_output=True, text=True, timeout=10)
                if 'StatusCode' in result.stdout and ('200' in result.stdout or '201' in result.stdout):
                    print(f"✅ Success via PowerShell")
                else:
                    print(f"❌ PowerShell result: {result.stdout[:100]}...")
            except Exception as e:
                print(f"❌ PowerShell error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_with_curl()
