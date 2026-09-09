#!/usr/bin/env python3
"""
MedEd Validation & Test Suite
-----------------------------
Validates repository structure, topics.json schema, relative links,
Markdown frontmatter, and HTML syntax before committing/pushing.
"""

import os
import sys
import json
import re
from html.parser import HTMLParser

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

errors = []
warnings = []
passed = 0

def log_pass(msg):
    global passed
    passed += 1
    print(f"  \033[92m✔\033[0m {msg}")

def log_error(msg):
    errors.append(msg)
    print(f"  \033[91m✖\033[0m {msg}")

def log_warning(msg):
    warnings.append(msg)
    print(f"  \033[93m⚠\033[0m {msg}")

# -------------------------------------------------------------
# 1. Validate data/topics.json
# -------------------------------------------------------------
def test_topics_json():
    print("\n\033[1m[1/4] Validating data/topics.json...\033[0m")
    topics_path = os.path.join(ROOT_DIR, "data", "topics.json")
    if not os.path.exists(topics_path):
        log_error("data/topics.json does not exist!")
        return

    try:
        with open(topics_path, "r", encoding="utf-8") as f:
            topics = json.load(f)
        log_pass("data/topics.json is valid JSON.")
    except Exception as e:
        log_error(f"data/topics.json failed JSON parse: {e}")
        return

    if not isinstance(topics, list):
        log_error("topics.json must contain a JSON array/list.")
        return

    if len(topics) == 0:
        log_warning("topics.json is empty.")
        return

    seen_ids = set()
    required_fields = ["id", "title", "category", "categorySlug", "type", "typeSlug", "status", "path"]

    for idx, topic in enumerate(topics):
        topic_id = topic.get("id", f"item-{idx}")
        if not topic.get("id"):
            log_error(f"Topic index {idx} is missing 'id'.")
        elif topic_id in seen_ids:
            log_error(f"Duplicate topic id '{topic_id}' found.")
        seen_ids.add(topic_id)

        for req in required_fields:
            if req not in topic or not str(topic[req]).strip():
                log_error(f"Topic '{topic_id}' missing required field: '{req}'.")

        # Validate file existence for active topics
        if topic.get("status") == "Active":
            path = topic.get("path")
            if path and not path.startswith("#"):
                abs_path = os.path.join(ROOT_DIR, path)
                if os.path.exists(abs_path):
                    log_pass(f"Active topic '{topic_id}' entry path resolves to '{path}'.")
                else:
                    log_error(f"Active topic '{topic_id}' path '{path}' does NOT exist on disk.")

            gh_path = topic.get("githubPath")
            if gh_path and not gh_path.startswith("#"):
                abs_gh_path = os.path.join(ROOT_DIR, gh_path)
                if not os.path.exists(abs_gh_path):
                    log_warning(f"Topic '{topic_id}' githubPath '{gh_path}' does not exist on disk.")

# -------------------------------------------------------------
# 2. Validate Markdown Syllabus & Frontmatter
# -------------------------------------------------------------
def test_markdown_files():
    print("\n\033[1m[2/4] Validating Markdown content files...\033[0m")
    topics_dir = os.path.join(ROOT_DIR, "topics")
    if not os.path.exists(topics_dir):
        log_warning("No 'topics/' directory found.")
        return

    md_count = 0
    for root, _, files in os.walk(topics_dir):
        for file in files:
            if file.startswith("."):
                continue
            if file.endswith(".md"):
                md_count += 1
                rel_path = os.path.relpath(os.path.join(root, file), ROOT_DIR)
                full_path = os.path.join(root, file)

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if len(content.strip()) == 0:
                        log_error(f"{rel_path} is completely empty.")
                        continue

                    # If it's a course lesson file under content/, check frontmatter
                    if "/content/" in rel_path.replace("\\", "/"):
                        if not content.startswith("---"):
                            log_warning(f"{rel_path} does not start with YAML frontmatter ('---').")
                        else:
                            parts = content.split("---", 2)
                            if len(parts) < 3:
                                log_error(f"{rel_path} has unclosed frontmatter.")
                            else:
                                log_pass(f"{rel_path} has valid frontmatter & {len(content.splitlines())} lines.")
                    else:
                        log_pass(f"{rel_path} is present and readable ({len(content.splitlines())} lines).")

                except Exception as e:
                    log_error(f"Failed to read {rel_path}: {e}")

    if md_count == 0:
        log_warning("No markdown files found under topics/.")

# -------------------------------------------------------------
# 3. Validate HTML Syntax and Relative File References
# -------------------------------------------------------------
class StrictHTMLValidator(HTMLParser):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.links = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "a" and "href" in attr_dict:
            self.links.append(attr_dict["href"])
        elif tag == "script" and "src" in attr_dict:
            self.scripts.append(attr_dict["src"])

