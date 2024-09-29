import time
import re
import json
import datetime
from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# Import configurations from config.py
import config

# Define the blacklist directly or load from a file/module
blacklist = [
    "https://bold.org/scholarships/by-demographics/minorities/black-students-scholarships/",
    "https://bold.org/scholarships/by-demographics/minorities/hispanic-students-scholarships/",
    "https://bold.org/scholarships/by-demographics/minorities/",
    "https://bold.org/scholarships/by-demographics/minorities/native-american-scholarships/",
    "https://bold.org/scholarships/by-demographics/women/",
    "https://bold.org/scholarships/by-demographics/women/women-stem-scholarships/",
    "https://bold.org/scholarships/by-demographics/",
    "https://bold.org/scholarships/by-state/florida-scholarships/",
    "https://bold.org/scholarships/by-state/texas-scholarships/",
    "https://bold.org/scholarships/by-state/",
    "https://bold.org/scholarships/by-year/graduate-students-scholarships/",
    "https://bold.org/scholarships/by-year/high-school/",
    "https://bold.org/scholarships/by-year/high-school/juniors/",
    "https://bold.org/scholarships/by-year/mba-students-scholarships/",
    "https://bold.org/scholarships/by-year/high-school/seniors/",
    "https://bold.org/scholarships/by-year/undergraduate-scholarships/",
    "https://bold.org/scholarships/by-year/",
    "https://bold.org/scholarships/by-major/law-school-scholarships/",
    "https://bold.org/scholarships/by-major/medical-school-scholarships/",
    "https://bold.org/scholarships/by-major/nursing-scholarships/",
    "https://bold.org/scholarships/by-major/",
    "https://bold.org/scholarships/by-type/easy-scholarships/",
    "https://bold.org/scholarships/by-type/grants-to-pay-off-student-loans/",
    "https://bold.org/scholarships/by-type/merit-based/",
    "https://bold.org/scholarships/by-type/no-essay-scholarships/",
    "https://bold.org/scholarships/by-type/",
    "https://bold.org/",
    "https://bold.org/",
    "https://bold.org/",
    "https://bold.org/scholarships/undergraduate-scholarships/",
    "https://bold.org/scholarships/scholarships-for-college-freshmen-list/",
    "https://bold.org/scholarships/scholarships-for-college-sophomores/",
    "https://bold.org/scholarships/high-school/",
    "https://bold.org/",
    "https://bold.org/scholarships/scholarships-for-graduate-students-list/",
    "https://bold.org/scholarships/no-essay-scholarships-list/",
    "https://bold.org/scholarships/scholarships-for-women/",
    "https://bold.org/scholarships/scholarships-for-women-in-stem-list/",
    "https://bold.org/scholarships/scholarships-for-minorities-list/",
    "https://bold.org/scholarships/scholarships-for-black-students/",
    "https://bold.org/scholarships/native-american/",
    "https://bold.org/scholarships/scholarships-for-hispanic-students-list/",
    "https://bold.org/scholarships/asian-american-and-pacific-islander-scholarships-list/",
    "https://bold.org/scholarships/native-american/",
    "https://bold.org/scholarships/easy-scholarships-list/",
    "https://bold.org/scholarships/computer-science-scholarships/",
    "https://bold.org/scholarships/scholarships-for-women-in-stem-list/",
    "https://bold.org/",
    "https://bold.org/scholarships/",
    "https://bold.org/",
    "https://bold.org/scholarships/north-carolina/",
    "https://bold.org/scholarships/georgia/",
    "https://bold.org/scholarships/michigan/",
    "https://bold.org/scholarships/florida/",
    "https://bold.org/scholarships/by-state/",
    "https://bold.org/",
    "https://bold.org/scholarships/international-students-scholarships/",
    "https://bold.org/scholarships/athletic/",
    "https://bold.org/scholarships/btl-athletes-scholarship/",
    "https://bold.org/scholarships/full-tuition/",
    "https://bold.org/scholarships/blog/how-to-write-a-scholarship-essay/",
    "https://bold.org/",
    "https://bold.org/scholarships/blog/how-to-write-a-scholarship-essay/",
    "https://bold.org/scholarships/blog/how-to-write-a-scholarship-essay/",
    "https://bold.org/",
    "https://bold.org/scholarships/blog/how-to-write-a-scholarship-essay/",
    "http://bold.org/",
    "http://bold.org/",
    "https://bold.org/do-not-sell/",
    "https://bold.org/donors/how-it-works/",
    "https://bold.org/donors/award-features/",
    "https://bold.org/donors/pricing/",
    "https://bold.org/donors/faq/",
    "https://bold.org/donor-terms-and-conditions/",
    "https://bold.org/scholarship-rules/",
    "https://bold.org/blog/",
    "https://bold.org/scholarships/by-demographics/women/",
    "https://bold.org/scholarships/by-year/high-school/",
    "https://bold.org/scholarships/by-type/merit-based/",
    "https://bold.org/scholarships/by-year/high-school/seniors/",
    "https://bold.org/scholarships/by-year/graduate-students-scholarships/",
    "https://bold.org/scholarships/by-major/nursing-scholarships/",
    "https://bold.org/scholarships/by-demographics/minorities/hispanic-students-scholarships/",
    "https://bold.org/scholarships/by-state/texas-scholarships/",
    "https://bold.org/scholarships/",
    "https://bold.org/ambassadors/",
    "https://bold.org/schools/",
    "https://bold.org/about/",
    "https://bold.org/contact/",
    "https://bold.org/careers/",
    "https://bold.org/privacy/",
    "https://bold.org/terms-of-use/",
    "https://bold.org/press/",
    "https://enrollment.bold.org/",
    "https://bold.org/app/home/",
    "https://bold.org/app/home/",
    "https://app.bold.org/debt-automation/onboarding",
    "https://bold.org/resources/",
    "https://bold.org/leaders/",
    "https://bold.org/app/prioritypass/",
    "https://bold.org/scholarships/by-demographics/women/",
    "https://bold.org/scholarships/by-year/high-school/",
    "https://bold.org/scholarships/by-type/merit-based/",
    "https://bold.org/scholarships/by-year/high-school/seniors/",
    "https://bold.org/scholarships/by-year/graduate-students-scholarships/",
    "https://bold.org/scholarships/by-major/nursing-scholarships/",
    "https://bold.org/scholarships/by-demographics/minorities/hispanic-students-scholarships/",
    "https://bold.org/scholarships/by-state/texas-scholarships/",
    "https://bold.org/scholarships/by-state/florida-scholarships/",
    "https://bold.org/scholarships/by-demographics/minorities/native-american-scholarships/",
    "https://bold.org/scholarships/by-demographics/minorities/",
    "https://bold.org/scholarships/by-demographics/women/women-stem-scholarships/",
    "https://bold.org/scholarships/by-major/law-school-scholarships/",
    "https://bold.org/scholarships/by-year/mba-students-scholarships/",
    "https://bold.org/scholarships/by-type/no-essay-scholarships/",
    "https://bold.org/scholarships/by-demographics/minorities/black-students-scholarships/",
    "https://bold.org/scholarships/by-major/medical-school-scholarships/",
    "https://bold.org/scholarships/by-type/easy-scholarships/",
    "https://bold.org/scholarships/by-year/high-school/juniors/",
    "https://bold.org/scholarships/by-type/grants-to-pay-off-student-loans/",
    "https://bold.org/scholarships/by-year/undergraduate-scholarships/",
    "https://bold.org/app/prioritypass/",
    "https://bold.org/app/matched/scholarships/",
]

