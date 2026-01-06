# Task data generation - most critical for realism
# Based on real GitHub issues, Asana templates, and productivity research

import random
from datetime import datetime, timedelta, date
from typing import List, Tuple, Optional
from models import Task, Subtask, Comment, Tag, CustomFieldValue, TaskTag
from utils.helpers import (
    generate_uuid, generate_weighted_due_date, avoid_weekend,
    generate_completion_time, is_realistic_date_range
)
import numpy as np

# Real task naming patterns extracted from GitHub issues (engineering)
GITHUB_ENGINEERING_PATTERNS = [
    "Fix {component} {issue}",
    "Refactor {component} for {goal}",
    "Add {feature} to {component}",
    "Improve {component} {metric}",
    "Optimize {component} {area}",
    "Handle {edge_case} in {component}",
    "Update {component} to {version}",
    "Implement {feature} in {component}",
    "Debug {issue} in {component}",
    "Add tests for {component}"
]

COMPONENTS = [
    "authentication", "database", "API", "frontend", "backend",
    "cache layer", "message queue", "payment gateway", "search",
    "analytics", "notifications", "logging", "monitoring", "security"
]

ISSUES = [
    "race condition", "memory leak", "SQL injection", "timeout",
    "missing validation", "incorrect parsing", "unicode handling",
    "performance degradation", "inconsistent state", "concurrent access"
]

GOALS = [
    "readability", "maintainability", "scalability", "security",
    "performance", "testability", "extensibility"
]

METRICS = [
    "latency", "throughput", "memory usage", "CPU consumption",
    "response time", "error rate", "availability"
]

EDGE_CASES = [
    "null values", "empty arrays", "circular references",
    "large payloads", "network timeouts", "duplicate requests"
]

# Marketing task patterns
MARKETING_PATTERNS = [
    "Create {content_type} for {channel}",
    "Plan {campaign} campaign",
    "Analyze {metric} for {period}",
    "Develop {content_type} assets",
    "Execute {campaign} launch",
    "Update {asset} with new branding",
    "Research {topic} for content"
]

CONTENT_TYPES = ["blog post", "case study", "video", "infographic", "whitepaper", "webinar", "email series"]
CHANNELS = ["social media", "email", "blog", "LinkedIn", "Twitter", "website"]
CAMPAIGNS = ["Q1 launch", "product launch", "seasonal", "partnership", "thought leadership"]
ASSETS = ["brand guidelines", "website copy", "social templates", "email templates"]
TOPICS = ["market trends", "user needs", "competitor landscape", "industry insights"]

# Operations task patterns
OPERATIONS_PATTERNS = [
    "Prepare {document} for {event}",
    "Schedule {event_type} with {team}",
    "Update {system} configuration",
    "Review {process} and optimize",
    "Conduct {activity} session",
    "Onboard {resource_type}",
    "Complete {compliance} check"
]

DOCUMENTS = ["budget", "report", "presentation", "memo", "plan"]
EVENTS = ["board meeting", "town hall", "team building", "offsite"]
EVENT_TYPES = ["meeting", "training", "workshop", "conference"]
SYSTEMS = ["HR", "finance", "CRM", "project management"]
PROCESSES = ["hiring", "onboarding", "expense approval", "hiring workflow"]
ACTIVITIES = ["training", "planning", "feedback", "retrospective"]
RESOURCES = ["new hire", "new team", "vendor", "contractor"]
COMPLIANCE = ["security audit", "GDPR", "SOC2", "financial"]

def generate_task_name(project_type: str) -> str:
    """Generate realistic task names based on project type"""
    if project_type == 'product_development':
        pattern = random.choice(GITHUB_ENGINEERING_PATTERNS)
        name = pattern.format(
            component=random.choice(COMPONENTS),
            issue=random.choice(ISSUES),
            feature=random.choice(["feature", "endpoint", "widget", "component"]),
            goal=random.choice(GOALS),
            metric=random.choice(METRICS),
            edge_case=random.choice(EDGE_CASES),
            version=f"v{random.randint(1, 5)}.{random.randint(0, 9)}",
            area=random.choice(["performance", "security", "reliability"])
        )
    elif project_type == 'marketing_campaign':
        pattern = random.choice(MARKETING_PATTERNS)
        name = pattern.format(
            content_type=random.choice(CONTENT_TYPES),
            channel=random.choice(CHANNELS),
            campaign=random.choice(CAMPAIGNS),
            metric=random.choice(["engagement", "conversion", "reach", "sentiment"]),
            period=random.choice(["Q1", "Q2", "this month", "this week"]),
            asset=random.choice(ASSETS),
            topic=random.choice(TOPICS)
        )
    elif project_type == 'operations':
        pattern = random.choice(OPERATIONS_PATTERNS)
        name = pattern.format(
            document=random.choice(DOCUMENTS),
            event=random.choice(EVENTS),
            event_type=random.choice(EVENT_TYPES),
            team=random.choice(["engineering", "sales", "marketing", "leadership"]),
            system=random.choice(SYSTEMS),
            process=random.choice(PROCESSES),
            activity=random.choice(ACTIVITIES),
            resource_type=random.choice(RESOURCES),
            compliance=random.choice(COMPLIANCE)
        )
    else:
        # Default generic task
        verbs = ["Implement", "Fix", "Update", "Review", "Test", "Deploy", "Document", "Optimize"]
        objects = ["feature", "bug", "process", "documentation", "system", "workflow"]
        name = f"{random.choice(verbs)} {random.choice(objects)}"
    
    return name.capitalize()

