# Team data generation
import random
from datetime import datetime, timedelta
from typing import List
from models import Team, TeamMembership, User
from utils.helpers import generate_uuid

TEAM_TYPES = ['engineering', 'marketing', 'operations', 'sales', 'design', 'leadership', 'product', 'data']

TEAM_NAMES = {
    'engineering': [
        "Backend Platform", "Frontend Systems", "Mobile Team", "Infrastructure",
        "DevOps", "Full Stack", "API Team", "Core Platform", "Tools & Systems",
        "Cloud Engineering", "Performance", "Platform Engineering", "Data Infrastructure"
    ],
    'marketing': [
        "Demand Gen", "Product Marketing", "Content Marketing", "Brand & Design",
        "Growth Marketing", "Marketing Ops", "Digital Marketing", "Campaign Management"
    ],
    'operations': [
        "Finance", "Human Resources", "Legal & Compliance", "Facilities",
        "Business Operations", "IT Operations", "Admin", "People Operations"
    ],
    'sales': [
        "Enterprise Sales", "Mid-Market Sales", "Sales Development", "Account Management",
        "Customer Success", "Partnerships", "Sales Operations"
    ],
    'design': [
        "Product Design", "UX/UI", "Design Systems", "Brand Design", "Design Ops"
    ],
    'product': [
        "Product Management", "Product Analytics", "Product Operations"
    ],
    'data': [
        "Data Science", "Analytics", "Data Engineering", "BI", "Machine Learning"
    ],
    'leadership': [
        "Executive Team", "Leadership Council"
    ]
}

TEAM_DESCRIPTIONS = {
    'engineering': "Responsible for building and maintaining our core platform",
    'marketing': "Drives awareness and demand generation for our products",
    'operations': "Manages business operations and organizational effectiveness",
    'sales': "Drives revenue through customer acquisition and account management",
    'design': "Creates exceptional user experiences and visual design",
    'product': "Defines and manages product strategy and direction",
    'data': "Provides insights and analytics to drive decision-making",
    'leadership': "Company leadership and strategic direction"
}

def generate_team(
    org_id: str,
    team_index: int,
    team_type: str,
    base_datetime: datetime
) -> Team:
    """Generate a single realistic team"""
    team_id = generate_uuid()
    
    # Choose realistic name for team type
    team_names = TEAM_NAMES.get(team_type, TEAM_NAMES['engineering'])
    name = random.choice(team_names)
    
    description = TEAM_DESCRIPTIONS.get(team_type, "")
    
    # Team created shortly after organization
    days_ago = random.randint(10, 180)
    created_at = base_datetime - timedelta(days=days_ago)
    
    # Most teams are active
    is_active = random.random() < 0.95
    
    return Team(
        team_id=team_id,
        org_id=org_id,
        name=name,
        description=description,
        team_type=team_type,
        created_at=created_at,
        is_active=is_active
    )

def generate_teams(
    org_id: str,
    base_datetime: datetime = None
) -> List[Team]:
    """Generate teams for an organization"""
    if base_datetime is None:
        base_datetime = datetime.now()
    
    teams = []
    used_names = set()  # Track team names to avoid duplicates
    
    # Realistic organization structure
    # 1 leadership team
    team = generate_team(org_id, 0, 'leadership', base_datetime)
    while team.name in used_names:
        team = generate_team(org_id, 0, 'leadership', base_datetime)
    used_names.add(team.name)
    teams.append(team)
    
    # 2-3 engineering teams (large company)
    for i in range(random.randint(2, 3)):
        team = generate_team(org_id, len(teams), 'engineering', base_datetime)
        while team.name in used_names:
            team = generate_team(org_id, len(teams), 'engineering', base_datetime)
        used_names.add(team.name)
        teams.append(team)
    
    # 1-2 product teams
    for i in range(random.randint(1, 2)):
        team = generate_team(org_id, len(teams), 'product', base_datetime)
        while team.name in used_names:
            team = generate_team(org_id, len(teams), 'product', base_datetime)
        used_names.add(team.name)
        teams.append(team)
    
    # 1-2 design teams
    for i in range(random.randint(1, 2)):
        team = generate_team(org_id, len(teams), 'design', base_datetime)
        while team.name in used_names:
            team = generate_team(org_id, len(teams), 'design', base_datetime)
        used_names.add(team.name)
        teams.append(team)
    
    # 1-2 data teams
    for i in range(random.randint(1, 2)):
        team = generate_team(org_id, len(teams), 'data', base_datetime)
        while team.name in used_names:
            team = generate_team(org_id, len(teams), 'data', base_datetime)
        used_names.add(team.name)
        teams.append(team)
    
    # 2-3 marketing teams (multiple disciplines)
    for i in range(random.randint(2, 3)):
        team = generate_team(org_id, len(teams), 'marketing', base_datetime)
        while team.name in used_names:
            team = generate_team(org_id, len(teams), 'marketing', base_datetime)
        used_names.add(team.name)
        teams.append(team)
    
    # 2-3 sales teams
    for i in range(random.randint(2, 3)):
        team = generate_team(org_id, len(teams), 'sales', base_datetime)
        while team.name in used_names:
            team = generate_team(org_id, len(teams), 'sales', base_datetime)
        used_names.add(team.name)
        teams.append(team)
    
    # 1 operations team
    team = generate_team(org_id, len(teams), 'operations', base_datetime)
    while team.name in used_names:
        team = generate_team(org_id, len(teams), 'operations', base_datetime)
    used_names.add(team.name)
    teams.append(team)
    
    return teams

def generate_team_memberships(
    teams: List[Team],
    users: List[User],
    base_datetime: datetime = None
) -> List[TeamMembership]:
    """
    Generate realistic team memberships.
    Distribution: Most users in 1-2 teams, some in 3+ teams
    """
    if base_datetime is None:
        base_datetime = datetime.now()
    
    memberships = []
    user_team_count = {}  # Track how many teams each user is in
    
    for team in teams:
        team_size_range = {
            'leadership': (8, 12),
            'engineering': (15, 35),
            'product': (8, 15),
            'design': (5, 12),
            'data': (8, 15),
            'marketing': (10, 25),
            'sales': (15, 40),
            'operations': (10, 20)
        }
        
        min_size, max_size = team_size_range.get(team.team_type, (10, 20))
        team_size = random.randint(min_size, max_size)
        
        # Select users for this team
        # Prefer users not yet assigned or assigned to few teams
        available_users = [u for u in users if user_team_count.get(u.user_id, 0) < 3]
        
        if len(available_users) < team_size:
            available_users = users
        
        selected_users = random.sample(available_users, min(team_size, len(available_users)))
        
        for user in selected_users:
            membership_id = generate_uuid()
            
            # Chance of being a team lead (higher for senior roles)
            is_lead = False
            if user.role in ['lead', 'manager', 'director', 'executive']:
                is_lead = random.random() < 0.6
            elif user.seniority_level in ['senior', 'staff', 'principal']:
                is_lead = random.random() < 0.2
            
            role_in_team = 'lead' if is_lead else 'member'
            
            # Joined shortly after team creation
            days_since_team_creation = (base_datetime - team.created_at).days
            days_ago = random.randint(0, max(1, days_since_team_creation - 5))
            joined_at = base_datetime - timedelta(days=days_ago)
            
            memberships.append(TeamMembership(
                membership_id=membership_id,
                team_id=team.team_id,
                user_id=user.user_id,
                joined_at=joined_at,
                is_lead=is_lead,
                role_in_team=role_in_team
            ))
            
            user_team_count[user.user_id] = user_team_count.get(user.user_id, 0) + 1
    
    return memberships