class ScholarshipScraper:
    def __init__(self):
        self.default_page_load_timeout = 6
        self.driver = self.setup_driver()
        self.scholarship_data = []
        self.blacklist = self.load_blacklist()
        self.executor = ThreadPoolExecutor(max_workers=1)  # Single thread executor

    def setup_driver(self):
        """Set up the Firefox WebDriver"""
        try:
            service = FirefoxService(executable_path=config.GECKODRIVER_PATH)
            options = Options()
            options.binary_location = config.FIREFOX_BINARY_PATH
            # Optional: Run in headless mode
            # options.headless = True
            driver = webdriver.Firefox(options=options, service=service)
            driver.maximize_window()
            driver.set_page_load_timeout(self.default_page_load_timeout)
            return driver
        except Exception as e:
            print(f"Error setting up WebDriver: {e}")
            raise

    def load_blacklist(self):
        """Load the list of blacklisted URLs"""
        return set(blacklist)

    def find_scholarship_links(self, elems, scholarship_list):
        """Find scholarship links from elements and add them to the set"""
        for elem in elems:
            try:
                link = elem.get_attribute("href")
                if link and link not in self.blacklist and 'scholarship' in link and '/contribute/' not in link:
                    scholarship_list.add(link)
            except Exception as e:
                print(f"Error processing element: {e}")

    def look_for_scholarships(self, stop=100):
        """Look for scholarships and return a set of scholarship URLs"""
        scholarship_list = set()
        self.driver.get("https://bold.org/scholarships/")
        wait = WebDriverWait(self.driver, 10)

        # Set filters using JavaScript (adjust filters as needed)
        self.driver.execute_script(
            '''sessionStorage.setItem('bold.scholarshipFilters', '{"selectedCategories":["Any Category"],"selectedEducation":["Any"],"selectedStatus":["Open"],"nameFilter":"","noEssayFilter":false,"sortOption":{"label":"Deadline","value":"deadline","direction":"asc"}}')'''
        )
        time.sleep(1)  # Allow time for filters to apply

        page_number = 1
        while len(scholarship_list) < stop:
            url = f"https://bold.org/scholarships/{page_number}/"
            try:
                self.driver.get(url)
            except TimeoutException:
                print(f"Warning: Timeout while loading scholarship page: {url}. Skipping this scholarship.")
            except WebDriverException as e:
                print(f"WebDriverException while loading {url}: {e}. Skipping this scholarship.")

            time.sleep(0.5)  # Allow page to load
            elems = self.driver.find_elements(By.XPATH, "//a[@href]")
            if not elems:
                print(f"No elements found on page {page_number}, stopping search.")
                break
            self.find_scholarship_links(elems, scholarship_list)
            print(f"Total scholarships found so far: {len(scholarship_list)}")
            if len(scholarship_list) >= stop:
                break
            page_number += 1

        print(f"Total scholarships collected: {len(scholarship_list)}")
        return list(scholarship_list)[:stop]

    def scrape_scholarship(self, scholarship_url):
        """Scrape data from a specific scholarship"""
        print(f"Scraping scholarship: {scholarship_url}")
        scholarship_info = {}

        # Define a dictionary to hold extraction functions and their keys
        extraction_steps = {
            'Title': self.extract_title,
            'Prize': self.extract_prize,
            'Eligibility Requirements': self.get_eligibility_requirements,
            'Content': self.get_scholarship_content,
            'Application Deadline': self.extract_application_deadline_formatted,
            'Winners Announced': self.get_winners_announced_time,
            'Essay Topic': self.get_essay_topic,
        }

        # Attempt to load the scholarship page with timeout
        try:
            self.driver.get(scholarship_url)
        except TimeoutException:
            print(f"Warning: Timeout while loading scholarship page: {scholarship_url}. Skipping this scholarship.")
        except WebDriverException as e:
            print(f"WebDriverException while loading {scholarship_url}: {e}. Skipping this scholarship.")

        for key, func in extraction_steps.items():
            future = self.executor.submit(func)
            try:
                result = future.result(timeout=5)  # 5-second timeout per step
                scholarship_info[key] = result
                if isinstance(result, dict):
                    print(f"{key}: {json.dumps(result, ensure_ascii=False)}")
                else:
                    print(f"{key}: {result if result else 'None'}")
            except TimeoutError:
                print(f"Warning: Timeout while extracting {key} from {scholarship_url}.")
                scholarship_info[key] = None
            except Exception as e:
                print(f"Error extracting {key} from {scholarship_url}: {e}")
                scholarship_info[key] = None

        self.scholarship_data.append(scholarship_info)

        # Print out the scholarship info in JSON format
        print(json.dumps(scholarship_info, ensure_ascii=False, indent=4))

    def extract_title(self):
        """Extract the scholarship title"""
        wait = WebDriverWait(self.driver, 5)
        title_element = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        return title_element.text.strip()

    def extract_prize(self):
        """Extract Max Prize with four fallback methods"""
        # Method 1: Specific class-based XPath
        try:
            prize_element = self.driver.find_element(By.XPATH,
                                                     "//div[contains(@class, 'text-[40px]') and contains(@class, 'font-semibold')]")
            prize_text = prize_element.text.strip()
            if prize_text:
                return prize_text
            else:
                raise ValueError("Prize text is empty.")
        except Exception as e:
            print(f"Method 1 failed to extract Prize: {e}")

        # Method 2: Searching for divs containing a '$' sign
        try:
            prize_elements = self.driver.find_elements(By.XPATH, "//div[contains(text(), '$')]")
            for elem in prize_elements:
                prize_text = elem.text.strip()
                if re.search(r'\$\d+', prize_text):
                    return prize_text
            raise ValueError("No prize found with '$' in text.")
        except Exception as e:
            print(f"Method 2 failed to extract Prize: {e}")

        # Method 3: Locating prize within specific parent div structures
        try:
            prize_parent = self.driver.find_element(By.XPATH, "//div[contains(@class, 'text-text') and contains(@class, 'flex') and contains(text(), '$')]")
            spans = prize_parent.find_elements(By.TAG_NAME, "span")
            for span in spans:
                text = span.text.strip()
                if text.startswith('$'):
                    return text
            raise ValueError("Prize span with '$' not found.")
        except Exception as e:
            print(f"Method 3 failed to extract Prize: {e}")

        # Method 4: Using regex to search all visible text for monetary amounts
        try:
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            match = re.search(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?', page_text)
            if match:
                return match.group(0)
            else:
                raise ValueError("No monetary amount found using regex.")
        except Exception as e:
            print(f"Method 4 failed to extract Prize: {e}")

        # If all methods fail
        print("Failed to extract Prize using all methods.")
        return None

    def extract_application_deadline_formatted(self):
        """Extract and format Application Deadline"""
        deadline_raw = self.extract_application_deadline()
        return self.format_date(deadline_raw)

    def extract_application_deadline(self):
        """Extract Application Deadline with fallback methods"""
        # Method 1: Direct following sibling
        try:
            deadline_label = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Application Deadline')]")
            deadline_text = deadline_label.find_element(By.XPATH, "./following-sibling::div").text.strip()
            if deadline_text:
                return deadline_text
            else:
                raise ValueError("Deadline text is empty.")
        except Exception as e:
            print(f"Method 1 failed to extract Application Deadline: {e}")

        # Method 2: Search for patterns like 'Deadline: Dec 31, 2024'
        try:
            deadline_elements = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'Deadline') or contains(text(), 'deadline')]")
            for elem in deadline_elements:
                deadline_text = elem.text.strip()
                match = re.search(r'\b\w{3,9}\s\d{1,2},\s\d{4}\b', deadline_text)
                if match:
                    return match.group(0)
            raise ValueError("No date pattern found in Method 2.")
        except Exception as e:
            print(f"Method 2 failed to extract Application Deadline: {e}")

        # Method 3: Look for divs with class containing 'deadline'
        try:
            deadline_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'deadline') and contains(text(), '$')]")
            deadline_text = deadline_element.text.strip()
            if deadline_text:
                return deadline_text
            else:
                raise ValueError("Deadline text is empty in Method 3.")
        except Exception as e:
            print(f"Method 3 failed to extract Application Deadline: {e}")

        # Method 4: Use regex to find dates in all visible text
        try:
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            matches = re.findall(r'\b\w{3,9}\s\d{1,2},\s\d{4}\b', page_text)
            if matches:
                # Assuming the first match is the deadline
                return matches[0]
            else:
                raise ValueError("No date found using regex in Method 4.")
        except Exception as e:
            print(f"Method 4 failed to extract Application Deadline: {e}")

        # If all methods fail
        print("Failed to extract Application Deadline using all methods.")
        return None

    def format_date(self, date_str):
        """Convert date string to MM/DD/YYYY format."""
        if not date_str:
            return None
        try:
            # Remove ordinal suffixes (e.g., 'st', 'nd', 'rd', 'th')
            date_str_clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
            # Define possible date formats
            date_formats = [
                "%b %d, %Y",    # Dec 31, 2024
                "%B %d, %Y",    # December 31, 2024
                "%m/%d/%Y",     # 12/31/2024
                "%m-%d-%Y",     # 12-31-2024
                "%Y-%m-%d",     # 2024-12-31
            ]
            for fmt in date_formats:
                try:
                    parsed_date = datetime.datetime.strptime(date_str_clean, fmt)
                    return parsed_date.strftime("%m/%d/%Y")
                except ValueError:
                    continue
            # If none of the formats match, attempt to parse using dateutil (if available)
            try:
                from dateutil import parser
                parsed_date = parser.parse(date_str_clean)
                return parsed_date.strftime("%m/%d/%Y")
            except (ImportError, ValueError):
                pass
            print(f"Unable to parse date: {date_str}")
            return date_str  # Return the original string if parsing fails
        except Exception as e:
            print(f"Error formatting date '{date_str}': {e}")
            return date_str  # Return the original string in case of error

    def get_eligibility_requirements(self):
        """Extract eligibility requirements as a dictionary"""
        try:
            # Find the Eligibility Requirements section
            requirements_section = self.driver.find_element(By.XPATH, "//div[contains(., 'Eligibility Requirements') and contains(@class, 'mb-10')]")
            # Now, within this section, find all the labels and values
            labels = requirements_section.find_elements(By.XPATH, ".//div[@class='mr-5 hidden md:block']//div[@class='text-text whitespace-nowrap text-sm font-medium']")
            values = requirements_section.find_elements(By.XPATH, ".//div[@class='hidden md:block']//div[@class='text-text text-sm']")
            # Create a dictionary of eligibility requirements
            eligibility_dict = {}
            for label, value in zip(labels, values):
                eligibility_dict[label.text.strip().rstrip(':')] = value.text.strip()
            return eligibility_dict
        except Exception as e:
            print(f"Error extracting eligibility requirements: {e}")
            return None

    def get_scholarship_content(self):
        """Extracts the scholarship content from the webpage"""
        try:
            content_div = self.driver.find_element(By.CSS_SELECTOR, "div[class*='break-words text-lg']")
            content_text = content_div.text.strip()
            return content_text
        except Exception as e:
            print(f"Error extracting content: {e}")
            return None

    def get_winners_announced_time(self):
        """Extract the winners announced time"""
        try:
            # Find the element that contains 'Winner Announced'
            winner_label = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Winner Announced')]")
            # The date is in the following div
            winner_text = winner_label.find_element(By.XPATH, "./following-sibling::div").text.strip()
            return winner_text
        except Exception as e:
            print(f"Error extracting winners announced time: {e}")
            return None

    def get_essay_topic(self):
        """Extract the essay topic"""
        try:
            essay_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Essay Topic')]/following-sibling::div")
            essay_text = essay_element.text.strip()
            return essay_text
        except Exception as e:
            print(f"Error extracting essay topic: {e}")
            return None

    def close(self):
        """Closes the WebDriver and executor"""
        self.driver.quit()
        self.executor.shutdown(wait=False)
        print("WebDriver and Executor closed.")

def main():
    scraper = ScholarshipScraper()
    try:
        # Look for scholarships and scrape data
        scholarships = scraper.look_for_scholarships(stop=400)
        for scholarship_url in scholarships:
            scraper.scrape_scholarship(scholarship_url)
            # Optional: Sleep to be polite to the server
            time.sleep(0.5)
        # At this point, scraper.scholarship_data contains all the scraped data
        # You can save it to a file or process it further
        # For example, save to a JSON file:
        with open('scholarships_data.json', 'w', encoding='utf-8') as f:
            json.dump(scraper.scholarship_data, f, ensure_ascii=False, indent=4)
        print("Scholarship data saved to 'scholarships_data.json'")
    finally:
        scraper.close()

def test_scraper():
    scraper = ScholarshipScraper()
    try:
        scraper.scrape_scholarship("https://bold.org/scholarships/concrete-rose-scholarship-award/")
        scraper.scrape_scholarship("https://bold.org/scholarships/christal-carter-creative-arts-scholarship/")
    finally:
        scraper.close()

if __name__ == '__main__':
    # Run the main scraper to scrape 50 scholarships
    main()
    # Alternatively, run a test scraper for specific scholarships
    #test_scraper()