def generate_task_description(task_name: str, project_type: str) -> str:
    """Generate realistic task descriptions with varying detail levels"""
    # 20% no description
    if random.random() < 0.20:
        return None
    
    # 50% brief 1-3 sentence description
    if random.random() < 0.50:
        descriptions_brief = [
            "Work on implementing this feature in upcoming sprint.",
            "Investigate and resolve reported issue.",
            "Review and merge proposed changes.",
            "Complete as part of planned milestone.",
            "User-requested improvement for workflow optimization."
        ]
        return random.choice(descriptions_brief)
    
    # 30% detailed with bullet points (LLM-like content)
    detailed_templates = [
        f"""
{task_name} - Detailed Implementation

Current State:
- Limited functionality in current implementation
- Performance concerns reported

Goals:
- Implement full {random.choice(['feature set', 'workflow', 'integration'])}
- Improve performance metrics
- Ensure comprehensive test coverage

Acceptance Criteria:
- All tests passing
- Code review approval
- Performance benchmarks met
- Documentation updated

Timeline: {random.randint(1, 4)} weeks
Priority: {random.choice(['High', 'Medium'])}
        """,
        f"""
Background: {task_name}

Description:
{task_name} is critical for our {random.choice(['Q1', 'Q2', 'Q3', 'Q4'])} roadmap.

Requirements:
- Backward compatibility required
- Cross-team coordination needed
- Stakeholder approval pending

Next Steps:
1. Design review meeting
2. Implementation sprint
3. QA testing
4. Production deployment

Stakeholders: {random.choice(['Product', 'Engineering', 'Marketing'])} team
        """
    ]
    
    return random.choice(detailed_templates)

def generate_priority() -> str:
    """Generate task priority with realistic distribution"""
    # Based on typical task distribution: most medium, fewer high/low
    return random.choices(
        ['low', 'medium', 'high', 'urgent'],
        weights=[10, 60, 25, 5],
        k=1
    )[0]

def generate_task_status(is_completed: bool) -> str:
    """Generate task status based on completion"""
    if is_completed:
        return 'completed'
    
    # Distribution of non-completed tasks
    return random.choices(
        ['not_started', 'in_progress', 'on_hold'],
        weights=[30, 60, 10],
        k=1
    )[0]

def generate_task(
    project_id: str,
    section_id: str,
    user_ids: List[str],
    created_by_user_id: str,
    created_at: datetime,
    project_type: str,
    project_owner_id: str,
    base_datetime: datetime
) -> Task:
    """Generate a single realistic task with temporal consistency"""
    task_id = generate_uuid()
    
    # Generate name and description
    name = generate_task_name(project_type)
    description = generate_task_description(name, project_type)
    
    # Assignee: 85% assigned, 15% unassigned (per Asana benchmarks)
    if random.random() < 0.85:
        assignee_id = random.choice(user_ids)
    else:
        assignee_id = None
    
    # Due date with realistic distribution
    due_date, is_overdue = generate_weighted_due_date(created_at, base_datetime.date())
    if due_date:
        due_date = avoid_weekend(due_date, avoid_weekend=True)
    
    # Priority
    priority = generate_priority()
    
    # Completion with realistic cycle time distribution
    # Engineering: 70-85%, Bug tracking: 60-70%, Ongoing: 40-50%
    if project_type == 'product_development':
        completion_prob = 0.75
    elif project_type == 'infrastructure':
        completion_prob = 0.70
    else:
        completion_prob = 0.60
    
    completed_at, is_completed = generate_completion_time(created_at, completion_prob)
    status = generate_task_status(is_completed)
    
    # Ensure temporal consistency
    if completed_at and due_date:
        if not is_realistic_date_range(created_at, completed_at):
            completed_at = created_at + timedelta(days=random.randint(1, 14))
    
    # Estimated hours (varies by task)
    if random.random() < 0.7:
        estimated_hours = random.choices(
            [2, 4, 8, 16, 24, 40],
            weights=[20, 25, 30, 15, 8, 2],
            k=1
        )[0]
    else:
        estimated_hours = None
    
    # Actual hours (if completed, typically close to estimate)
    actual_hours = None
    if is_completed and estimated_hours:
        variance = random.gauss(0, 0.3)  # 30% variance
        actual_hours = max(estimated_hours * (1 + variance), 0.5)
    
    return Task(
        task_id=task_id,
        project_id=project_id,
        section_id=section_id,
        name=name,
        description=description,
        assignee_id=assignee_id,
        created_by_user_id=created_by_user_id,
        created_at=created_at,
        due_date=due_date,
        start_date=None,
        priority=priority,
        status=status,
        is_completed=is_completed,
        completed_at=completed_at,
        estimated_hours=estimated_hours,
        actual_hours=actual_hours
    )

