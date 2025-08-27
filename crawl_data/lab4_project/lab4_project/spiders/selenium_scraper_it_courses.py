"""
Selenium scraper: Collect IT-related courses from Edumall, Coursera, edX, and DataCamp.

Collected fields per course:
- platform
- course_name
- instructor
- time_info (duration/effort/pace if available)
- outcomes (short description / what you'll learn, if available)
- course_link
- learning_mode (e.g., self-paced/part-time/full-time if detectable)

Usage:
1) Install dependencies (Python 3.9+ recommended):
   pip install selenium pandas webdriver-manager

2) Make sure Google Chrome is installed. The script uses webdriver-manager to auto-download the right ChromeDriver.

3) Run (headless by default):
   python selenium_scraper_it_courses.py --query "information technology" --per-site 40 --headless

Notes & Caveats:
- Websites change frequently. If a site updates its HTML/CSS, adjust the CSS/XPath selectors marked with TODO in each scraper.
- Respect each website's Terms of Service and robots.txt. This code is for educational/lab purposes.
- "part-time" vs "full-time" is rarely explicit on MOOC sites. The script infers learning_mode from labels like "Self-paced" / schedules when present.
"""
from __future__ import annotations
import re
import time
import argparse
from dataclasses import dataclass, asdict
from typing import List, Optional

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


@dataclass
class Course:
    platform: str
    course_name: str
    instructor: str
    time_info: str
    outcomes: str
    course_link: str
    learning_mode: str


def make_driver(headless: bool = True) -> webdriver.Chrome:
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1600,1200")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(40)
    return driver


def safe_text(el) -> str:
    try:
        return el.text.strip()
    except Exception:
        return ""


def scroll_to_load(driver: webdriver.Chrome, max_scrolls: int = 6, sleep: float = 1.2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# ----------------------- Edumall -----------------------

def scrape_edumall(driver: webdriver.Chrome, query: str, limit: int) -> List[Course]:
    courses: List[Course] = []
    search_url = f"https://edumall.vn/search?query={query.replace(' ', '%20')}"
    driver.get(search_url)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/course/'], a[href*='/khoa-hoc/']"))
        )
    except TimeoutException:
        pass

    scroll_to_load(driver, max_scrolls=8)

    # NOTE: Selectors here are intentionally broad to be resilient.
    cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='/course/'], a[href*='/khoa-hoc/']")
    seen = set()
    for a in cards:
        if len(courses) >= limit:
            break
        href = a.get_attribute("href") or ""
        title = safe_text(a)
        if not href or href in seen or not title:
            continue
        seen.add(href)

        # Attempt to fetch extra meta from nearby elements
        parent = a.find_element(By.XPATH, "./ancestor-or-self::*[1]")
        desc = ""
        try:
            # Try a sibling/child element that could contain a description
            desc_el = parent.find_element(By.XPATH, ".//p | .//div[contains(@class,'description')]")
            desc = safe_text(desc_el)
        except Exception:
            pass

        instructor = ""
        try:
            instr_el = parent.find_element(By.XPATH, ".//*[contains(text(),'Giảng viên')]/following::*[1]")
            instructor = safe_text(instr_el)
        except Exception:
            pass

        time_info = ""
        try:
            time_el = parent.find_element(By.XPATH, ".//*[contains(text(),'giờ') or contains(text(),'buổi') or contains(text(),'tuần')]")
            time_info = safe_text(time_el)
        except Exception:
            pass

        learning_mode = "Self-paced"  # Edumall courses are typically self-paced

        courses.append(Course(
            platform="Edumall",
            course_name=title,
            instructor=instructor,
            time_info=time_info,
            outcomes=desc,
            course_link=href,
            learning_mode=learning_mode,
        ))
    return courses


# ----------------------- Coursera -----------------------

