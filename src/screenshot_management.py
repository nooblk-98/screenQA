import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black, red, green


class ScreenshotManager:
    """Manages screenshot files, organization, and analysis"""
    
    def __init__(self, screenshots_dir: str):
        self.screenshots_dir = screenshots_dir
        self.reports_dir = os.path.join(os.path.dirname(screenshots_dir), 'reports')
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories"""
        for directory in [self.screenshots_dir, self.reports_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def organize_by_date(self) -> Dict[str, List[str]]:
        """Organize screenshots by date"""
        organized = {}
        
        for filename in os.listdir(self.screenshots_dir):
            if filename.endswith('.png'):
                filepath = os.path.join(self.screenshots_dir, filename)
                timestamp = os.path.getctime(filepath)
                date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                
                if date_str not in organized:
                    organized[date_str] = []
                organized[date_str].append(filename)
        
        return organized
    
    def organize_by_domain(self) -> Dict[str, List[str]]:
        """Organize screenshots by domain"""
        organized = {}
        
        for filename in os.listdir(self.screenshots_dir):
            if filename.endswith('.png'):
                # Parse domain from filename
                parts = filename.split('_')
                if len(parts) >= 1:
                    domain = parts[0]
                    if domain not in organized:
                        organized[domain] = []
                    organized[domain].append(filename)
        
        return organized
    
    def organize_by_device(self) -> Dict[str, List[str]]:
        """Organize screenshots by device"""
        organized = {}
        
        for filename in os.listdir(self.screenshots_dir):
            if filename.endswith('.png'):
                # Parse device from filename
                parts = filename.replace('.png', '').split('_')
                if len(parts) >= 3:
                    device = '_'.join(parts[1:-1])  # Device name might contain underscores
                    if device not in organized:
                        organized[device] = []
                    organized[device].append(filename)
        
        return organized
    
    def get_screenshot_stats(self) -> Dict:
        """Get statistics about screenshots"""
        screenshots = []
        total_size = 0
        
        for filename in os.listdir(self.screenshots_dir):
            if filename.endswith('.png'):
                filepath = os.path.join(self.screenshots_dir, filename)
                stats = os.stat(filepath)
                screenshots.append({
                    'filename': filename,
                    'size': stats.st_size,
                    'created': stats.st_ctime
                })
                total_size += stats.st_size
        
        if not screenshots:
            return {
                'count': 0,
                'total_size': 0,
                'average_size': 0,
                'oldest': None,
                'newest': None
            }
        
        screenshots.sort(key=lambda x: x['created'])
        
        return {
            'count': len(screenshots),
            'total_size': total_size,
            'average_size': total_size / len(screenshots),
            'oldest': datetime.fromtimestamp(screenshots[0]['created']),
            'newest': datetime.fromtimestamp(screenshots[-1]['created'])
        }
    
    def cleanup_old_screenshots(self, days: int = 30) -> int:
        """Remove screenshots older than specified days"""
        removed_count = 0
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        for filename in os.listdir(self.screenshots_dir):
            if filename.endswith('.png'):
                filepath = os.path.join(self.screenshots_dir, filename)
                if os.path.getctime(filepath) < cutoff_time:
                    os.remove(filepath)
                    removed_count += 1
        
        return removed_count
    
    def create_comparison_image(self, screenshot_paths: List[str], 
                              output_path: str, labels: List[str] = None) -> bool:
        """Create side-by-side comparison of screenshots"""
        try:
            if not screenshot_paths or len(screenshot_paths) < 2:
                return False
            
            # Load images
            images = []
            for path in screenshot_paths:
                if os.path.exists(path):
                    img = Image.open(path)
                    images.append(img)
                else:
                    return False
            
            if not images:
                return False
            
            # Calculate dimensions for comparison
            max_height = max(img.height for img in images)
            total_width = sum(img.width for img in images)
            
            # Create comparison image
            comparison = Image.new('RGB', (total_width, max_height + 50), 'white')
            
            x_offset = 0
            for i, img in enumerate(images):
                comparison.paste(img, (x_offset, 0))
                
                # Add label if provided
                if labels and i < len(labels):
                    draw = ImageDraw.Draw(comparison)
                    label_text = labels[i]
                    
                    # Try to use a nice font, fall back to default
                    try:
                        font = ImageFont.truetype("arial.ttf", 16)
                    except:
                        font = ImageFont.load_default()
                    
                    text_bbox = draw.textbbox((0, 0), label_text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    
                    # Center text under image
                    text_x = x_offset + (img.width - text_width) // 2
                    text_y = max_height + 10
                    
                    draw.text((text_x, text_y), label_text, fill='black', font=font)
                
                x_offset += img.width
            
            comparison.save(output_path)
            return True
            
        except Exception as e:
            print(f"Error creating comparison: {e}")
            return False
    
    def analyze_layout_differences(self, screenshot_paths: List[str]) -> Dict:
        """Analyze layout differences between screenshots"""
        analysis = {
            'dimensions': [],
            'file_sizes': [],
            'color_profiles': []
        }
        
        for path in screenshot_paths:
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    
                    # Dimensions
                    analysis['dimensions'].append({
                        'width': img.width,
                        'height': img.height,
                        'aspect_ratio': img.width / img.height
                    })
                    
                    # File size
                    analysis['file_sizes'].append(os.path.getsize(path))
                    
                    # Basic color analysis
                    if img.mode == 'RGB':
                        colors = img.getcolors(maxcolors=1000000)
                        if colors:
                            dominant_colors = sorted(colors, reverse=True)[:5]
                            analysis['color_profiles'].append({
                                'dominant_colors': [(count, color) for count, color in dominant_colors],
                                'unique_colors': len(colors)
                            })
                    
                except Exception as e:
                    print(f"Error analyzing {path}: {e}")
        
        return analysis


class QAReportGenerator:
    """Generates comprehensive QA reports"""
    
    def __init__(self, screenshots_dir: str, reports_dir: str):
        self.screenshots_dir = screenshots_dir
        self.reports_dir = reports_dir
        self.manager = ScreenshotManager(screenshots_dir)
    
    def generate_html_report(self, results: Dict, url: str, 
                           output_path: str = None) -> str:
        """Generate comprehensive HTML report"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.reports_dir, f'qa_report_{timestamp}.html')
        
        # Calculate stats
        total_devices = len(results)
        successful = sum(1 for r in results.values() if r['success'])
        failed = total_devices - successful
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ScreenQA Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: 300;
                }}
                .stats {{
                    display: flex;
                    justify-content: space-around;
                    padding: 20px;
                    background: #f8f9fa;
                    border-bottom: 1px solid #dee2e6;
                }}
                .stat {{
                    text-align: center;
                }}
                .stat-number {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #495057;
                }}
                .stat-label {{
                    color: #6c757d;
                    font-size: 0.9em;
                }}
                .success {{ color: #28a745; }}
                .error {{ color: #dc3545; }}
                .content {{
                    padding: 30px;
                }}
                .device-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }}
                .device-card {{
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .device-header {{
                    padding: 15px;
                    background: #f8f9fa;
                    border-bottom: 1px solid #dee2e6;
                }}
                .device-name {{
                    font-weight: bold;
                    font-size: 1.1em;
                }}
                .device-info {{
                    color: #6c757d;
                    font-size: 0.9em;
                    margin-top: 5px;
                }}
                .screenshot-container {{
                    text-align: center;
                    padding: 15px;
                }}
                .screenshot {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 4px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                }}
                .error-message {{
                    color: #dc3545;
                    padding: 15px;
                    background: #f8d7da;
                    border-radius: 4px;
                    margin: 10px;
                }}
                .metadata {{
                    background: #f8f9fa;
                    padding: 15px;
                    font-size: 0.9em;
                    color: #6c757d;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    background: #f8f9fa;
                    color: #6c757d;
                    border-top: 1px solid #dee2e6;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>ScreenQA Testing Report</h1>
                    <p>Cross-Device Website Screenshot Analysis</p>
                </div>
                
                <div class="stats">
                    <div class="stat">
                        <div class="stat-number">{total_devices}</div>
                        <div class="stat-label">Total Devices</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number success">{successful}</div>
                        <div class="stat-label">Successful</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number error">{failed}</div>
                        <div class="stat-label">Failed</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{(successful/total_devices*100):.1f}%</div>
                        <div class="stat-label">Success Rate</div>
                    </div>
                </div>
                
                <div class="content">
                    <div class="metadata">
                        <strong>URL:</strong> {url}<br>
                        <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                        <strong>Report ID:</strong> {timestamp}
                    </div>
                    
                    <div class="device-grid">
        """
        
        # Add device cards
        for device_name, result in results.items():
            if result['success']:
                # Convert path to relative for HTML
                rel_path = os.path.relpath(result['screenshot_path'], os.path.dirname(output_path))
                
                device_info = result.get('device_info', {})
                resolution = f"{device_info.get('width', 'Unknown')}x{device_info.get('height', 'Unknown')}"
                platform = device_info.get('platform', 'Unknown')
                
                # Get file size
                try:
                    file_size = os.path.getsize(result['screenshot_path'])
                    size_str = f"{file_size / 1024:.1f} KB"
                except:
                    size_str = "Unknown"
                
                html_content += f"""
                        <div class="device-card">
                            <div class="device-header">
                                <div class="device-name success">✓ {device_name}</div>
                                <div class="device-info">
                                    {platform} • {resolution} • {size_str}
                                </div>
                            </div>
                            <div class="screenshot-container">
                                <img src="{rel_path}" alt="{device_name} screenshot" class="screenshot">
                            </div>
                        </div>
                """
            else:
                html_content += f"""
                        <div class="device-card">
                            <div class="device-header">
                                <div class="device-name error">✗ {device_name}</div>
                                <div class="device-info">Capture failed</div>
                            </div>
                            <div class="error-message">
                                {result.get('error', 'Unknown error occurred')}
                            </div>
                        </div>
                """
        
        html_content += f"""
                    </div>
                </div>
                
                <div class="footer">
                    Generated by ScreenQA • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def generate_pdf_report(self, results: Dict, url: str, 
                           output_path: str = None) -> str:
        """Generate PDF report"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.reports_dir, f'qa_report_{timestamp}.pdf')
        
        # Create PDF
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        
        # Title page
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredText(width/2, height - 100, "ScreenQA Testing Report")
        
        c.setFont("Helvetica", 12)
        c.drawCentredText(width/2, height - 150, f"URL: {url}")
        c.drawCentredText(width/2, height - 170, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Stats
        total_devices = len(results)
        successful = sum(1 for r in results.values() if r['success'])
        
        c.drawCentredText(width/2, height - 220, f"Total Devices: {total_devices}")
        c.drawCentredText(width/2, height - 240, f"Successful Captures: {successful}")
        c.drawCentredText(width/2, height - 260, f"Success Rate: {successful/total_devices*100:.1f}%")
        
        y_position = height - 320
        
        # Device results
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y_position, "Device Results:")
        y_position -= 30
        
        c.setFont("Helvetica", 10)
        for device_name, result in results.items():
            if y_position < 100:
                c.showPage()
                y_position = height - 50
            
            status = "SUCCESS" if result['success'] else "FAILED"
            c.drawString(50, y_position, f"• {device_name}: {status}")
            
            if result['success'] and result.get('device_info'):
                device_info = result['device_info']
                resolution = f"{device_info.get('width')}x{device_info.get('height')}"
                c.drawString(70, y_position - 15, f"Resolution: {resolution}")
                c.drawString(70, y_position - 30, f"Platform: {device_info.get('platform', 'Unknown')}")
                y_position -= 45
            elif not result['success']:
                c.drawString(70, y_position - 15, f"Error: {result.get('error', 'Unknown error')}")
                y_position -= 30
            else:
                y_position -= 15
        
        c.save()
        return output_path
    
    def generate_comparison_report(self, screenshot_groups: Dict[str, List[str]], 
                                 output_path: str = None) -> str:
        """Generate comparison report for multiple screenshot sets"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.reports_dir, f'comparison_report_{timestamp}.html')
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ScreenQA Comparison Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .comparison-group { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
                .screenshots { display: flex; flex-wrap: wrap; gap: 10px; }
                .screenshot { max-width: 300px; }
            </style>
        </head>
        <body>
            <h1>ScreenQA Comparison Report</h1>
        """
        
        for group_name, screenshots in screenshot_groups.items():
            html_content += f"""
            <div class="comparison-group">
                <h2>{group_name}</h2>
                <div class="screenshots">
            """
            
            for screenshot in screenshots:
                rel_path = os.path.relpath(screenshot, os.path.dirname(output_path))
                filename = os.path.basename(screenshot)
                html_content += f'<img src="{rel_path}" alt="{filename}" class="screenshot">'
            
            html_content += "</div></div>"
        
        html_content += """
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path


# Additional utility functions
def batch_resize_screenshots(screenshots_dir: str, max_width: int = 1920, max_height: int = 1080):
    """Batch resize screenshots to reduce file size"""
    resized_count = 0
    
    for filename in os.listdir(screenshots_dir):
        if filename.endswith('.png'):
            filepath = os.path.join(screenshots_dir, filename)
            try:
                with Image.open(filepath) as img:
                    if img.width > max_width or img.height > max_height:
                        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                        img.save(filepath, optimize=True)
                        resized_count += 1
            except Exception as e:
                print(f"Error resizing {filename}: {e}")
    
    return resized_count


def create_device_comparison_matrix(results: Dict, output_path: str):
    """Create a visual comparison matrix of all devices"""
    devices = list(results.keys())
    successful_devices = [name for name, result in results.items() if result['success']]
    
    if not successful_devices:
        return False
    
    # Create figure
    fig, axes = plt.subplots(1, len(successful_devices), figsize=(20, 5))
    if len(successful_devices) == 1:
        axes = [axes]
    
    for i, device_name in enumerate(successful_devices):
        result = results[device_name]
        if result['success']:
            try:
                img = Image.open(result['screenshot_path'])
                axes[i].imshow(img)
                axes[i].set_title(f"{device_name}\\n{img.width}x{img.height}", fontsize=8)
                axes[i].axis('off')
            except Exception as e:
                axes[i].text(0.5, 0.5, f"Error loading\\n{device_name}", 
                           ha='center', va='center', transform=axes[i].transAxes)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return True


if __name__ == "__main__":
    # Example usage
    screenshots_dir = os.path.join(os.path.dirname(__file__), '..', 'screenshots')
    manager = ScreenshotManager(screenshots_dir)
    
    # Print statistics
    stats = manager.get_screenshot_stats()
    print(f"Screenshot Statistics:")
    print(f"  Count: {stats['count']}")
    print(f"  Total Size: {stats['total_size'] / (1024*1024):.2f} MB")
    print(f"  Average Size: {stats['average_size'] / 1024:.1f} KB")