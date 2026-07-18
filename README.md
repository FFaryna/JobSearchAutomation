Job Search Automation
A Python-based job search automation tool that aggregates remote job listings from multiple job boards, filters them based on your preferences, and ranks them by relevance.

Features
Multi-source scraping: Aggregates job listings from RemoteOK and Remotive APIs
Smart filtering: Filter jobs by keywords, tags, and minimum salary
Intelligent ranking: Scores jobs based on relevance to your criteria with source-weighted scoring
Deduplication: Removes duplicate job listings across sources and keeps the highest quality version
User-friendly interface: Interactive command-line interface to specify your job search preferences
How It Works
The application follows a 5-step pipeline:

Extract: Fetches job data from RemoteOK and Remotive APIs
Deduplicate: Identifies and removes duplicate job listings, keeping the highest quality version
Filter: Narrows down results based on keywords, tags, and minimum salary requirements
Score: Ranks filtered jobs based on relevance to your criteria
Sort & Select: Returns the top N matching job listings
Installation
Clone the repository:

git clone <repository-url>
cd JobSearchAutomation
Install dependencies:

pip install -r requirements.txt
Usage
Run the application:

python main.py
The program will prompt you for:

Tags: Technical skills/technologies you're interested in (e.g., "Python React AWS")
Keywords: Job title keywords to search for (e.g., "backend developer")
Minimum Salary: The lowest acceptable salary in your preferred currency
The application will then display the top 15 job matches with:

Position title
Company name
Minimum salary
Job listing URL
Example
Provide me with the list of Tags you want to see within jobs: python django postgresql
Provide me with a list of keywords in searched jobs: backend developer
Provide me with a minimum acceptable salary: 50000

These are top jobs found:

Senior Backend Developer | TechCorp | 75000.0 | https://remoteok.com/j/...
Full-Stack Developer | StartupXYZ | 60000.0 | https://remotive.com/j/...
Project Structure
main.py: Entry point for the application
pipeline.py: Core data processing pipeline (filtering, scoring, ranking)
remoteok_scraper.py: Scraper for RemoteOK API
remotivecom_scraper.py: Scraper for Remotive.com API
Configuration
Environment Variables
DEBUG_MODE: Set to true to use local JSON file instead of API calls (useful for testing)
Adjustable Parameters
In main.py:

TOP_OFFERS_COUNTS: Number of top results to display (default: 15)
In pipeline.py:

SOURCE_WEIGHTS: Scoring weights for different job sources (default: RemoteOK=1.0, Remotive=0.7) ##To be changed lated

TOP_VALUES: Used internally for ranking (default: 10)
Requirements
See requirements.txt for all dependencies. Main dependencies include:

requests: For API calls to job boards
License
MIT

Contributing
Contributions are welcome! Please feel free to submit pull requests with improvements.

Note
This tool respects the terms of service of the job board APIs. Please ensure you comply with their usage policies when running this application.

### Extensions for future versions:
- Create Job class to standardise output of the scrapers
- Implement AI to analyse unstructured data from scrapers and create tags/descriptions for useful scoring system
  - refine scoring
- Allow user to upload CV, scrape data, let AI match jobs -> later version
- Create UI/explore streamlit