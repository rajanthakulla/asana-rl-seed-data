# Project data generation based on real Asana/GitHub/ProductHunt patterns
import random
from datetime import datetime, timedelta, date
from typing import List
from models import Project, Section
from utils.helpers import generate_uuid

# Real project naming patterns from:
# 1. Public Asana templates
# 2. GitHub organization boards
# 3. ProductHunt launches

ENGINEERING_PROJECT_NAMES = [
    "Platform Core Redesign", "API v2 Migration", "Mobile App Launch",
    "Performance Optimization Q1", "Infrastructure Modernization",
    "Authentication Refactor", "Database Optimization", "DevOps Automation",
    "Cloud Migration", "Microservices Architecture", "GraphQL Implementation",
    "Search Engine Upgrade", "Payment Integration", "Analytics Pipeline",
    "Real-time Notifications", "CI/CD Pipeline Enhancement", "Security Hardening",
    "Accessibility Compliance", "Documentation Overhaul", "Testing Framework Upgrade"
]

MARKETING_PROJECT_NAMES = [
    "Q1 2025 Campaign Launch", "Content Marketing Strategy",
    "Social Media Revamp", "Email Marketing Campaign",
    "Website Redesign", "Brand Guidelines Update", "Influencer Partnerships",
    "Product Launch Campaign", "Customer Success Stories", "Webinar Series",
    "Case Study Development", "Marketing Automation Setup", "Video Content Series",
    "Blog Content Calendar", "Event Marketing Q1"
]

OPERATIONS_PROJECT_NAMES = [
    "Company Restructuring", "Office Expansion", "Process Automation",
    "Finance System Upgrade", "HR System Implementation", "Compliance Audit",
    "Vendor Management", "Contract Renewal", "Security Assessment",
    "Disaster Recovery Plan", "Budget Planning 2025"
]

PRODUCT_PROJECT_NAMES = [
    "Feature: Advanced Filters", "Feature: Real-time Collaboration",
    "Feature: Custom Workflows", "Roadmap Planning Q2",
    "User Research Sprint", "Competitive Analysis", "Market Research",
    "Product Strategy Alignment", "Beta Program Launch"
]

PROJECT_NAMES_BY_TYPE = {
    'product_development': ENGINEERING_PROJECT_NAMES,
    'marketing_campaign': MARKETING_PROJECT_NAMES,
    'operations': OPERATIONS_PROJECT_NAMES,
    'infrastructure': ["Kubernetes Migration", "Cloud Infrastructure", "DR Setup"],
    'product': PRODUCT_PROJECT_NAMES
}

# Standard sections/columns in Asana (realistic workflow)
PROJECT_SECTIONS = {
    'product_development': ["Backlog", "In Progress", "In Review", "Testing", "Deployed"],
    'marketing_campaign': ["Planning", "In Progress", "Review", "Scheduled", "Published"],
    'operations': ["To Do", "In Progress", "Completed"],
    'infrastructure': ["Backlog", "In Progress", "Testing", "Deployed"],
    'product': ["Discovery", "Scoping", "In Progress", "Done"]
}

PROJECT_DESCRIPTIONS = {
    'product_development': "Core platform and feature development initiative",
    'marketing_campaign': "Marketing campaign and awareness initiative",
    'operations': "Operational and organizational initiative",
    'infrastructure': "Infrastructure and systems initiative",
    'product': "Product strategy and planning initiative"
}

