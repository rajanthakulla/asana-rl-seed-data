# Data models for Asana simulation
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List

@dataclass
class Organization:
    """Represents an Asana organization/workspace"""
    org_id: str
    name: str
    domain: str
    is_verified: bool
    created_at: datetime
    employee_count: int
    industry: str

@dataclass
class Team:
    """Represents a team within an organization"""
    team_id: str
    org_id: str
    name: str
    description: Optional[str]
    team_type: str  # 'engineering', 'marketing', 'operations', etc.
    created_at: datetime
    is_active: bool

@dataclass
class User:
    """Represents a workspace user"""
    user_id: str
    org_id: str
    email: str
    full_name: str
    first_name: str
    last_name: str
    profile_picture_url: Optional[str]
    role: str  # 'individual_contributor', 'lead', 'manager', 'director', 'executive'
    seniority_level: str  # 'intern', 'junior', 'mid', 'senior', 'staff', 'principal'
    created_at: datetime
    is_active: bool
    department: Optional[str]

@dataclass
class Project:
    """Represents a project within a team"""
    project_id: str
    org_id: str
    team_id: str
    name: str
    description: Optional[str]
    project_type: str  # 'product_development', 'marketing_campaign', 'operations', 'infrastructure'
    status: str  # 'active', 'archived', 'completed'
    created_at: datetime
    start_date: Optional[date]
    target_end_date: Optional[date]
    owner_user_id: str
    visibility: str  # 'private', 'team', 'org'

@dataclass
class Section:
    """Represents a section/column within a project"""
    section_id: str
    project_id: str
    name: str
    description: Optional[str]
    display_order: int
    created_at: datetime

@dataclass
class Task:
    """Represents a task (main unit of work)"""
    task_id: str
    project_id: str
    section_id: str
    name: str
    description: Optional[str]
    assignee_id: Optional[str]
    created_by_user_id: str
    created_at: datetime
    due_date: Optional[date]
    start_date: Optional[date]
    priority: Optional[str]  # 'low', 'medium', 'high', 'urgent'
    status: str  # 'not_started', 'in_progress', 'completed', 'on_hold'
    is_completed: bool
    completed_at: Optional[datetime]
    estimated_hours: Optional[float]
    actual_hours: Optional[float]

@dataclass
class Subtask:
    """Represents a subtask nested within a task"""
    subtask_id: str
    task_id: str
    name: str
    description: Optional[str]
    assignee_id: Optional[str]
    created_at: datetime
    due_date: Optional[date]
    is_completed: bool
    completed_at: Optional[datetime]

@dataclass
class Comment:
    """Represents a comment on a task"""
    comment_id: str
    task_id: str
    user_id: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime]
    is_edited: bool

@dataclass
class Tag:
    """Represents a tag that can be applied to tasks"""
    tag_id: str
    org_id: str
    name: str
    color: Optional[str]
    created_at: datetime

@dataclass
class CustomFieldDefinition:
    """Represents a custom field definition for a project"""
    field_id: str
    project_id: str
    name: str
    field_type: str  # 'text', 'number', 'dropdown', 'date', 'checkbox', 'multi_select'
    description: Optional[str]
    is_required: bool
    created_at: datetime

@dataclass
class CustomFieldValue:
    """Represents the value of a custom field for a task"""
    value_id: str
    task_id: str
    field_id: str
    value: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

@dataclass
class TaskTag:
    """Association between a task and a tag"""
    task_tag_id: str
    task_id: str
    tag_id: str
    added_at: datetime

@dataclass
class TaskDependency:
    """Represents a dependency between two tasks"""
    dependency_id: str
    task_id: str
    depends_on_task_id: str
    dependency_type: str  # 'blocks', 'is_blocked_by', 'related_to'
    created_at: datetime

@dataclass
class Attachment:
    """Represents a file attachment to a task"""
    attachment_id: str
    task_id: str
    file_name: str
    file_size: Optional[int]
    file_url: Optional[str]
    uploaded_by_user_id: str
    created_at: datetime

@dataclass
class TeamMembership:
    """Represents a user's membership in a team"""
    membership_id: str
    team_id: str
    user_id: str
    joined_at: datetime
    is_lead: bool
    role_in_team: Optional[str]  # 'member', 'lead', 'manager'
