# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines constants."""

import os

import dotenv

dotenv.load_dotenv()

AGENT_NAME = "dev_news_agent"

MODEL = os.getenv("MODEL", "gemini-2.5-flash-lite")

# Browser configuration
DISABLE_WEB_DRIVER = int(os.getenv("DISABLE_WEB_DRIVER", "0"))
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true").lower() == "true"
BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30000"))  # 30 seconds

# News sources configuration
NEWS_SOURCES = {
    "techcrunch": {
        "url": "https://techcrunch.com",
        "search_url": "https://techcrunch.com/search/{query}",
        "article_selectors": {
            "title": "h2 a, h3 a, .post-block__title a",
            "link": "h2 a, h3 a, .post-block__title a",
            "date": "time, .post-block__time",
            "description": "p, .post-block__content p"
        }
    },
    "google": {
        "url": "https://google.com",
        "search_url": "https://google.com/search?q={query}",
        "article_selectors": {
            "title": "h2 a, h3 a, .post-block__title a",
            "link": "h2 a, h3 a, .post-block__title a",
            "date": "time, .post-block__time",
            "description": "p, .post-block__content p"
        }
    },
    "theverge": {
        "url": "https://www.theverge.com",
        "search_url": "https://www.theverge.com/search?q={query}",
        "article_selectors": {
            "title": "h2 a, h3 a, .c-entry-box--compact__title a",
            "link": "h2 a, h3 a, .c-entry-box--compact__title a",
            "date": "time, .c-byline__item",
            "description": "p, .c-entry-summary"
        }
    },
    "venturebeat": {
        "url": "https://venturebeat.com",
        "search_url": "https://venturebeat.com/?s={query}",
        "article_selectors": {
            "title": "h2 a, h3 a, .Article__title a",
            "link": "h2 a, h3 a, .Article__title a",
            "date": "time, .Article__date",
            "description": "p, .Article__excerpt p"
        }
    }
}

# Content type mapping for step identification
CONTENT_TYPES = {
    "announcement": ["announce", "release", "launch", "introducing"],
    "documentation": ["docs", "documentation", "api", "guide", "tutorial"],
    "implementation": ["code", "example", "implementation", "demo"],
    "discussion": ["discussion", "community", "feedback", "forum"],
    "education": ["tutorial", "learn", "guide", "how-to"],
    "application": ["app", "application", "use case", "production"]
}