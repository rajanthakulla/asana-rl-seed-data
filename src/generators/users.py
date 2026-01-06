# User data generation with realistic demographics
import random
from datetime import datetime, timedelta
from typing import List, Tuple
from models import User
from utils.helpers import generate_uuid, generate_email

# Realistic first names reflecting diverse workforce (top names from census data)
FIRST_NAMES_MALE = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Mark", "Donald",
    "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian", "George",
    "Edward", "Ronald", "Anthony", "Frank", "Ryan", "Gary", "Nicholas", "Eric",
    "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel",
    "Alexander", "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose"
]

FIRST_NAMES_FEMALE = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
    "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Margaret", "Sandra",
    "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Melissa", "Deborah",
    "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Kathleen", "Amy",
    "Angela", "Shirley", "Anna", "Brenda", "Pamela", "Emma", "Nicole", "Helen",
    "Samantha", "Katherine", "Christine", "Debra", "Rachel", "Catherine", "Carolyn",
    "Janet", "Maria", "Heather", "Diane"
]

# Realistic last names (diverse, from census data)
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Peterson", "Phillips", "Campbell", "Parker",
    "Evans", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales",
    "Murphy", "Cook", "Rogers", "Ortiz", "Morgan", "Peterson", "Cooper",
    "Peterson", "Brady", "Holley", "Maldonado", "Tate", "Lamb", "Ruiz"
]

# Job titles reflecting realistic org structure
INDIVIDUAL_CONTRIBUTOR_TITLES = [
    "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Data Scientist", "Data Analyst", "Product Manager", "Product Designer",
    "UX Designer", "UI Designer", "Marketing Manager", "Content Strategist",
    "Customer Success Manager", "Sales Representative", "Operations Associate",
    "Finance Analyst", "Business Analyst", "Solutions Architect", "DevOps Engineer",
    "ML Engineer", "Infrastructure Engineer", "Security Engineer", "QA Engineer",
    "Technical Writer", "Copywriter", "Graphic Designer", "Brand Manager",
    "Community Manager", "Growth Manager", "Research Manager"
]

LEAD_TITLES = [
    "Engineering Lead", "Product Lead", "Design Lead", "Marketing Lead",
    "Data Lead", "Operations Lead", "Analytics Lead", "Security Lead",
    "Platform Lead", "Infrastructure Lead"
]

MANAGER_TITLES = [
    "Engineering Manager", "Product Manager", "Design Manager", "Marketing Manager",
    "Operations Manager", "Finance Manager", "Sales Manager", "HR Manager",
    "Customer Success Manager", "Data Manager"
]

DIRECTOR_TITLES = [
    "Director of Engineering", "Director of Product", "Director of Design",
    "Director of Marketing", "VP of Operations", "VP of Sales", "VP of Finance",
    "Director of HR", "Director of Operations"
]

EXECUTIVE_TITLES = [
    "CEO", "CTO", "COO", "CFO", "CMO", "VP Product", "VP Engineering",
    "VP Marketing", "VP Sales", "SVP Operations", "Chief Product Officer"
]

SENIORITY_WEIGHTS = {
    'intern': 5,
    'junior': 30,
    'mid': 40,
    'senior': 20,
    'staff': 4,
    'principal': 1
}

ROLE_WEIGHTS = {
    'individual_contributor': 70,
    'lead': 15,
    'manager': 10,
    'director': 4,
    'executive': 1
}

def choose_title(role: str, seniority: str) -> str:
    """Choose a realistic job title based on role and seniority"""
    if role == 'executive':
        return random.choice(EXECUTIVE_TITLES)
    elif role == 'director':
        return random.choice(DIRECTOR_TITLES)
    elif role == 'manager':
        return random.choice(MANAGER_TITLES)
    elif role == 'lead':
        return random.choice(LEAD_TITLES)
    else:  # individual_contributor
        return random.choice(INDIVIDUAL_CONTRIBUTOR_TITLES)

