import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import time

class EnhancedCrawler:
    def __init__(self, base_url, user_agent="MyCrawlerBot", max_depth=3, max_pages=10):
        self.base_url = base_url
        self.visited_html = []  # Store tuples of (URL, HTML content)
        self.urls_to_visit = [(base_url, 0)]
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
        self.robots_parser = RobotFileParser()
        self.robots_parser.set_url(urljoin(base_url, 'robots.txt'))
        self.robots_parser.read()
        self.max_depth = max_depth
        self.max_pages = max_pages

    def get_html_contents(self):
        """Returns a list of HTML content for each fetched page."""
        return [html_content for _, html_content in self.visited_html]
    
    def crawl(self):
        """Starts crawling from the base URL, following internal links only."""
        while self.urls_to_visit and len(self.visited_html) < self.max_pages:
            url, depth = self.urls_to_visit.pop(0)  # FIFO for breadth-first search
            if depth <= self.max_depth:
                self.visit_url(url, depth)
            time.sleep(1)  # Simple rate limiting to be polite
    
    def visit_url(self, url, depth):
        """Visits a URL, stores its HTML, and finds all links to visit next."""
        if len(self.visited_html) >= self.max_pages:  # Check if max pages limit is reached
            return
        if any(url == page_url for page_url, _ in self.visited_html) or not self.robots_parser.can_fetch("*", url):
            return
        print(f"Visiting: {url}")
        try:
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Store URL and HTML content
                self.visited_html.append((url, response.text))
                if len(self.visited_html) >= self.max_pages:  # Check again after adding
                    return
                
                # Process all <a> tags with href attributes
                links = soup.find_all('a', href=True)
                for link in links:
                    full_url = urljoin(url, link['href'])
                    if self.is_internal_url(full_url) and (full_url, depth + 1) not in self.urls_to_visit:
                        self.urls_to_visit.append((full_url, depth + 1))
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
    
    def is_internal_url(self, url):
        """Checks if the URL belongs to the same website as the base URL."""
        parsed_base = urlparse(self.base_url)
        parsed_url = urlparse(url)
        return parsed_base.netloc == parsed_url.netloc

# Example usage
if __name__ == '__main__':
    crawler = EnhancedCrawler('http://books.toscrape.com/', max_pages=10)  # Set max_pages to 10
    crawler.crawl()
    html_contents = crawler.get_html_contents()
    for html_content in html_contents:
        print(f"HTML Length: {len(html_content)} characters\n")
