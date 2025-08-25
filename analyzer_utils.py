# analyzer_utils.py

import re
import time
import requests
from bs4 import BeautifulSoup
import openai
from openai import OpenAI
import os

# ---------- FETCH & TIMING ----------
def fetch_html(url: str, timeout: int = 10):
    """
    Returns (soup, load_time_seconds).
    Ensures `https://` is prepended if missing.
    """
    if not url.lower().startswith("http"):
        url = "https://" + url
    start = time.time()
    response = requests.get(url, timeout=timeout)
    load_time = time.time() - start
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup, load_time

# ---------- RULE-BASED CHECKS ----------
def check_ssl(url: str):
    if url.lower().startswith("https://"):
        return True, ""
    return False, "No SSL (site not secure)."

def check_mobile_meta(soup: BeautifulSoup):
    if soup.find("meta", {"name": "viewport"}):
        return True, ""
    return False, "Missing mobile viewport meta tag (not mobile-friendly)."

def check_page_speed(load_time: float, threshold: float = 4.0):
    if load_time <= threshold:
        return True, ""
    return False, f"Page load time {load_time:.1f}s (slower than {threshold}s)."

def check_company_name_or_title(soup: BeautifulSoup):
    title = soup.title.string if soup.title else ""
    if title and ("home" not in title.lower() and "index" not in title.lower() and len(title.strip()) > 5):
        return True, ""
    return False, "Generic or missing page title (poor SEO)."

def check_phone_number(soup: BeautifulSoup):
    text = soup.get_text()
    phone_patterns = [
        r'\(\d{3}\)\s*\d{3}-\d{4}',  # (123) 456-7890
        r'\d{3}-\d{3}-\d{4}',        # 123-456-7890
        r'\d{3}\.\d{3}\.\d{4}',      # 123.456.7890
        r'\d{10}',                   # 1234567890
    ]
    for pattern in phone_patterns:
        if re.search(pattern, text):
            return True, ""
    return False, "No visible phone number found."

def check_contact_info(soup: BeautifulSoup):
    text = soup.get_text().lower()
    contact_indicators = ["contact", "phone", "call", "email", "@", "address"]
    if any(indicator in text for indicator in contact_indicators):
        return True, ""
    return False, "Limited contact information visible."

def check_professional_content(soup: BeautifulSoup):
    text = soup.get_text().lower()
    professional_indicators = [
        "services", "about", "experience", "professional", "licensed", 
        "insured", "certified", "quality", "expert"
    ]
    count = sum(1 for indicator in professional_indicators if indicator in text)
    
    # Check for DIY website builder indicators (automatic fail)
    if any(builder in text for builder in ['weebly', 'wix', 'squarespace', 'godaddy']):
        return False, "Built with DIY website builder (unprofessional appearance)."
    
    # Require more professional indicators
    if count >= 4:
        return True, ""
    return False, "Content lacks sufficient professional business language."

def check_call_to_action(soup: BeautifulSoup):
    text = soup.get_text().lower()
    cta_phrases = [
        "call now", "contact us", "get quote", "free estimate", 
        "schedule", "book", "hire", "order"
    ]
    if any(phrase in text for phrase in cta_phrases):
        return True, ""
    return False, "No clear call-to-action found."

def check_social_proof(soup: BeautifulSoup):
    text = soup.get_text().lower()
    social_indicators = [
        "review", "testimonial", "customer", "client", "star", 
        "rating", "feedback", "recommend"
    ]
    if any(indicator in text for indicator in social_indicators):
        return True, ""
    return False, "No social proof or testimonials visible."

def check_images_and_media(soup: BeautifulSoup):
    images = soup.find_all("img")
    if len(images) >= 2:
        return True, ""
    return False, "Few or no images found (poor visual appeal)."

# ---------- MAIN ANALYSIS FUNCTION ----------
def analyze_website_comprehensive(url: str, openai_api_key: str):
    """
    Comprehensive website analysis returning score and detailed report.
    """
    try:
        # Fetch website
        soup, load_time = fetch_html(url)
        
        # Run all checks
        checks = [
            ("SSL Certificate", check_ssl(url)),
            ("Mobile Responsiveness", check_mobile_meta(soup)),
            ("Page Speed", check_page_speed(load_time)),
            ("Professional Title", check_company_name_or_title(soup)),
            ("Phone Number", check_phone_number(soup)),
            ("Contact Information", check_contact_info(soup)),
            ("Professional Content", check_professional_content(soup)),
            ("Call to Action", check_call_to_action(soup)),
            ("Social Proof", check_social_proof(soup)),
            ("Images/Media", check_images_and_media(soup))
        ]
        
        # Calculate score with weighted importance and quality assessment
        passed_checks = sum(1 for _, (passed, _) in checks if passed)
        
        # Add quality penalties for common issues
        quality_penalties = 0
        page_text_lower = soup.get_text().lower()
        
        # Check for template/DIY website builders (major penalty)
        if any(builder in page_text_lower for builder in ['weebly', 'wix', 'squarespace', 'godaddy']):
            quality_penalties += 2
        
        # Check for poor design indicators
        if 'under construction' in page_text_lower or 'coming soon' in page_text_lower:
            quality_penalties += 3
        
        # Check for minimal content (major penalty)
        if len(soup.get_text().strip()) < 500:
            quality_penalties += 2
        
        # Check for missing key business elements
        if not any(word in page_text_lower for word in ['service', 'about', 'contact', 'business', 'company']):
            quality_penalties += 2
        
        # Check for unprofessional content
        images = soup.find_all('img')
        images_with_src = 0
        for img in images:
            try:
                if img.get('src'):
                    images_with_src += 1
            except:
                continue
        if images_with_src < 2:
            quality_penalties += 1
        
        # Calculate final score with penalties
        base_score = passed_checks
        final_score = max(1, base_score - quality_penalties)
        score = min(10, final_score)
        
        # Debug info for scoring
        print(f"DEBUG: Base score: {base_score}, Quality penalties: {quality_penalties}, Final score: {score}")
        
        # Generate detailed report
        failed_checks = [name for name, (passed, reason) in checks if not passed and reason]
        
        if failed_checks:
            report = "Issues found:\n" + "\n".join(f"• {reason}" for _, (passed, reason) in checks if not passed and reason)
        else:
            report = "Excellent! This website passes all basic checks for local business optimization."
        
        # Extract business details for later use
        business_name = "Business"
        if soup.title and soup.title.string:
            title_text = soup.title.string.strip()
            if title_text and "home" not in title_text.lower() and "index" not in title_text.lower():
                business_name = title_text
            else:
                business_name = "Local Business"
        
        # Get page text for AI analysis
        page_text = soup.get_text()[:2000]  # First 2000 chars
        
        return {
            'url': url,
            'score': score,
            'report': report,
            'business_name': business_name,
            'page_text': page_text,
            'load_time': load_time,
            'checks': checks
        }
        
    except Exception as e:
        raise Exception(f"Failed to analyze website: {str(e)}")