def scrape_coursera(driver: webdriver.Chrome, query: str, limit: int) -> List[Course]:
    courses: List[Course] = []
    search_url = f"https://www.coursera.org/search?query={query.replace(' ', '%20')}"
    driver.get(search_url)

    try:
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "main"))
        )
    except TimeoutException:
        pass

    scroll_to_load(driver, max_scrolls=10)

    # Result links generally contain /learn/, /specializations/, or /professional-certificates/
    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/learn/'], a[href*='/specializations/'], a[href*='/professional-certificates/']")

    seen = set()
    for a in links:
        if len(courses) >= limit:
            break
        href = a.get_attribute("href") or ""
        title = a.get_attribute("aria-label") or safe_text(a)
        if not href or href in seen or not title:
            continue
        seen.add(href)

        # try to find surrounding metadata within the card
        card = a.find_element(By.XPATH, "./ancestor::div[contains(@data-e2e,'SearchCard')] | ./ancestor::li[1] | ./ancestor::div[1]")
        instructor = ""
        outcomes = ""
        time_info = ""
        try:
            # Coursera often has partner/instructor under subtitle or partner tag
            instructor_el = card.find_element(By.XPATH, ".//*[contains(@data-e2e,'ProductCard-instructor')] | .//*[contains(text(),'by ')]")
            instructor = safe_text(instructor_el)
        except Exception:
            pass
        try:
            outcomes_el = card.find_element(By.XPATH, ".//*[contains(@data-e2e,'ProductCard-description')] | .//p")
            outcomes = safe_text(outcomes_el)
        except Exception:
            pass
        try:
            time_el = card.find_element(By.XPATH, ".//*[contains(text(),'weeks') or contains(text(),'hours') or contains(text(),'Self-paced') or contains(text(),'months')]")
            time_info = safe_text(time_el)
        except Exception:
            pass

        learning_mode = "Self-paced" if re.search(r"Self-paced|Flexible", f"{time_info} {outcomes}", re.I) else "Unknown"

        courses.append(Course(
            platform="Coursera",
            course_name=title,
            instructor=instructor,
            time_info=time_info,
            outcomes=outcomes,
            course_link=href,
            learning_mode=learning_mode,
        ))
    return courses


# ----------------------- edX -----------------------

def scrape_edx(driver: webdriver.Chrome, query: str, limit: int) -> List[Course]:
    courses: List[Course] = []
    search_url = f"https://www.edx.org/search?q={query.replace(' ', '%20')}"
    driver.get(search_url)

    try:
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "main"))
        )
    except TimeoutException:
        pass

    scroll_to_load(driver, max_scrolls=10)

    # edX card links often contain /course/ or /xseries/ or /professional-certificate/
    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/course/'], a[href*='/professional-certificate/'], a[href*='/program/']")

    seen = set()
    for a in links:
        if len(courses) >= limit:
            break
        href = a.get_attribute("href") or ""
        title = a.get_attribute("aria-label") or safe_text(a)
        if not href or href in seen or not title:
            continue
        seen.add(href)

        card = a.find_element(By.XPATH, "./ancestor::article[1] | ./ancestor::li[1] | ./ancestor::div[1]")
        instructor = ""
        outcomes = ""
        time_info = ""
        try:
            instructor_el = card.find_element(By.XPATH, ".//*[contains(text(),'Instructor') or contains(@class,'instructor') or contains(@class,'provider')]")
            instructor = safe_text(instructor_el)
        except Exception:
            pass
        try:
            outcomes_el = card.find_element(By.XPATH, ".//p | .//*[contains(@class,'description')]")
            outcomes = safe_text(outcomes_el)
        except Exception:
            pass
        try:
            time_el = card.find_element(By.XPATH, ".//*[contains(text(),'weeks') or contains(text(),'hours per') or contains(text(),'Self-Paced') or contains(text(),'Paced')]")
            time_info = safe_text(time_el)
        except Exception:
            pass

        learning_mode = "Self-paced" if re.search(r"Self|Paced|self-paced", f"{time_info} {outcomes}", re.I) else "Unknown"

        courses.append(Course(
            platform="edX",
            course_name=title,
            instructor=instructor,
            time_info=time_info,
            outcomes=outcomes,
            course_link=href,
            learning_mode=learning_mode,
        ))
    return courses


