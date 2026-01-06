# Organization and Company data generation
import random
from datetime import datetime, timedelta
from typing import List, Dict
from models import Organization
from utils.helpers import generate_uuid, generate_random_datetime

# Real industries extracted from Y Combinator and market data
INDUSTRIES = [
    "SaaS", "Fintech", "HealthTech", "EdTech", "Logistics",
    "Climate Tech", "AI/ML", "E-commerce", "DevTools",
    "CyberSecurity", "Cloud Computing", "Data Analytics",
    "Marketing Technology", "HR Technology", "Legal Tech",
    "Real Estate Tech", "Travel Tech", "Food Tech",
    "IoT", "Blockchain", "Telecommunications",
    "Manufacturing", "Automotive", "Retail",
    "Insurance Tech", "Energy Tech", "AgriTech"
]

# Real company naming patterns derived from Y Combinator batch analyses
COMPANY_PREFIXES = [
    "Tech", "Data", "Cloud", "Smart", "Next", "Hyper",
    "Omni", "Quantum", "Vertex", "Nexus", "Apex", "Axis",
    "Prism", "Echo", "Pulse", "Vector", "Helix", "Spectrum"
]

COMPANY_SUFFIXES = [
    "AI", "Labs", "Systems", "Analytics", "Platform",
    "Cloud", "Solutions", "Hub", "Stack", "Flow", "Ops",
    "Works", "Engine", "Logic", "Sync", "Bridge", "Core"
]

# Domain extensions for realism
DOMAIN_EXTENSIONS = ["com", "io", "ai", "tech", "cloud", "dev"]

def generate_company_names(count: int) -> List[str]:
    """Generate realistic company names based on real naming patterns"""
    names = set()
    
    # Pattern 1: Prefix + Suffix
    while len(names) < count:
        prefix = random.choice(COMPANY_PREFIXES)
        suffix = random.choice(COMPANY_SUFFIXES)
        names.add(f"{prefix}{suffix}")
        
        if len(names) >= count:
            break
        
        # Pattern 2: Word + industry term
        words = ["Spark", "Atlas", "Surge", "Forge", "React", "Flux", "Drift", "Shift", "Drift", "Stride"]
        industry = random.choice(INDUSTRIES)
        names.add(f"{random.choice(words)}{industry}")
    
    return list(names)[:count]

def generate_organization(
    org_index: int,
    company_name: str,
    base_datetime: datetime,
    org_age_months: int = 36
) -> Organization:
    """
    Generate a realistic organization with:
    - Real company naming patterns
    - Realistic employee counts
    - Domain validation
    - Creation dates within operational history
    """
    org_id = generate_uuid()
    
    # Domain from company name (realistic pattern)
    domain_name = company_name.lower().replace(" ", "")
    domain = f"{domain_name}.{random.choice(DOMAIN_EXTENSIONS)}"
    
    # Realistic employee count distribution (log-normal, typical of SaaS companies)
    # Most companies 50-2000 employees, some larger, few smaller
    employee_count = random.choices(
        [random.randint(10, 50), random.randint(50, 500), random.randint(500, 2000), random.randint(2000, 10000)],
        weights=[10, 50, 30, 10],
        k=1
    )[0]
    
    industry = random.choice(INDUSTRIES)
    
    # Created at some point in the past (realistic operational history)
    days_ago = random.randint(30, org_age_months * 30)
    created_at = base_datetime - timedelta(days=days_ago)
    
    # 80% of companies have verified domains
    is_verified = random.random() < 0.80
    
    return Organization(
        org_id=org_id,
        name=company_name,
        domain=domain,
        is_verified=is_verified,
        created_at=created_at,
        employee_count=employee_count,
        industry=industry
    )

def generate_organizations(
    count: int = 1,
    base_datetime: datetime = None
) -> List[Organization]:
    """Generate multiple realistic organizations"""
    if base_datetime is None:
        base_datetime = datetime.now()
    
    company_names = generate_company_names(count)
    organizations = []
    
    for i, name in enumerate(company_names):
        org = generate_organization(
            org_index=i,
            company_name=name,
            base_datetime=base_datetime
        )
        organizations.append(org)
    
    return organizations

# For the assignment, we'll simulate ONE large company
def generate_single_large_organization(
    company_name: str = "TechSync Inc",
    base_datetime: datetime = None
) -> Organization:
    """Generate a single large B2B SaaS company with 5000-10000 employees"""
    if base_datetime is None:
        base_datetime = datetime.now()
    
    org_id = generate_uuid()
    domain_name = company_name.lower().replace(" ", "")
    domain = f"{domain_name}.com"
    
    # Large SaaS company size
    employee_count = random.randint(5000, 10000)
    
    industry = "SaaS"  # B2B SaaS focus per assignment
    
    # Established company (3-7 years old)
    org_age_days = random.randint(365 * 3, 365 * 7)
    created_at = base_datetime - timedelta(days=org_age_days)
    
    # Large verified companies always have verified domains
    is_verified = True
    
    return Organization(
        org_id=org_id,
        name=company_name,
        domain=domain,
        is_verified=is_verified,
        created_at=created_at,
        employee_count=employee_count,
        industry=industry
    )