def generate_project(
    org_id: str,
    team_id: str,
    owner_user_id: str,
    project_type: str,
    project_index: int,
    base_datetime: datetime
) -> Project:
    """Generate a single realistic project"""
    project_id = generate_uuid()
    
    # Choose realistic name
    names = PROJECT_NAMES_BY_TYPE.get(project_type, ENGINEERING_PROJECT_NAMES)
    name = random.choice(names)
    
    # Add uniqueness by appending initiative name or quarter
    if random.random() < 0.3:
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        years = [2024, 2025]
        name = f"{name} {random.choice(quarters)} {random.choice(years)}"
    
    description = PROJECT_DESCRIPTIONS.get(project_type, "")
    
    # Project created at some point in the past (realistic timeline)
    days_ago = random.randint(10, 365)
    created_at = base_datetime - timedelta(days=days_ago)
    
    # Start date typically at or after creation
    start_date = (created_at + timedelta(days=random.randint(0, 10))).date()
    
    # Target end date (realistic project duration)
    # Most projects: 3-6 months
    duration_days = random.randint(30, 180)
    target_end_date = start_date + timedelta(days=duration_days)
    
    # Status distribution: 70% active, 20% archived, 10% completed
    rand = random.random()
    if rand < 0.10:
        status = 'completed'
        # Completed projects must have end date in past
        target_end_date = (base_datetime - timedelta(days=random.randint(1, 100))).date()
    elif rand < 0.30:
        status = 'archived'
    else:
        status = 'active'
    
    return Project(
        project_id=project_id,
        org_id=org_id,
        team_id=team_id,
        name=name,
        description=description,
        project_type=project_type,
        status=status,
        created_at=created_at,
        start_date=start_date,
        target_end_date=target_end_date,
        owner_user_id=owner_user_id,
        visibility='team'
    )

def generate_projects(
    org_id: str,
    teams: List,
    users: List,
    base_datetime: datetime = None,
    projects_per_team: int = 3
) -> List[Project]:
    """Generate projects for teams in an organization"""
    if base_datetime is None:
        base_datetime = datetime.now()
    
    projects = []
    used_names = set()  # Track project names to avoid duplicates
    
    for team in teams:
        # Skip leadership team
        if team.team_type == 'leadership':
            continue
        
        # Projects per team varies
        num_projects = random.randint(max(1, projects_per_team - 1), projects_per_team + 2)
        
        # Determine project types based on team type
        if team.team_type == 'engineering':
            project_types = ['product_development', 'infrastructure']
        elif team.team_type == 'marketing':
            project_types = ['marketing_campaign']
        elif team.team_type == 'operations':
            project_types = ['operations']
        elif team.team_type == 'product':
            project_types = ['product']
        else:
            project_types = ['product_development', 'operations']
        
        for i in range(num_projects):
            project_type = random.choice(project_types)
            
            # Select owner from team (prefer leads/managers)
            owner = random.choice(users)
            
            # Ensure unique project name
            project = generate_project(
                org_id=org_id,
                team_id=team.team_id,
                owner_user_id=owner.user_id,
                project_type=project_type,
                project_index=len(projects),
                base_datetime=base_datetime
            )
            
            while project.name in used_names:
                project = generate_project(
                    org_id=org_id,
                    team_id=team.team_id,
                    owner_user_id=owner.user_id,
                    project_type=project_type,
                    project_index=len(projects),
                    base_datetime=base_datetime
                )
            
            used_names.add(project.name)
            projects.append(project)
    
    return projects

def generate_sections(
    project_id: str,
    project_type: str,
    created_at: datetime
) -> List[Section]:
    """Generate sections (columns) for a project"""
    section_names = PROJECT_SECTIONS.get(project_type, ["To Do", "In Progress", "Done"])
    sections = []
    
    for order, name in enumerate(section_names):
        section_id = generate_uuid()
        section = Section(
            section_id=section_id,
            project_id=project_id,
            name=name,
            description=f"Section for {name} status",
            display_order=order,
            created_at=created_at
        )
        sections.append(section)
    
    return sections

def generate_all_sections(
    projects: List[Project],
    base_datetime: datetime = None
) -> List[Section]:
    """Generate sections for all projects"""
    if base_datetime is None:
        base_datetime = datetime.now()
    
    sections = []
    for project in projects:
        project_sections = generate_sections(
            project.project_id,
            project.project_type,
            project.created_at
        )
        sections.extend(project_sections)
    
    return sections
