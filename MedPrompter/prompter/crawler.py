from bs4 import BeautifulSoup
import requests
import os
from dataclasses import dataclass
from urllib.parse import urljoin
import re


@dataclass
class Action:
    selector: str
    action: str

class Crawler:
    def __init__(self, base_url, action_sequences=[]):
        self.current_target_stack = [base_url]
        self.action_sequences = action_sequences

    def soupify(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def extract_links_div(self, soup, selector='col-md-6'):        
        left_column = soup.find("div", class_=selector)
        if not left_column:
            return []
        links = left_column.find_all('a')
        return links

    def extract_table_links(self, soup, selector='table'):
        table = soup.find('table', class_=selector)
        if not table:
            return []

        rows = table.find_all('tr')
        links = []
        for row in rows:
            link = row.find('a')
            if link:
                links.append(link)
        return links
    
    def extract_data(self, soup, selector=None):
        # Find all bold elements
        bold_elements = soup.find_all('b')
        results = {}
        for bold in bold_elements:
            if ":" not in bold.text:
                continue
            else:
                results[bold.text.split(":")[0].strip()] = "test"
        print(results)
        
        # Special handling for Medical Specialty and Sample Name
        h1 = soup.find('h1')
        if h1:
            specialty = h1.find('a')
            if specialty:
                results['Medical Specialty'] = specialty.text.strip()
            sample_name = re.search(r'Sample Name:\s*(.*)', h1.text)
            if sample_name:
                results['Sample Name'] = sample_name.group(1).strip()
        print(results)
        return results
    
    def run_crawler(self):
        for action in self.action_sequences:
            step_results = []
            while self.current_target_stack:
                current_node = self.current_target_stack.pop()
                soup = self.soupify(current_node)
                action_fn = getattr(self, action.action)
                results = action_fn(soup, action.selector)
                step_results.extend(results)

            if "link" in action.action:
                for link in step_results:
                    link_href = link.get('href')
                    next_link = urljoin(current_node, link_href)
                    self.current_target_stack.append(next_link)
                    # print(f'{link_name}: {next_link}')
    
action_1 = Action('col-md-6', 'extract_links_div')
action_2 = Action('table', 'extract_table_links')
action_3 = Action(None, 'extract_data')
           
crawler = Crawler('https://mtsamples.com', [action_1, action_2, action_3])
crawler.run_crawler()