# ----------------------- DataCamp -----------------------

def scrape_datacamp(driver: webdriver.Chrome, query: str, limit: int) -> List[Course]:
    courses: List[Course] = []
    search_url = f"https://www.datacamp.com/search?q={query.replace(' ', '%20')}"
    driver.get(search_url)

    try:
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "main"))
        )
    except TimeoutException:
        pass

    scroll_to_load(driver, max_scrolls=10)

    # DataCamp course links usually contain /courses/ and projects contain /projects/
    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/courses/'], a[href*='/tracks/'], a[href*='/skills/']")

    seen = set()
    for a in links:
        if len(courses) >= limit:
            break
        href = a.get_attribute("href") or ""
        title = a.get_attribute("aria-label") or safe_text(a)
        if not href or href in seen or not title:
            continue
        seen.add(href)

        card = a.find_element(By.XPATH, "./ancestor::article[1] | ./ancestor::li[1] | ./ancestor::div[1]")
        instructor = ""
        outcomes = ""
        time_info = ""
        try:
            instructor_el = card.find_element(By.XPATH, ".//*[contains(text(),'Instructor') or contains(text(),'by ')]")
            instructor = safe_text(instructor_el)
        except Exception:
            pass
        try:
            outcomes_el = card.find_element(By.XPATH, ".//p | .//*[contains(@class,'description')]")
            outcomes = safe_text(outcomes_el)
        except Exception:
            pass
        try:
            time_el = card.find_element(By.XPATH, ".//*[contains(text(),'hours') or contains(text(),'chapters') or contains(text(),'exercise')]")
            time_info = safe_text(time_el)
        except Exception:
            pass

        learning_mode = "Self-paced"

        courses.append(Course(
            platform="DataCamp",
            course_name=title,
            instructor=instructor,
            time_info=time_info,
            outcomes=outcomes,
            course_link=href,
            learning_mode=learning_mode,
        ))
    return courses


# ----------------------- Orchestrator -----------------------

def run(query: str, per_site: int, headless: bool, out_csv: str):
    driver = make_driver(headless=headless)
    all_courses: List[Course] = []
    try:
        print(f"Scraping Edumall for '{query}'...")
        all_courses.extend(scrape_edumall(driver, query, per_site))
    except Exception as e:
        print("[WARN] Edumall scraping failed:", e)

    try:
        print(f"Scraping Coursera for '{query}'...")
        all_courses.extend(scrape_coursera(driver, query, per_site))
    except Exception as e:
        print("[WARN] Coursera scraping failed:", e)

    try:
        print(f"Scraping edX for '{query}'...")
        all_courses.extend(scrape_edx(driver, query, per_site))
    except Exception as e:
        print("[WARN] edX scraping failed:", e)

    try:
        print(f"Scraping DataCamp for '{query}'...")
        all_courses.extend(scrape_datacamp(driver, query, per_site))
    except Exception as e:
        print("[WARN] DataCamp scraping failed:", e)

    driver.quit()

    # Deduplicate by link
    dedup = {}
    for c in all_courses:
        if c.course_link not in dedup:
            dedup[c.course_link] = c

    df = pd.DataFrame([asdict(c) for c in dedup.values()])
    # Reorder columns
    cols = [
        "platform",
        "course_name",
        "instructor",
        "time_info",
        "outcomes",
        "course_link",
        "learning_mode",
    ]
    df = df.reindex(columns=cols)
    df.to_csv(out_csv, index=False)
    print(f"Saved {len(df)} courses to {out_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape IT courses from multiple platforms with Selenium.")
    parser.add_argument("--query", default="information technology", help="Search query keyword(s)")
    parser.add_argument("--per-site", type=int, default=40, help="Max items per platform")
    parser.add_argument("--out", default="it_courses.csv", help="Output CSV path")
    parser.add_argument("--headless", action="store_true", help="Run Chrome in headless mode")
    args = parser.parse_args()

    run(query=args.query, per_site=args.per_site, headless=args.headless, out_csv=args.out)
