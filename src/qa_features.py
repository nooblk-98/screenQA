import time
import json
import os
from typing import Dict, List, Tuple, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image, ImageDraw, ImageFont
import requests
from urllib.parse import urlparse, urljoin
from datetime import datetime
import statistics


class PerformanceAnalyzer:
    """Analyzes website performance across different devices"""
    
    def __init__(self):
        self.metrics = {}
    
    def measure_load_time(self, url: str, device_config: Dict) -> Dict:
        """Measure page load time for specific device"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'--window-size={device_config["width"]},{device_config["height"]}')
        chrome_options.add_argument(f'--user-agent={device_config["user_agent"]}')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            start_time = time.time()
            driver.get(url)
            
            # Wait for page to be ready
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            load_time = time.time() - start_time
            
            # Get additional performance metrics
            performance_data = driver.execute_script("""
                return {
                    loadEventEnd: performance.timing.loadEventEnd,
                    navigationStart: performance.timing.navigationStart,
                    domContentLoaded: performance.timing.domContentLoadedEventEnd,
                    firstPaint: performance.getEntriesByType('paint')[0] ? performance.getEntriesByType('paint')[0].startTime : null,
                    resources: performance.getEntriesByType('resource').length
                };
            """)
            
            # Calculate metrics
            if performance_data['loadEventEnd'] and performance_data['navigationStart']:
                total_load_time = (performance_data['loadEventEnd'] - performance_data['navigationStart']) / 1000
                dom_ready_time = (performance_data['domContentLoaded'] - performance_data['navigationStart']) / 1000
            else:
                total_load_time = load_time
                dom_ready_time = load_time
            
            return {
                'success': True,
                'load_time': load_time,
                'total_load_time': total_load_time,
                'dom_ready_time': dom_ready_time,
                'first_paint': performance_data['firstPaint'] / 1000 if performance_data['firstPaint'] else None,
                'resource_count': performance_data['resources'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        
        finally:
            driver.quit()
    
    def analyze_performance_across_devices(self, url: str, devices: Dict) -> Dict:
        """Analyze performance across multiple devices"""
        results = {}
        
        for device_name, device_config in devices.items():
            print(f"Testing performance on {device_name}...")
            results[device_name] = self.measure_load_time(url, device_config)
        
        return results
    
    def generate_performance_report(self, results: Dict) -> Dict:
        """Generate performance analysis report"""
        successful_results = {k: v for k, v in results.items() if v.get('success')}
        
        if not successful_results:
            return {'error': 'No successful performance measurements'}
        
        load_times = [r['load_time'] for r in successful_results.values()]
        
        report = {
            'summary': {
                'devices_tested': len(results),
                'successful_tests': len(successful_results),
                'average_load_time': statistics.mean(load_times),
                'median_load_time': statistics.median(load_times),
                'min_load_time': min(load_times),
                'max_load_time': max(load_times),
                'std_deviation': statistics.stdev(load_times) if len(load_times) > 1 else 0
            },
            'device_results': successful_results,
            'recommendations': self.generate_performance_recommendations(successful_results)
        }
        
        return report
    
    def generate_performance_recommendations(self, results: Dict) -> List[str]:
        """Generate performance improvement recommendations"""
        recommendations = []
        load_times = [r['load_time'] for r in results.values()]
        avg_load_time = statistics.mean(load_times)
        
        if avg_load_time > 5:
            recommendations.append("⚠️ Page load time is too slow (>5s). Consider optimizing images, minifying CSS/JS, and using CDN.")
        elif avg_load_time > 3:
            recommendations.append("⚡ Page load time could be improved (<3s is ideal for user experience).")
        else:
            recommendations.append("✅ Good page load performance!")
        
        # Check for resource count
        resource_counts = [r.get('resource_count', 0) for r in results.values()]
        avg_resources = statistics.mean(resource_counts) if resource_counts else 0
        
        if avg_resources > 100:
            recommendations.append("📦 High number of resources loaded. Consider bundling CSS/JS files.")
        
        # Check for mobile vs desktop performance
        mobile_devices = [k for k in results.keys() if any(mobile in k.lower() for mobile in ['iphone', 'android', 'mobile'])]
        desktop_devices = [k for k in results.keys() if k not in mobile_devices]
        
        if mobile_devices and desktop_devices:
            mobile_times = [results[d]['load_time'] for d in mobile_devices]
            desktop_times = [results[d]['load_time'] for d in desktop_devices]
            
            mobile_avg = statistics.mean(mobile_times)
            desktop_avg = statistics.mean(desktop_times)
            
            if mobile_avg > desktop_avg * 1.5:
                recommendations.append("📱 Mobile performance significantly slower than desktop. Consider mobile-specific optimizations.")
        
        return recommendations


class ResponsiveAnalyzer:
    """Analyzes responsive design behavior"""
    
    def __init__(self):
        self.breakpoints = {
            'mobile': 320,
            'mobile_large': 425,
            'tablet': 768,
            'laptop': 1024,
            'desktop': 1440,
            'desktop_large': 2560
        }
    
    def test_breakpoints(self, url: str, custom_breakpoints: Dict = None) -> Dict:
        """Test responsive behavior at different breakpoints"""
        breakpoints = custom_breakpoints or self.breakpoints
        results = {}
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            for bp_name, width in breakpoints.items():
                print(f"Testing breakpoint: {bp_name} ({width}px)")
                
                # Set viewport
                driver.set_window_size(width, 1080)
                driver.get(url)
                time.sleep(2)
                
                # Analyze layout
                layout_info = self.analyze_layout_at_breakpoint(driver, width)
                
                # Take screenshot
                screenshot_path = os.path.join(
                    os.path.dirname(__file__), '..', 'screenshots',
                    f'responsive_{bp_name}_{width}px_{int(time.time())}.png'
                )
                driver.save_screenshot(screenshot_path)
                
                results[bp_name] = {
                    'width': width,
                    'screenshot_path': screenshot_path,
                    'layout_info': layout_info
                }
                
        except Exception as e:
            print(f"Error testing breakpoints: {e}")
        
        finally:
            driver.quit()
        
        return results
    
    def analyze_layout_at_breakpoint(self, driver, width: int) -> Dict:
        """Analyze layout characteristics at specific breakpoint"""
        try:
            # Get viewport dimensions
            viewport = driver.execute_script("return {width: window.innerWidth, height: window.innerHeight};")
            
            # Check for horizontal scrolling
            has_horizontal_scroll = driver.execute_script("return document.documentElement.scrollWidth > window.innerWidth;")
            
            # Get navigation info
            nav_elements = driver.find_elements(By.TAG_NAME, "nav")
            header_elements = driver.find_elements(By.TAG_NAME, "header")
            
            # Check for mobile menu (common indicators)
            mobile_menu_indicators = driver.find_elements(By.CSS_SELECTOR, ".mobile-menu, .hamburger, .menu-toggle, [class*='burger']")
            
            # Get font sizes (sample from various elements)
            font_sizes = []
            for tag in ['h1', 'h2', 'p', 'span']:
                elements = driver.find_elements(By.TAG_NAME, tag)[:5]  # Sample first 5
                for element in elements:
                    try:
                        font_size = driver.execute_script("return window.getComputedStyle(arguments[0]).fontSize;", element)
                        if font_size:
                            font_sizes.append(float(font_size.replace('px', '')))
                    except:
                        pass
            
            return {
                'viewport': viewport,
                'has_horizontal_scroll': has_horizontal_scroll,
                'navigation_elements': len(nav_elements),
                'header_elements': len(header_elements),
                'mobile_menu_present': len(mobile_menu_indicators) > 0,
                'average_font_size': statistics.mean(font_sizes) if font_sizes else None,
                'font_size_range': {'min': min(font_sizes), 'max': max(font_sizes)} if font_sizes else None
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_responsive_report(self, breakpoint_results: Dict) -> Dict:
        """Generate responsive design analysis report"""
        issues = []
        recommendations = []
        
        for bp_name, result in breakpoint_results.items():
            layout = result.get('layout_info', {})
            
            # Check for horizontal scrolling
            if layout.get('has_horizontal_scroll'):
                issues.append(f"Horizontal scrolling detected at {bp_name} ({result['width']}px)")
            
            # Check font sizes
            avg_font_size = layout.get('average_font_size')
            if avg_font_size and result['width'] <= 425:  # Mobile
                if avg_font_size < 14:
                    issues.append(f"Font size too small on mobile ({avg_font_size:.1f}px at {bp_name})")
            
            # Check for mobile menu
            if result['width'] <= 768 and not layout.get('mobile_menu_present'):
                issues.append(f"No mobile menu detected at {bp_name}")
        
        # Generate recommendations
        if issues:
            recommendations.append("🔧 Fix responsive design issues identified above")
        else:
            recommendations.append("✅ No major responsive issues detected")
        
        return {
            'issues': issues,
            'recommendations': recommendations,
            'breakpoint_analysis': breakpoint_results
        }


class AccessibilityChecker:
    """Basic accessibility checking"""
    
    def check_accessibility(self, url: str) -> Dict:
        """Perform basic accessibility checks"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            driver.get(url)
            time.sleep(3)
            
            issues = []
            recommendations = []
            
            # Check for alt text on images
            images = driver.find_elements(By.TAG_NAME, "img")
            images_without_alt = [img for img in images if not img.get_attribute("alt")]
            
            if images_without_alt:
                issues.append(f"{len(images_without_alt)} images missing alt text")
                recommendations.append("Add descriptive alt text to all images")
            
            # Check for heading structure
            headings = {}
            for level in range(1, 7):
                headings[f'h{level}'] = len(driver.find_elements(By.TAG_NAME, f"h{level}"))
            
            if headings['h1'] == 0:
                issues.append("No H1 heading found")
                recommendations.append("Add a main H1 heading to the page")
            elif headings['h1'] > 1:
                issues.append(f"Multiple H1 headings found ({headings['h1']})")
                recommendations.append("Use only one H1 heading per page")
            
            # Check for form labels
            inputs = driver.find_elements(By.TAG_NAME, "input")
            unlabeled_inputs = []
            for input_elem in inputs:
                input_id = input_elem.get_attribute("id")
                input_type = input_elem.get_attribute("type")
                
                if input_type not in ['hidden', 'submit', 'button']:
                    has_label = False
                    if input_id:
                        labels = driver.find_elements(By.CSS_SELECTOR, f"label[for='{input_id}']")
                        has_label = len(labels) > 0
                    
                    if not has_label:
                        # Check for aria-label or title
                        aria_label = input_elem.get_attribute("aria-label")
                        title = input_elem.get_attribute("title")
                        placeholder = input_elem.get_attribute("placeholder")
                        
                        if not (aria_label or title or placeholder):
                            unlabeled_inputs.append(input_elem)
            
            if unlabeled_inputs:
                issues.append(f"{len(unlabeled_inputs)} form inputs without proper labels")
                recommendations.append("Add labels or aria-label attributes to form inputs")
            
            # Check color contrast (basic check)
            contrast_issues = self.check_basic_contrast(driver)
            if contrast_issues:
                issues.extend(contrast_issues)
                recommendations.append("Improve color contrast for better readability")
            
            return {
                'success': True,
                'issues': issues,
                'recommendations': recommendations,
                'details': {
                    'images_total': len(images),
                    'images_without_alt': len(images_without_alt),
                    'heading_structure': headings,
                    'form_inputs': len(inputs),
                    'unlabeled_inputs': len(unlabeled_inputs)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        
        finally:
            driver.quit()
    
    def check_basic_contrast(self, driver) -> List[str]:
        """Basic color contrast checking"""
        issues = []
        
        try:
            # Check common text elements
            text_elements = driver.find_elements(By.CSS_SELECTOR, "p, h1, h2, h3, h4, h5, h6, span, a, button")[:20]
            
            low_contrast_count = 0
            for element in text_elements:
                try:
                    styles = driver.execute_script("""
                        var elem = arguments[0];
                        var style = window.getComputedStyle(elem);
                        return {
                            color: style.color,
                            backgroundColor: style.backgroundColor,
                            fontSize: style.fontSize
                        };
                    """, element)
                    
                    # This is a simplified check - real contrast checking requires color parsing
                    color = styles.get('color', '')
                    bg_color = styles.get('backgroundColor', '')
                    
                    # Basic check for very light text on light background or dark on dark
                    if ('rgb(255, 255, 255)' in color or 'rgb(240,' in color) and ('rgb(255' in bg_color or 'rgba(0, 0, 0, 0)' in bg_color):
                        low_contrast_count += 1
                    
                except:
                    pass
            
            if low_contrast_count > 2:
                issues.append(f"Potential low contrast issues detected on {low_contrast_count} elements")
                
        except Exception as e:
            pass
        
        return issues


class SEOAnalyzer:
    """Basic SEO analysis"""
    
    def analyze_seo(self, url: str) -> Dict:
        """Perform basic SEO analysis"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            driver.get(url)
            time.sleep(3)
            
            issues = []
            recommendations = []
            
            # Check title
            title = driver.title
            if not title:
                issues.append("Missing page title")
                recommendations.append("Add a descriptive page title")
            elif len(title) > 60:
                issues.append(f"Title too long ({len(title)} characters)")
                recommendations.append("Keep title under 60 characters")
            elif len(title) < 30:
                issues.append(f"Title too short ({len(title)} characters)")
                recommendations.append("Make title more descriptive (30-60 characters)")
            
            # Check meta description
            meta_desc = driver.find_elements(By.CSS_SELECTOR, "meta[name='description']")
            if not meta_desc:
                issues.append("Missing meta description")
                recommendations.append("Add a meta description (150-160 characters)")
            else:
                desc_content = meta_desc[0].get_attribute("content")
                if desc_content:
                    if len(desc_content) > 160:
                        issues.append(f"Meta description too long ({len(desc_content)} characters)")
                    elif len(desc_content) < 120:
                        issues.append(f"Meta description too short ({len(desc_content)} characters)")
            
            # Check headings
            h1_tags = driver.find_elements(By.TAG_NAME, "h1")
            if len(h1_tags) == 0:
                issues.append("Missing H1 tag")
                recommendations.append("Add an H1 tag with main keyword")
            elif len(h1_tags) > 1:
                issues.append(f"Multiple H1 tags ({len(h1_tags)})")
                recommendations.append("Use only one H1 tag per page")
            
            # Check images alt text
            images = driver.find_elements(By.TAG_NAME, "img")
            images_without_alt = [img for img in images if not img.get_attribute("alt")]
            if images_without_alt:
                issues.append(f"{len(images_without_alt)} images missing alt text")
                recommendations.append("Add alt text to all images for SEO and accessibility")
            
            # Check for meta viewport (mobile-friendly)
            viewport_meta = driver.find_elements(By.CSS_SELECTOR, "meta[name='viewport']")
            if not viewport_meta:
                issues.append("Missing viewport meta tag")
                recommendations.append("Add viewport meta tag for mobile compatibility")
            
            return {
                'success': True,
                'issues': issues,
                'recommendations': recommendations,
                'details': {
                    'title': title,
                    'title_length': len(title) if title else 0,
                    'meta_description_length': len(desc_content) if meta_desc and desc_content else 0,
                    'h1_count': len(h1_tags),
                    'total_images': len(images),
                    'images_without_alt': len(images_without_alt),
                    'has_viewport_meta': len(viewport_meta) > 0
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        
        finally:
            driver.quit()


class ComprehensiveQAAnalyzer:
    """Main QA analyzer that combines all analysis tools"""
    
    def __init__(self):
        self.performance_analyzer = PerformanceAnalyzer()
        self.responsive_analyzer = ResponsiveAnalyzer()
        self.accessibility_checker = AccessibilityChecker()
        self.seo_analyzer = SEOAnalyzer()
    
    def run_full_analysis(self, url: str, devices: Dict) -> Dict:
        """Run comprehensive QA analysis"""
        print("Starting comprehensive QA analysis...")
        
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'performance': None,
            'responsive': None,
            'accessibility': None,
            'seo': None,
            'summary': {}
        }
        
        try:
            # Performance analysis
            print("Analyzing performance...")
            perf_results = self.performance_analyzer.analyze_performance_across_devices(url, devices)
            results['performance'] = self.performance_analyzer.generate_performance_report(perf_results)
        except Exception as e:
            results['performance'] = {'error': str(e)}
        
        try:
            # Responsive analysis
            print("Analyzing responsive design...")
            responsive_results = self.responsive_analyzer.test_breakpoints(url)
            results['responsive'] = self.responsive_analyzer.generate_responsive_report(responsive_results)
        except Exception as e:
            results['responsive'] = {'error': str(e)}
        
        try:
            # Accessibility analysis
            print("Checking accessibility...")
            results['accessibility'] = self.accessibility_checker.check_accessibility(url)
        except Exception as e:
            results['accessibility'] = {'error': str(e)}
        
        try:
            # SEO analysis
            print("Analyzing SEO...")
            results['seo'] = self.seo_analyzer.analyze_seo(url)
        except Exception as e:
            results['seo'] = {'error': str(e)}
        
        # Generate summary
        results['summary'] = self.generate_analysis_summary(results)
        
        return results
    
    def generate_analysis_summary(self, results: Dict) -> Dict:
        """Generate overall analysis summary"""
        total_issues = 0
        total_recommendations = 0
        categories_analyzed = 0
        
        summary = {
            'overall_score': 0,
            'categories': {},
            'top_issues': [],
            'top_recommendations': []
        }
        
        for category in ['performance', 'responsive', 'accessibility', 'seo']:
            if results.get(category) and 'error' not in results[category]:
                categories_analyzed += 1
                
                issues = results[category].get('issues', [])
                recommendations = results[category].get('recommendations', [])
                
                total_issues += len(issues)
                total_recommendations += len(recommendations)
                
                # Calculate category score (simple scoring)
                category_score = max(0, 100 - (len(issues) * 10))
                summary['categories'][category] = {
                    'score': category_score,
                    'issues_count': len(issues),
                    'recommendations_count': len(recommendations)
                }
                
                # Add top issues and recommendations
                summary['top_issues'].extend(issues[:2])  # Top 2 from each category
                summary['top_recommendations'].extend(recommendations[:2])
        
        # Calculate overall score
        if categories_analyzed > 0:
            avg_score = sum(cat['score'] for cat in summary['categories'].values()) / categories_analyzed
            summary['overall_score'] = round(avg_score, 1)
        
        summary['total_issues'] = total_issues
        summary['total_recommendations'] = total_recommendations
        summary['categories_analyzed'] = categories_analyzed
        
        return summary
    
    def save_analysis_report(self, analysis_results: Dict, output_path: str = None) -> str:
        """Save analysis results to JSON file"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(os.path.dirname(__file__), '..', 'reports', f'qa_analysis_{timestamp}.json')
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        return output_path


if __name__ == "__main__":
    # Example usage
    analyzer = ComprehensiveQAAnalyzer()
    
    # Example device configuration
    devices = {
        "Desktop": {
            "width": 1920,
            "height": 1080,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
        "Mobile": {
            "width": 375,
            "height": 667,
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        }
    }
    
    # Run analysis
    results = analyzer.run_full_analysis("https://example.com", devices)
    
    # Save results
    report_path = analyzer.save_analysis_report(results)
    print(f"Analysis complete! Report saved to: {report_path}")
    
    # Print summary
    summary = results['summary']
    print(f"\\nOverall Score: {summary['overall_score']}/100")
    print(f"Total Issues: {summary['total_issues']}")
    print(f"Categories Analyzed: {summary['categories_analyzed']}")