def generate_tasks(
    projects: List,
    sections: List,
    users: List,
    base_datetime: datetime = None,
    tasks_per_section: int = 10
) -> List[Task]:
    """Generate tasks for all projects and sections"""
    if base_datetime is None:
        base_datetime = datetime.now()
    
    tasks = []
    user_ids = [u.user_id for u in users]
    
    for project in projects:
        # Get sections for this project
        project_sections = [s for s in sections if s.project_id == project.project_id]
        
        # Generate tasks (more for active projects)
        if project.status == 'active':
            num_tasks = random.randint(tasks_per_section - 2, tasks_per_section + 5)
        else:
            num_tasks = random.randint(3, 10)
        
        for _ in range(num_tasks):
            section = random.choice(project_sections)
            task_created_at = generate_task_creation_time(
                project.created_at,
                base_datetime
            )
            
            task = generate_task(
                project_id=project.project_id,
                section_id=section.section_id,
                user_ids=user_ids,
                created_by_user_id=random.choice(user_ids),
                created_at=task_created_at,
                project_type=project.project_type,
                project_owner_id=project.owner_user_id,
                base_datetime=base_datetime
            )
            tasks.append(task)
    
    return tasks

def generate_task_creation_time(
    project_created_at: datetime,
    base_datetime: datetime
) -> datetime:
    """Generate task creation time distributed throughout project lifetime"""
    project_age = (base_datetime - project_created_at).days
    
    # Most tasks created early in project (realistic pattern)
    # But some added throughout project
    rand = random.random()
    if rand < 0.6:
        # 60% created in first 20% of project timeline
        days_into_project = random.randint(0, max(1, int(project_age * 0.2)))
    elif rand < 0.85:
        # 25% created in first 50% of project timeline
        days_into_project = random.randint(0, max(1, int(project_age * 0.5)))
    else:
        # 15% created throughout project
        days_into_project = random.randint(0, project_age)
    
    task_created_at = project_created_at + timedelta(days=days_into_project)
    
    # Randomize within the day
    hours = random.randint(8, 18)
    minutes = random.randint(0, 59)
    
    return task_created_at.replace(hour=hours, minute=minutes, second=0)

def generate_subtasks(
    tasks: List[Task],
    users: List,
    base_datetime: datetime = None
) -> List[Subtask]:
    """Generate subtasks for complex tasks (realistic pattern)"""
    if base_datetime is None:
        base_datetime = datetime.now()
    
    subtasks = []
    user_ids = [u.user_id for u in users]
    
    for task in tasks:
        # 40% of tasks have subtasks
        if random.random() > 0.40:
            continue
        
        # 1-4 subtasks per task
        num_subtasks = random.randint(1, 4)
        
        for i in range(num_subtasks):
            subtask_id = generate_uuid()
            
            subtask_names = [
                f"Design & Planning",
                f"Implementation",
                f"Testing",
                f"Documentation",
                f"Review & Feedback",
                f"Refinement",
                f"Deployment"
            ]
            
            subtask = Subtask(
                subtask_id=subtask_id,
                task_id=task.task_id,
                name=random.choice(subtask_names),
                description=None if random.random() < 0.5 else "Subtask details",
                assignee_id=random.choice([None, random.choice(user_ids)]),
                created_at=task.created_at + timedelta(days=random.randint(0, 5)),
                due_date=task.due_date,
                is_completed=task.is_completed,
                completed_at=task.completed_at if task.is_completed else None
            )
            subtasks.append(subtask)
    
    return subtasks

def generate_comments(
    tasks: List[Task],
    users: List,
    base_datetime: datetime = None
) -> List[Comment]:
    """Generate realistic comments on tasks"""
    if base_datetime is None:
        base_datetime = datetime.now()
    
    comments = []
    user_ids = [u.user_id for u in users]
    
    comment_templates = [
        "Looking good! Please make sure to test thoroughly.",
        "I've reviewed the changes - a few minor suggestions in the PR.",
        "Great progress on this. Let me know if you need any help.",
        "This is blocking the release. Can we prioritize?",
        "Thanks for the update. Ready to move forward.",
        "I found an issue in the implementation. Let's sync up.",
        "Approved for merge. Thanks for the thorough testing.",
        "Do we have a timeline for this?",
        "I'll take a look and provide feedback.",
        "This needs more documentation before we proceed."
    ]
    
    for task in tasks:
        # 30% of tasks have comments
        if random.random() > 0.30:
            continue
        
        # 1-3 comments per task
        num_comments = random.randint(1, 3)
        
        for j in range(num_comments):
            comment_id = generate_uuid()
            comment_at = task.created_at + timedelta(days=random.randint(0, 10))
            
            comment = Comment(
                comment_id=comment_id,
                task_id=task.task_id,
                user_id=random.choice(user_ids),
                content=random.choice(comment_templates),
                created_at=comment_at,
                updated_at=None,
                is_edited=False
            )
            comments.append(comment)
    
    return comments
