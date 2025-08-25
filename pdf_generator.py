# pdf_generator.py

def generate_pdf_report(results: dict, url: str):
    """
    Generate PDF report from analysis results.
    Optional functionality - requires pdfkit installation.
    """
    try:
        import pdfkit
        from datetime import datetime
        
        # Create HTML content for PDF
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Website Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }}
                .score {{ font-size: 48px; font-weight: bold; text-align: center; 
                         padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .score.high {{ background-color: #d4edda; color: #155724; }}
                .score.medium {{ background-color: #fff3cd; color: #856404; }}
                .score.low {{ background-color: #f8d7da; color: #721c24; }}
                .section {{ margin: 30px 0; }}
                .section h2 {{ color: #333; border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
                pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; 
                      white-space: pre-wrap; word-wrap: break-word; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Website Analysis Report</h1>
                <p><strong>Website:</strong> {url}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>Overall Score</h2>
                <div class="score {'high' if results['analysis']['score'] >= 7 else 'medium' if results['analysis']['score'] >= 4 else 'low'}">
                    {results['analysis']['score']}/10
                </div>
            </div>
            
            <div class="section">
                <h2>Analysis Report</h2>
                <pre>{results['analysis']['report']}</pre>
            </div>
            
            <div class="section">
                <h2>Lead Qualification</h2>
                <pre>{results['lead_qualification']}</pre>
            </div>
            
            <div class="section">
                <h2>Replit Site Builder Prompt</h2>
                <pre>{results['replit_prompt']}</pre>
            </div>
            
            <div class="section">
                <h2>Outreach Email</h2>
                <pre>{results['outreach_email']}</pre>
            </div>
            
            <div class="section">
                <h2>Outreach DM</h2>
                <pre>{results['outreach_dm']}</pre>
            </div>
        </body>
        </html>
        """
        
        # Generate PDF
        pdf = pdfkit.from_string(html_content, False)
        return pdf
        
    except ImportError:
        raise ImportError("pdfkit not installed. Run: pip install pdfkit")
    except Exception as e:
        raise Exception(f"PDF generation failed: {str(e)}")
