# Website Analyzer & Site Builder

## Overview

The 5MM Website Analyzer & Site Builder is a Streamlit-based web application designed to analyze local business websites and generate comprehensive reports with actionable insights. The system evaluates website quality across multiple dimensions and provides automated tools for lead qualification, site improvement recommendations, and outreach templates.

## System Architecture

### Frontend Architecture
- **Streamlit Web Interface**: Single-page application with session state management
- **Authentication System**: Optional email-based authorization (currently disabled)
- **Interactive UI Components**: Form inputs, file uploads, real-time analysis displays
- **PDF Export**: Optional report generation using pdfkit

### Backend Architecture
- **Analysis Engine**: Rule-based website evaluation with OpenAI API integration
- **Web Scraping**: BeautifulSoup for HTML parsing and content extraction
- **API Integration**: OpenAI GPT models for intelligent analysis and content generation
- **Session Management**: Streamlit session state for user data persistence

### Data Processing Pipeline
1. URL validation and SSL checking
2. HTML content fetching with performance timing
3. Rule-based technical analysis (mobile-friendly, SEO, speed)
4. AI-powered content analysis using OpenAI
5. Lead qualification scoring (1-10 scale)
6. Automated template generation for outreach and site building

## Key Components

### Core Analysis Module (`analyzer_utils.py`)
- **Website Fetching**: HTTP requests with timeout handling and automatic HTTPS enforcement
- **Technical Checks**: SSL validation, mobile viewport detection, page speed analysis
- **Content Analysis**: Company name extraction, phone number detection, SEO evaluation
- **AI Integration**: OpenAI API calls for comprehensive website analysis

### Main Application (`main.py` / `app.py`)
- **User Interface**: Streamlit components for URL input and results display
- **Authentication Flow**: Optional email verification against authorized user list
- **API Key Management**: Secure OpenAI API key handling in session state
- **Results Management**: Analysis caching and export functionality

### Authorization System (`authorized_users.py`)
- **Access Control**: Email-based whitelist for application access
- **Configuration**: Simple Python list for authorized email addresses

### Template Generation
- **Replit Prompt**: Structured prompts for AI site building
- **Outreach Templates**: Email and DM templates for lead contact
- **PDF Reports**: Optional formatted report generation

## Data Flow

1. **User Authentication** (if enabled): Email verification against authorized list
2. **API Key Validation**: OpenAI API key verification and session storage
3. **URL Input**: Website URL validation and preprocessing
4. **Content Fetching**: HTML retrieval with performance monitoring
5. **Technical Analysis**: Rule-based checks for common web standards
6. **AI Analysis**: OpenAI-powered comprehensive website evaluation
7. **Report Generation**: Scoring, recommendations, and template creation
8. **Export Options**: PDF download and clipboard copying functionality

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework for user interface
- **OpenAI**: AI analysis and content generation via GPT models
- **BeautifulSoup4**: HTML parsing and content extraction
- **Requests**: HTTP client for website fetching
- **python-dotenv**: Environment variable management

### Optional Dependencies
- **pdfkit**: PDF report generation (requires system-level wkhtmltopdf)
- **trafilatura**: Advanced text extraction (not actively used)

### Environment Variables
- `OPENAI_API_KEY`: Required for AI analysis functionality
- Additional API keys can be added to `.env` file

## Deployment Strategy

### Replit Configuration
- **Runtime**: Python 3.11 with Nix package management
- **Port Configuration**: Internal port 5000, external port 80
- **Autoscale Deployment**: Configured for automatic scaling
- **Process Management**: Streamlit server with custom port binding

### Deployment Commands
```bash
streamlit run main.py --server.port 5000
```

### Environment Setup
1. Fork repository in Replit
2. Create `.env` file with OpenAI API key
3. Configure authorized users in `authorized_users.py`
4. Run application using Replit's run button

### File Structure
```
/
├── main.py              # Primary application entry point
├── app.py               # Alternative entry point (duplicate)
├── analyzer_utils.py    # Core analysis functionality
├── authorized_users.py  # Access control configuration
├── pdf_generator.py     # PDF export functionality
├── replit_prompt_template.txt  # Template for site building
├── .env                 # Environment variables (user-created)
├── .streamlit/          # Streamlit configuration
└── requirements files   # Python dependencies
```

## Changelog
- June 23, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.