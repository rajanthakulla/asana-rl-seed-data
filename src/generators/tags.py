# Tags, Custom Fields and other metadata generation
import random
from datetime import datetime
from typing import List
from models import Tag, CustomFieldDefinition, CustomFieldValue, TaskTag, TaskDependency
from utils.helpers import generate_uuid

# Realistic tags used across teams
UNIVERSAL_TAGS = [
    ("bug", "#FF0000"),
    ("feature", "#0066FF"),
    ("documentation", "#6600FF"),
    ("testing", "#FF9900"),
    ("performance", "#FF6600"),
    ("security", "#DD0000"),
    ("ui_ux", "#00BB00"),
    ("devops", "#0099FF"),
    ("refactoring", "#9933FF"),
    ("epic", "#0066FF"),
    ("chore", "#999999"),
    ("tech_debt", "#FF6633"),
    ("review_needed", "#FFFF00"),
    ("blocked", "#FF3333"),
    ("urgent", "#FF0000"),
    ("p0_critical", "#DD0000"),
    ("p1_high", "#FF6600"),
    ("p2_medium", "#FFFF00"),
    ("p3_low", "#00BB00"),
    ("backlog", "#CCCCCC"),
]

# Custom field patterns by project type
CUSTOM_FIELDS_BY_TYPE = {
    'product_development': [
        ('Priority', 'dropdown', ['P0 - Critical', 'P1 - High', 'P2 - Medium', 'P3 - Low']),
        ('Story Points', 'number', None),
        ('Status', 'dropdown', ['Not Started', 'In Progress', 'In Review', 'Done']),
        ('Effort', 'number', None),
        ('Type', 'dropdown', ['Feature', 'Bug', 'Technical Debt', 'Refactoring']),
        ('Sprint', 'dropdown', None),
    ],
    'marketing_campaign': [
        ('Campaign Type', 'dropdown', ['Social Media', 'Email', 'Blog', 'Event', 'Partnership']),
        ('Status', 'dropdown', ['Planning', 'In Progress', 'Review', 'Published']),
        ('ROI Target %', 'number', None),
        ('Budget', 'number', None),
        ('Owner', 'text', None),
    ],
    'operations': [
        ('Department', 'dropdown', ['HR', 'Finance', 'Legal', 'Admin', 'IT']),
        ('Approval Status', 'dropdown', ['Pending', 'Approved', 'Rejected']),
        ('Budget Code', 'text', None),
        ('Compliance', 'dropdown', ['SOC2', 'GDPR', 'ISO', 'None']),
    ]
}

def generate_tags(org_id: str, created_at: datetime) -> List[Tag]:
    """Generate organization-wide tags"""
    tags = []
    
    for name, color in UNIVERSAL_TAGS:
        tag_id = generate_uuid()
        tag = Tag(
            tag_id=tag_id,
            org_id=org_id,
            name=name,
            color=color,
            created_at=created_at
        )
        tags.append(tag)
    
    return tags

def generate_custom_fields(
    projects: List,
    created_at: datetime
) -> List[CustomFieldDefinition]:
    """Generate custom field definitions for projects"""
    fields = []
    
    for project in projects:
        # Get default fields for project type
        default_fields = CUSTOM_FIELDS_BY_TYPE.get(
            project.project_type,
            [('Status', 'dropdown', ['To Do', 'In Progress', 'Done'])]
        )
        
        for field_name, field_type, options in default_fields:
            field_id = generate_uuid()
            field = CustomFieldDefinition(
                field_id=field_id,
                project_id=project.project_id,
                name=field_name,
                field_type=field_type,
                description=f"Custom field: {field_name}",
                is_required=field_name == 'Status',
                created_at=created_at
            )
            fields.append(field)
    
    return fields

def generate_custom_field_values(
    tasks: List,
    custom_fields: List,
    created_at: datetime
) -> List[CustomFieldValue]:
    """Generate values for custom fields on tasks"""
    values = []
    
    for task in tasks:
        # Get fields for this task's project
        task_fields = [f for f in custom_fields if f.project_id == task.project_id]
        
        for field in task_fields:
            value_id = generate_uuid()
            
            # Generate value based on field type
            if field.field_type == 'dropdown':
                field_value = random.choice(['Yes', 'No', 'Pending', 'Done', 'In Progress'])
            elif field.field_type == 'number':
                field_value = str(random.randint(1, 100))
            elif field.field_type == 'text':
                field_value = f"Value_{random.randint(1, 1000)}"
            else:
                field_value = "Unknown"
            
            value = CustomFieldValue(
                value_id=value_id,
                task_id=task.task_id,
                field_id=field.field_id,
                value=field_value,
                created_at=created_at,
                updated_at=None
            )
            values.append(value)
    
    return values

def generate_task_tags(
    tasks: List,
    tags: List,
    created_at: datetime
) -> List[TaskTag]:
    """Generate tag associations for tasks"""
    task_tags = []
    
    for task in tasks:
        # 60% of tasks get 1-3 tags
        if random.random() > 0.60:
            continue
        
        num_tags = random.randint(1, 3)
        selected_tags = random.sample(tags, min(num_tags, len(tags)))
        
        for tag in selected_tags:
            task_tag_id = generate_uuid()
            task_tag = TaskTag(
                task_tag_id=task_tag_id,
                task_id=task.task_id,
                tag_id=tag.tag_id,
                added_at=created_at
            )
            task_tags.append(task_tag)
    
    return task_tags

def generate_task_dependencies(
    tasks: List,
    created_at: datetime
) -> List[TaskDependency]:
    """Generate task dependencies"""
    dependencies = []
    
    for task in tasks:
        # 20% of tasks have dependencies
        if random.random() > 0.20:
            continue
        
        # Find other tasks in same project
        related_tasks = [t for t in tasks if t.project_id == task.project_id and t.task_id != task.task_id]
        
        if not related_tasks:
            continue
        
        # 1-2 dependencies per task
        num_deps = random.randint(1, 2)
        selected_deps = random.sample(related_tasks, min(num_deps, len(related_tasks)))
        
        for dep_task in selected_deps:
            dep_id = generate_uuid()
            dependency = TaskDependency(
                dependency_id=dep_id,
                task_id=task.task_id,
                depends_on_task_id=dep_task.task_id,
                dependency_type=random.choice(['blocks', 'is_blocked_by', 'related_to']),
                created_at=created_at
            )
            dependencies.append(dependency)
    
    return dependencies
