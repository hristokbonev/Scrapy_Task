# H&M Product Scraper

A Scrapy-based web scraper that extracts a product information from H&M's website

## Features

- **Product Information Extraction**: Scrapes product name, price, color, and available color variations
- **Reviews Data**: Intercepts requests to capture customer reviews count and average rating
- **JavaScript Support**: Uses Playwright integration to handle dynamic content loading

## Requirements

- Python 3.7+
- All dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository**

2. **Create and activate a virtual environment**

3. **Install dependencies**

4. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

## Usage

### Running the Spider

Navigate to the project directory and run:

```bash
cd task_project
scrapy crawl taskspider -o output.json
```

This will:
- Scrape the configured H&M product page
- Extract product information and reviews data
- Save results to `output.json`

## Data Structure

The scraper extracts the following information for the product:

```json
{
    "name": String,
    "price": Double,
    "color": String,
    “availableColors”: Array,
    "reviews_count": Int,
    "reviews_score": Double,
 }

```

### Spider Settings

The spider is configured with the following key features:

- **Playwright Integration**: Handles JavaScript-rendered content
- **Response Interception**: Captures requests for reviews data
- **User-Agent**: Mimics a real browser to avoid detection (the website has bot protection)

##  Troubleshooting

### Common Issues

1. **Stuck on "INFO: Enabled item pipelines" when ran on Windows**:
   - **Issue**: The spider appears to hang after showing "INFO: Enabled item pipelines"
   - **Fix**: Press `Ctrl + C` in the terminal to interrupt and the spider should continue normally