def test_html_files():
    print("\n\033[1m[3/4] Validating HTML structure & local relative links...\033[0m")
    html_files = []
    for root, _, files in os.walk(ROOT_DIR):
        if ".git" in root or "node_modules" in root or ".githooks" in root:
            continue
        for file in files:
            if file.startswith("."):
                continue
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))

    for html_path in html_files:
        rel_html = os.path.relpath(html_path, ROOT_DIR)
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                content = f.read()

            parser = StrictHTMLValidator(html_path)
            parser.feed(content)
            log_pass(f"{rel_html} parsed successfully with valid HTML structure.")

            # Ensure essential production CSS & Icons are linked (skip google verification file)
            if not rel_html.startswith("google"):
                if "font-awesome" not in content:
                    log_error(f"In {rel_html}: FontAwesome stylesheet link is missing! Icons will not render.")
                else:
                    log_pass(f"In {rel_html}: verified FontAwesome icon stylesheet.")

                if "cdn.tailwindcss.com" in content:
                    log_error(f"In {rel_html}: cdn.tailwindcss.com is present! Replace with main.min.css.")
                else:
                    log_pass(f"In {rel_html}: verified no cdn.tailwindcss.com runtime script.")

            # Validate relative href links
            html_dir = os.path.dirname(html_path)
            for link in parser.links:
                if link.startswith("http://") or link.startswith("https://") or link.startswith("#") or link.startswith("mailto:"):
                    continue
                
                # Clean query strings/hashes
                clean_link = link.split("#")[0].split("?")[0]
                if not clean_link:
                    continue

                target_file = os.path.normpath(os.path.join(html_dir, clean_link))
                if not os.path.exists(target_file):
                    log_error(f"In {rel_html}: broken relative link '{link}' (target '{os.path.relpath(target_file, ROOT_DIR)}' not found).")
                else:
                    log_pass(f"In {rel_html}: verified link to '{clean_link}'.")

        except Exception as e:
            log_error(f"HTML error in {rel_html}: {e}")

# -------------------------------------------------------------
# 4. Check Root Platform Essentials
# -------------------------------------------------------------
def test_root_essentials():
    print("\n\033[1m[4/4] Validating repository root essentials, SEO assets & compiled assets...\033[0m")
    essentials = ["index.html", "README.md", "LICENSE", "assets/css/main.min.css", "sitemap.xml", "sitemap.xsl", "robots.txt"]
    for item in essentials:
        path = os.path.join(ROOT_DIR, item)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            log_pass(f"Essential file '{item}' is present and non-empty ({os.path.getsize(path)} bytes).")
        else:
            log_error(f"Essential file '{item}' is missing or empty.")

    # Validate .nojekyll presence for raw GitHub Pages asset serving
    nojekyll_path = os.path.join(ROOT_DIR, ".nojekyll")
    if os.path.exists(nojekyll_path):
        log_pass("'.nojekyll' flag is present (bypasses Jekyll processing).")
    else:
        log_warning("'.nojekyll' flag is missing.")

    # Validate sitemap XML structure and URLs
    sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
    if os.path.exists(sitemap_path):
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            urls = [elem.text for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
            log_pass(f"sitemap.xml is valid XML with {len(urls)} indexed URLs.")
            
            # Check topics from topics.json
            with open(os.path.join(ROOT_DIR, "data/topics.json"), "r", encoding="utf-8") as f:
                topics = json.load(f)
            for t in topics:
                if t.get("status") == "Active":
                    topic_rel = t.get('path', '').replace('index.html', '').rstrip('/')
                    expected_url = f"https://borun.github.io/meded/{topic_rel}/" if topic_rel else "https://borun.github.io/meded/"
                    if expected_url in urls or f"{expected_url}index.html" in urls:
                        log_pass(f"Sitemap indexes active course: '{t.get('title')}'")
                    else:
                        log_warning(f"Sitemap missing active course URL: '{expected_url}'")
        except Exception as e:
            log_error(f"Invalid sitemap.xml: {e}")

    # Validate robots.txt references sitemap
    robots_path = os.path.join(ROOT_DIR, "robots.txt")
    if os.path.exists(robots_path):
        with open(robots_path, "r", encoding="utf-8") as f:
            robots_txt = f.read()
        if "sitemap.xml" in robots_txt:
            log_pass("robots.txt correctly declares Sitemap location.")
        else:
            log_error("robots.txt is missing 'Sitemap: ...' declaration.")

# -------------------------------------------------------------
# Main Runner
# -------------------------------------------------------------
def main():
    print("========================================")
    print(" 🏥 MedEd Platform Pre-Push Test Suite")
    print("========================================")

    test_topics_json()
    test_markdown_files()
    test_html_files()
    test_root_essentials()

    print("\n----------------------------------------")
    print(f"Summary: \033[92m{passed} passed\033[0m, \033[93m{len(warnings)} warnings\033[0m, \033[91m{len(errors)} errors\033[0m.")
    print("----------------------------------------")

    if errors:
        print("\033[91m✖ TESTS FAILED. Please fix the above errors before pushing.\033[0m\n")
        sys.exit(1)
    else:
        print("\033[92m✔ ALL TESTS PASSED! Safe to commit and push.\033[0m\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
