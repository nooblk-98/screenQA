import os
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import requests
from urllib.parse import urlparse
import threading
from typing import Dict, List, Tuple, Optional


class ScreenshotCapture:
    def __init__(self):
        self.devices = self.load_devices()
        self.screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'screenshots')
        self.ensure_directories()
        
    def load_devices(self) -> Dict:
        """Load device configurations from JSON file"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'devices.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Device config file not found at {config_path}")
            return {}
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)
    
    def create_webdriver(self, device_config: Dict) -> webdriver.Chrome:
        """Create a Chrome WebDriver instance with specific device configuration"""
        chrome_options = Options()
        
        # Add common options for better screenshot quality
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size={},{}'.format(device_config['width'], device_config['height']))
        chrome_options.add_argument('--force-device-scale-factor=1')
        chrome_options.add_argument('--high-dpi-support=1')
        
        # Set user agent
        chrome_options.add_argument(f'--user-agent={device_config["user_agent"]}')
        
        # Mobile emulation for mobile devices
        if 'mobile' in device_config.get('platform', '').lower() or 'phone' in device_config.get('platform', '').lower():
            mobile_emulation = {
                "deviceMetrics": {
                    "width": device_config['width'],
                    "height": device_config['height'],
                    "pixelRatio": 2.0
                },
                "userAgent": device_config['user_agent']
            }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # Create service
        service = Service(ChromeDriverManager().install())
        
        # Create and return driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_window_size(device_config['width'], device_config['height'])
        
        return driver
    
    def capture_screenshot(self, url: str, device_name: str, 
                         progress_callback: Optional[callable] = None) -> Tuple[bool, str, str]:
        """
        Capture screenshot for a specific URL and device
        Returns: (success, screenshot_path, error_message)
        """
        if device_name not in self.devices['devices']:
            return False, "", f"Device '{device_name}' not found in configuration"
        
        device_config = self.devices['devices'][device_name]
        driver = None
        
        try:
            if progress_callback:
                progress_callback(f"Initializing browser for {device_name}...")
            
            # Create webdriver
            driver = self.create_webdriver(device_config)
            
            if progress_callback:
                progress_callback(f"Loading {url}...")
            
            # Navigate to URL
            driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Scroll to capture full page
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            if progress_callback:
                progress_callback(f"Capturing screenshot for {device_name}...")
            
            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = urlparse(url).netloc or "unknown_site"
            safe_device_name = device_name.replace(" ", "_").replace("\"", "")
            filename = f"{domain}_{safe_device_name}_{timestamp}.png"
            screenshot_path = os.path.join(self.screenshots_dir, filename)
            
            # Take screenshot
            driver.save_screenshot(screenshot_path)
            
            # Optionally capture full page height
            full_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
            
            if full_height > device_config['height']:
                # Capture full page
                driver.set_window_size(device_config['width'], full_height)
                time.sleep(1)
                driver.save_screenshot(screenshot_path)
            
            if progress_callback:
                progress_callback(f"Screenshot saved: {filename}")
            
            return True, screenshot_path, ""
            
        except Exception as e:
            error_msg = f"Error capturing screenshot for {device_name}: {str(e)}"
            if progress_callback:
                progress_callback(error_msg)
            return False, "", error_msg
            
        finally:
            if driver:
                driver.quit()
    
    def capture_multiple_devices(self, url: str, selected_devices: List[str], 
                               progress_callback: Optional[callable] = None) -> Dict:
        """
        Capture screenshots for multiple devices
        Returns: Dictionary with results for each device
        """
        results = {}
        total_devices = len(selected_devices)
        
        for i, device_name in enumerate(selected_devices, 1):
            if progress_callback:
                progress_callback(f"Processing device {i}/{total_devices}: {device_name}")
            
            success, path, error = self.capture_screenshot(url, device_name, progress_callback)
            results[device_name] = {
                'success': success,
                'screenshot_path': path,
                'error': error,
                'device_info': self.devices['devices'].get(device_name, {})
            }
            
            # Small delay between captures
            time.sleep(1)
        
        return results
    
    def capture_all_devices(self, url: str, progress_callback: Optional[callable] = None) -> Dict:
        """Capture screenshots for all available devices"""
        all_devices = list(self.devices['devices'].keys())
        return self.capture_multiple_devices(url, all_devices, progress_callback)
    
    def get_available_devices(self) -> Dict:
        """Get list of available devices grouped by platform"""
        devices_by_platform = {}
        
        for device_name, device_info in self.devices['devices'].items():
            platform = device_info.get('platform', 'Other')
            if platform not in devices_by_platform:
                devices_by_platform[platform] = []
            
            devices_by_platform[platform].append({
                'name': device_name,
                'description': device_info.get('description', ''),
                'resolution': f"{device_info['width']}x{device_info['height']}"
            })
        
        return devices_by_platform
    
    def validate_url(self, url: str) -> Tuple[bool, str]:
        """Validate if URL is accessible"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code < 400:
                return True, url
            else:
                return False, f"URL returned status code: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"URL validation failed: {str(e)}"
    
    def get_screenshot_history(self) -> List[Dict]:
        """Get list of previously captured screenshots"""
        screenshots = []
        
        if not os.path.exists(self.screenshots_dir):
            return screenshots
        
        for filename in os.listdir(self.screenshots_dir):
            if filename.endswith('.png'):
                filepath = os.path.join(self.screenshots_dir, filename)
                stats = os.stat(filepath)
                
                # Parse filename to extract info
                parts = filename.replace('.png', '').split('_')
                if len(parts) >= 3:
                    domain = parts[0]
                    device = '_'.join(parts[1:-1])  # Device name might contain underscores
                    timestamp = parts[-1]
                    
                    screenshots.append({
                        'filename': filename,
                        'filepath': filepath,
                        'domain': domain,
                        'device': device,
                        'timestamp': timestamp,
                        'size': stats.st_size,
                        'created': datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        # Sort by creation time (newest first)
        screenshots.sort(key=lambda x: x['created'], reverse=True)
        return screenshots


# Threading wrapper for async screenshot capture
class AsyncScreenshotCapture:
    def __init__(self):
        self.capture = ScreenshotCapture()
        self.current_thread = None
        self.is_running = False
    
    def capture_async(self, url: str, selected_devices: List[str], 
                     progress_callback: Optional[callable] = None,
                     complete_callback: Optional[callable] = None):
        """Capture screenshots asynchronously"""
        if self.is_running:
            return False, "Another capture is already in progress"
        
        def capture_thread():
            self.is_running = True
            try:
                results = self.capture.capture_multiple_devices(url, selected_devices, progress_callback)
                if complete_callback:
                    complete_callback(results)
            except Exception as e:
                if progress_callback:
                    progress_callback(f"Error: {str(e)}")
            finally:
                self.is_running = False
        
        self.current_thread = threading.Thread(target=capture_thread)
        self.current_thread.daemon = True
        self.current_thread.start()
        return True, "Capture started"
    
    def stop_capture(self):
        """Stop current capture operation"""
        if self.current_thread and self.current_thread.is_alive():
            # Note: This is a graceful approach, actual interruption is complex with selenium
            self.is_running = False
            return True
        return False


if __name__ == "__main__":
    # Test the capture functionality
    capture = ScreenshotCapture()
    
    # Test URL validation
    valid, url_or_error = capture.validate_url("example.com")
    if valid:
        print(f"Testing with URL: {url_or_error}")
        
        # Test single device capture
        success, path, error = capture.capture_screenshot(url_or_error, "Desktop Windows")
        if success:
            print(f"Screenshot saved to: {path}")
        else:
            print(f"Error: {error}")
    else:
        print(f"URL validation failed: {url_or_error}")