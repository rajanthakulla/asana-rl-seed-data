"""
Data sources and external data reference module.

This module documents the external data sources used for generating realistic
seed data for the Asana RL environment. While the actual implementation uses
heuristic patterns and hardcoded data, this module provides references to
the real-world sources that informed the data generation strategies.
"""

# Company Data Sources
COMPANY_DATA_SOURCES = {
    "Fortune 500 Companies": "https://www.forbes.com/global2000/",
    "Y Combinator Companies": "https://www.ycombinator.com/companies",
    "Tech Companies": "https://www.techcrunch.com",
    "Crunchbase": "https://www.crunchbase.com",
}

# User Demographics Sources
USER_DEMOGRAPHICS_SOURCES = {
    "US Census Bureau": "https://www.census.gov/topics/population/data.html",
    "Social Security Administration": "https://www.ssa.gov/oact/babynames/",
    "Kaggle Datasets": "https://www.kaggle.com/datasets/",
}

# Project Management Patterns
PROJECT_PATTERN_SOURCES = {
    "Asana Templates": "https://asana.com/templates",
    "GitHub Projects": "https://github.com/",
    "ProductHunt": "https://www.producthunt.com",
}

# Task Management Research
TASK_MANAGEMENT_SOURCES = {
    "Asana Anatomy of Work Report": "https://asana.com/resources/anatomy-of-work",
    "GitHub Issues Database": "https://github.com/",
    "StackOverflow": "https://stackoverflow.com",
}

# Distribution Benchmarks
DISTRIBUTION_BENCHMARKS = {
    "Task Completion Rates": "Asana Anatomy of Work - Industry Reports",
    "Sprint Duration": "Agile/Scrum Best Practices",
    "Team Size Distribution": "Bureau of Labor Statistics",
    "Work Schedule Patterns": "Gallup Work Research",
}


def get_company_sources():
    """Returns list of company data sources."""
    return COMPANY_DATA_SOURCES


def get_user_sources():
    """Returns list of user demographic sources."""
    return USER_DEMOGRAPHICS_SOURCES


def get_project_sources():
    """Returns list of project pattern sources."""
    return PROJECT_PATTERN_SOURCES


def get_task_sources():
    """Returns list of task management sources."""
    return TASK_MANAGEMENT_SOURCES


def get_benchmark_sources():
    """Returns list of distribution benchmark sources."""
    return DISTRIBUTION_BENCHMARKS