def choose_seniority() -> str:
    """Choose seniority level with realistic distribution"""
    return random.choices(
        list(SENIORITY_WEIGHTS.keys()),
        weights=list(SENIORITY_WEIGHTS.values()),
        k=1
    )[0]

def choose_role(seniority: str) -> str:
    """Choose role based on seniority level"""
    # More senior people more likely to be in leadership
    if seniority == 'principal':
        weights = [20, 40, 30, 10, 0]  # mostly lead/manager/director
    elif seniority == 'staff':
        weights = [40, 30, 25, 5, 0]
    elif seniority == 'senior':
        weights = [60, 20, 15, 5, 0]
    elif seniority == 'mid':
        weights = [80, 10, 8, 2, 0]
    else:  # junior, intern
        weights = [95, 3, 2, 0, 0]
    
    return random.choices(
        list(ROLE_WEIGHTS.keys()),
        weights=weights,
        k=1
    )[0]

def generate_user(
    org_id: str,
    org_domain: str,
    user_index: int,
    base_datetime: datetime
) -> User:
    """Generate a single realistic user"""
    user_id = generate_uuid()
    
    # Realistic gender distribution (~50/50)
    is_male = random.random() < 0.5
    first_name = random.choice(FIRST_NAMES_MALE if is_male else FIRST_NAMES_FEMALE)
    last_name = random.choice(LAST_NAMES)
    
    email = generate_email(first_name, last_name, org_domain)
    full_name = f"{first_name} {last_name}"
    
    # Role and seniority with realistic distribution
    seniority = choose_seniority()
    role = choose_role(seniority)
    
    # Department assignment based on title
    departments = ["Engineering", "Product", "Design", "Marketing", "Operations",
                   "Sales", "Finance", "HR", "Legal", "Business Development"]
    department = random.choice(departments)
    
    # Created at some point after org was created
    days_ago = random.randint(30, 365 * 3)
    created_at = base_datetime - timedelta(days=days_ago)
    
    # 95% of users are active
    is_active = random.random() < 0.95
    
    return User(
        user_id=user_id,
        org_id=org_id,
        email=email,
        full_name=full_name,
        first_name=first_name,
        last_name=last_name,
        profile_picture_url=None,  # In real scenario, would generate avatar URL
        role=role,
        seniority_level=seniority,
        created_at=created_at,
        is_active=is_active,
        department=department
    )

def generate_users(
    org_id: str,
    org_domain: str,
    count: int = 100,
    base_datetime: datetime = None
) -> List[User]:
    """Generate multiple realistic users for an organization"""
    if base_datetime is None:
        base_datetime = datetime.now()
    
    users = []
    used_emails = set()  # Track emails to avoid duplicates
    
    for i in range(count):
        # Ensure unique email
        while True:
            user = generate_user(
                org_id=org_id,
                org_domain=org_domain,
                user_index=i,
                base_datetime=base_datetime
            )
            if user.email not in used_emails:
                used_emails.add(user.email)
                break
        
        users.append(user)
    
    return users

def ensure_role_distribution(users: List[User]) -> List[User]:
    """Ensure realistic distribution of roles in user list"""
    total = len(users)
    
    # Reset roles based on distribution
    for i, user in enumerate(users):
        rand = random.random()
        if rand < 0.01:  # 1% executives
            seniority = random.choice(['staff', 'principal'])
            user.role = 'executive'
        elif rand < 0.05:  # 4% directors
            seniority = random.choice(['senior', 'staff', 'principal'])
            user.role = 'director'
        elif rand < 0.15:  # 10% managers
            seniority = random.choice(['mid', 'senior', 'staff'])
            user.role = 'manager'
        elif rand < 0.30:  # 15% leads
            seniority = random.choice(['mid', 'senior'])
            user.role = 'lead'
        else:  # 70% individual contributors
            seniority = random.choice(['intern', 'junior', 'mid'])
            user.role = 'individual_contributor'
        
        user.seniority_level = seniority
    
    return users