# ---------- AI-POWERED FUNCTIONS ----------
def generate_lead_qualification(analysis_results: dict, openai_api_key: str):
    """Generate AI-powered lead qualification assessment."""
    try:
        client = OpenAI(api_key=openai_api_key)
        
        prompt = f"""
        Based on this website analysis, determine if this is a good lead for website redesign services:
        
        Website: {analysis_results['url']}
        Business Name: {analysis_results['business_name']}
        Issues Found: {analysis_results['report']}
        
        Consider:
        - Local businesses with poor web presence are prime candidates
        - Missing contact info, poor mobile experience, slow loading, unprofessional appearance are key indicators
        - DIY website builders often indicate a business ready for professional help
        
        Respond with "Yes" or "No" and provide a 2-3 sentence rationale focusing on how these issues are likely costing them customers and business opportunities.
        """
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Unable to generate lead qualification: {str(e)}"

def generate_replit_prompt(analysis_results: dict):
    """Generate the exact Replit site-builder prompt with placeholders filled."""
    try:
        # Read the template
        with open("replit_prompt_template.txt", "r") as f:
            template = f.read()
        
        # Extract domain from URL
        domain = analysis_results['url'].replace("https://", "").replace("http://", "").split("/")[0]
        
        # Determine business type and location from content
        business_type = "Local Business"  # Default
        location = "Local Area"  # Default
        
        # Simple heuristics to detect business type
        text = analysis_results['page_text'].lower()
        if any(word in text for word in ["plumb", "pipe", "drain", "water"]):
            business_type = "Plumbing Company"
        elif any(word in text for word in ["electric", "wire", "power"]):
            business_type = "Electrical Company"
        elif any(word in text for word in ["roof", "gutter", "shingle"]):
            business_type = "Roofing Company"
        elif any(word in text for word in ["hvac", "air", "heat", "cool"]):
            business_type = "HVAC Company"
        elif any(word in text for word in ["lawn", "landscape", "garden"]):
            business_type = "Landscaping Company"
        
        # Replace placeholders in template
        filled_prompt = template.replace("{domain}", domain)
        filled_prompt = filled_prompt.replace("{business_type}", business_type)
        filled_prompt = filled_prompt.replace("{location}", location)
        
        return filled_prompt
        
    except Exception as e:
        return f"Unable to generate Replit prompt: {str(e)}"

def generate_outreach_email(analysis_results: dict, openai_api_key: str):
    """Generate personalized outreach email."""
    try:
        client = OpenAI(api_key=openai_api_key)
        
        prompt = f"""
        Write a professional outreach email for a web design service targeting this local business:
        
        Website: {analysis_results['url']}
        Business: {analysis_results['business_name']}
        Issues Found: {analysis_results['report']}
        
        Email should:
        - Be friendly but professional
        - Mention 2-3 specific issues found on their site and how they impact customer acquisition
        - Explain how these issues are likely costing them business
        - Offer to help improve their online presence
        - Include a soft call-to-action
        - Be 150-200 words
        - Have a subject line
        
        Format as:
        Subject: [subject line]
        
        [email body]
        """
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Unable to generate outreach email: {str(e)}"

def generate_outreach_dm(analysis_results: dict, openai_api_key: str):
    """Generate short social media DM."""
    try:
        client = OpenAI(api_key=openai_api_key)
        
        prompt = f"""
        Write a brief, friendly social media DM for this local business:
        
        Business: {analysis_results['business_name']}
        Website Issues: {analysis_results['report'][:200]}
        
        DM should:
        - Be casual and friendly
        - Mention you noticed their website and how it might be affecting their business
        - Offer help in a non-pushy way focusing on customer acquisition
        - Be under 100 words
        - Feel like a genuine message from one business owner to another
        """
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Unable to generate outreach DM: {str(e)}"
