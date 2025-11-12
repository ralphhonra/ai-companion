"""
Tool Executor Module
Executes system commands based on LLM responses.
"""
import subprocess
import json
from datetime import datetime
from typing import Dict, Any, Optional


class ToolExecutor:
    """Executes system automation tools on Mac."""
    
    def __init__(self):
        """Initialize tool executor."""
        self.tool_handlers = {
            "open_app": self._open_app,
            "search_files": self._search_files,
            "get_info": self._get_info,
            "control_app": self._control_app,
            "web_search": self._web_search,
            "open_url": self._open_url,
            "play_youtube": self._play_youtube,
            "browser_control": self._browser_control,
            "none": self._no_action,
        }
    
    def execute(self, llm_response: str) -> tuple[bool, str]:
        """
        Execute command from LLM response.
        
        Args:
            llm_response: JSON string from LLM
            
        Returns:
            Tuple of (success, result_message)
        """
        try:
            # Parse JSON response
            data = json.loads(llm_response)
            tool = data.get("tool", "none")
            response_text = data.get("response", "")
            
            print(f"🔧 Tool: {tool}")
            print(f"📝 Response text: {response_text}")
            print(f"📦 Data: {data}")
            
            # Execute tool
            if tool in self.tool_handlers:
                print(f"✓ Executing tool handler: {tool}")
                success, details = self.tool_handlers[tool](data)
                print(f"✓ Tool result - Success: {success}, Details: {details}")
                
                # Combine response with details if any
                if details:
                    full_response = f"{response_text}\n{details}"
                else:
                    full_response = response_text
                
                return success, full_response
            else:
                print(f"⚠️  Unknown tool: {tool}, attempting fallback...")
                # Try to guess what the user wanted based on the parameters
                return self._handle_unknown_action(data, response_text)
                
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Response was: {llm_response}")
            
            # Try to extract just the first JSON object if multiple were sent
            try:
                # Find the first complete JSON object
                lines = llm_response.strip().split('\n')
                json_str = ""
                brace_count = 0
                
                for line in lines:
                    json_str += line
                    brace_count += line.count('{') - line.count('}')
                    if brace_count == 0 and json_str.strip():
                        # Found complete JSON
                        break
                
                # Try parsing just the first JSON
                data = json.loads(json_str)
                tool = data.get("tool", "none")
                response_text = data.get("response", "")
                
                print(f"✓ Recovered first JSON object: {tool}")
                
                if tool in self.tool_handlers:
                    success, details = self.tool_handlers[tool](data)
                    return success, response_text if not details else f"{response_text}\n{details}"
                else:
                    return self._handle_unknown_action(data, response_text)
                    
            except Exception as recovery_error:
                print(f"Could not recover JSON: {recovery_error}")
                # If not JSON, treat as plain response
                return True, llm_response
        except Exception as e:
            return False, f"Error executing tool: {e}"
    
    def _no_action(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """No system action needed."""
        return True, ""
    
    def _open_app(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Open an application."""
        app_name = data.get("app_name", "")
        if not app_name:
            return False, "No application name provided."
        
        try:
            subprocess.run(["open", "-a", app_name], check=True)
            return True, ""
        except subprocess.CalledProcessError:
            return False, f"Could not open {app_name}. Is it installed?"
        except Exception as e:
            return False, f"Error: {e}"
    
    def _search_files(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Search for files using Spotlight."""
        query = data.get("query", "")
        if not query:
            return False, "No search query provided."
        
        try:
            result = subprocess.run(
                ["mdfind", query],
                capture_output=True,
                text=True,
                timeout=5,
                check=True
            )
            
            files = result.stdout.strip().split('\n')
            files = [f for f in files if f]  # Remove empty lines
            
            if not files:
                return True, "No files found matching your query."
            
            # Return first 5 results
            file_list = '\n'.join(files[:5])
            count = len(files)
            
            if count > 5:
                return True, f"Found {count} files. Here are the first 5:\n{file_list}"
            else:
                return True, f"Found {count} file(s):\n{file_list}"
                
        except subprocess.TimeoutExpired:
            return False, "Search timed out."
        except Exception as e:
            return False, f"Search error: {e}"
    
    def _get_info(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Get system information."""
        info_type = data.get("info_type", "time")
        
        try:
            if info_type == "time":
                current_time = datetime.now().strftime("%I:%M %p")
                return True, f"The current time is {current_time}."
            
            elif info_type == "date":
                current_date = datetime.now().strftime("%A, %B %d, %Y")
                return True, f"Today is {current_date}."
            
            elif info_type == "battery":
                result = subprocess.run(
                    ["pmset", "-g", "batt"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                # Parse battery percentage
                output = result.stdout
                if "%" in output:
                    # Extract percentage
                    for line in output.split('\n'):
                        if '%' in line:
                            parts = line.split('\t')
                            if len(parts) > 1:
                                battery_info = parts[1].strip()
                                return True, f"Battery: {battery_info}"
                return True, "Could not read battery status."
            
            elif info_type == "disk_space":
                result = subprocess.run(
                    ["df", "-h", "/"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 5:
                        size = parts[1]
                        used = parts[2]
                        avail = parts[3]
                        percent = parts[4]
                        return True, f"Disk: {used} used of {size} ({percent}), {avail} available."
                return True, "Could not read disk space."
            
            else:
                return False, f"Unknown info type: {info_type}"
                
        except Exception as e:
            return False, f"Error getting info: {e}"
    
    def _control_app(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Control applications via AppleScript."""
        app_name = data.get("app_name", "Music")
        action = data.get("action", "play")
        
        # Map actions to AppleScript commands
        scripts = {
            "play": f'tell application "{app_name}" to play',
            "pause": f'tell application "{app_name}" to pause',
            "playpause": f'tell application "{app_name}" to playpause',
            "next": f'tell application "{app_name}" to next track',
            "previous": f'tell application "{app_name}" to previous track',
            "volume_up": f'tell application "{app_name}" to set sound volume to (sound volume + 10)',
            "volume_down": f'tell application "{app_name}" to set sound volume to (sound volume - 10)',
        }
        
        script = scripts.get(action)
        if not script:
            return False, f"Unknown action: {action}"
        
        try:
            subprocess.run(
                ["osascript", "-e", script],
                check=True,
                capture_output=True
            )
            return True, ""
        except subprocess.CalledProcessError:
            return False, f"{app_name} is not running or doesn't support this action."
        except Exception as e:
            return False, f"Error: {e}"
    
    def _web_search(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Open browser with search query."""
        query = data.get("query", "")
        if not query:
            return False, "No search query provided."
        
        try:
            # Use Google search
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            subprocess.run(["open", search_url], check=True)
            return True, ""
        except Exception as e:
            return False, f"Error: {e}"
    
    def _open_url(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Open a specific URL."""
        url = data.get("url", "")
        if not url:
            return False, "No URL provided."
        
        try:
            subprocess.run(["open", url], check=True)
            return True, ""
        except Exception as e:
            return False, f"Error: {e}"
    
    def _play_youtube(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Play a YouTube video or music."""
        query = data.get("query", "")
        if not query:
            return False, "No search query provided."
        
        try:
            # Open YouTube search
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            subprocess.run(["open", search_url], check=True)
            return True, ""
        except Exception as e:
            return False, f"Error: {e}"
    
    def _browser_control(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Control browser via AppleScript."""
        action = data.get("action", "")
        browser = data.get("browser", "Safari")
        
        # Normalize browser name
        if "chrome" in browser.lower():
            browser = "Google Chrome"
        
        # Different scripts for different browsers
        if browser == "Safari":
            scripts = {
                "refresh": 'tell application "Safari" to do JavaScript "location.reload()" in current tab of front window',
                "back": 'tell application "Safari" to go back',
                "forward": 'tell application "Safari" to go forward',
                "new_tab": 'tell application "Safari" to make new tab at end of tabs of front window',
                "close_tab": 'tell application "Safari" to close current tab of front window',
            }
        else:  # Chrome
            scripts = {
                "refresh": 'tell application "Google Chrome" to reload active tab of front window',
                "back": 'tell application "Google Chrome" to go back active tab of front window',
                "forward": 'tell application "Google Chrome" to go forward active tab of front window',
                "new_tab": 'tell application "Google Chrome" to make new tab at end of front window',
                "close_tab": 'tell application "Google Chrome" to close active tab of front window',
            }
        
        script = scripts.get(action)
        if not script:
            return False, f"Unknown browser action: {action}"
        
        try:
            subprocess.run(
                ["osascript", "-e", script],
                check=True,
                capture_output=True,
                timeout=5
            )
            return True, ""
        except subprocess.TimeoutExpired:
            return False, f"{browser} is not responding."
        except subprocess.CalledProcessError as e:
            return False, f"{browser} is not running. Please open it first."
        except Exception as e:
            return False, f"Error: {e}"
    
    def _handle_unknown_action(self, data: Dict[str, Any], response_text: str) -> tuple[bool, str]:
        """
        Try to handle unknown actions by guessing intent.
        """
        tool = data.get("tool", "")
        
        # Map common unknown actions to real ones
        if "youtube" in tool.lower() or "play" in tool.lower() and "track" in tool.lower():
            # User wants to play YouTube
            query = data.get("query", data.get("track", "music"))
            return self._play_youtube({"query": query, "response": response_text})
        
        elif "tab" in tool.lower() and "new" in tool.lower():
            # New tab
            return self._browser_control({"action": "new_tab", "browser": "Safari", "response": response_text})
        
        elif "chrome" in tool.lower() or "browser" in tool.lower():
            # User wants to open Chrome or browser
            try:
                subprocess.run(["open", "-a", "Google Chrome"], check=True)
                return True, response_text
            except:
                # Try Safari
                subprocess.run(["open", "-a", "Safari"], check=True)
                return True, response_text
        
        elif "record" in tool.lower() or "voice" in tool.lower():
            # User wants a voice recorder app
            try:
                # Try QuickTime Player (has audio recording)
                subprocess.run(["open", "-a", "QuickTime Player"], check=True)
                return True, f"{response_text}\nOpened QuickTime Player. Go to File → New Audio Recording."
            except:
                return False, "Could not open recording app."
        
        elif "note" in tool.lower():
            # User wants Notes app
            try:
                subprocess.run(["open", "-a", "Notes"], check=True)
                return True, response_text
            except:
                return False, "Could not open Notes."
        
        else:
            # Don't know what to do
            return False, f"I'm not sure how to {tool}. Try asking me to 'open [app name]' instead."


if __name__ == "__main__":
    # Test tool executor
    executor = ToolExecutor()
    
    # Test get_info
    test_response = '{"tool": "get_info", "info_type": "time", "response": "Getting current time."}'
    success, result = executor.execute(test_response)
    print(f"Success: {success}")
    print(f"Result: {result}")

