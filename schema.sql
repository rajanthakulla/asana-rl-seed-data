-- Asana RL Seed Data Schema
-- Comprehensive relational schema for simulating Asana enterprise workspace

-- ============================================================================
-- Organizations / Workspaces
-- ============================================================================
CREATE TABLE organizations (
    org_id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    domain TEXT NOT NULL UNIQUE,
    is_verified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    employee_count INTEGER NOT NULL,
    industry TEXT NOT NULL
);

-- ============================================================================
-- Teams
-- ============================================================================
CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    team_type TEXT NOT NULL, -- 'engineering', 'marketing', 'operations', 'sales', 'design', 'leadership'
    created_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id),
    UNIQUE(org_id, name)
);

-- ============================================================================
-- Users
-- ============================================================================
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    profile_picture_url TEXT,
    role TEXT NOT NULL, -- 'individual_contributor', 'lead', 'manager', 'director', 'executive'
    seniority_level TEXT NOT NULL, -- 'intern', 'junior', 'mid', 'senior', 'staff', 'principal'
    created_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    department TEXT,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- ============================================================================
-- Team Memberships
-- ============================================================================
CREATE TABLE team_memberships (
    membership_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    joined_at TIMESTAMP NOT NULL,
    is_lead BOOLEAN DEFAULT 0,
    role_in_team TEXT, -- 'member', 'lead', 'manager'
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(team_id, user_id)
);

-- ============================================================================
-- Projects
-- ============================================================================
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    project_type TEXT NOT NULL, -- 'product_development', 'marketing_campaign', 'operations', 'infrastructure'
    status TEXT NOT NULL DEFAULT 'active', -- 'active', 'archived', 'completed'
    created_at TIMESTAMP NOT NULL,
    start_date DATE,
    target_end_date DATE,
    owner_user_id TEXT NOT NULL,
    visibility TEXT DEFAULT 'team', -- 'private', 'team', 'org'
    FOREIGN KEY (org_id) REFERENCES organizations(org_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (owner_user_id) REFERENCES users(user_id),
    UNIQUE(org_id, name)
);

-- ============================================================================
-- Sections (subdivisions within projects)
-- ============================================================================
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    display_order INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    UNIQUE(project_id, name)
);

-- ============================================================================
-- Custom Field Definitions
-- ============================================================================
CREATE TABLE custom_field_definitions (
    field_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    field_type TEXT NOT NULL, -- 'text', 'number', 'dropdown', 'date', 'checkbox', 'multi_select'
    description TEXT,
    is_required BOOLEAN DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    UNIQUE(project_id, name)
);

-- ============================================================================
-- Tags
-- ============================================================================
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT, -- hex color code
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id),
    UNIQUE(org_id, name)
);

-- ============================================================================
-- Tasks (main unit of work)
-- ============================================================================
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT, -- can be null for unassigned tasks
    created_by_user_id TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    due_date DATE,
    start_date DATE,
    priority TEXT, -- 'low', 'medium', 'high', 'urgent'
    status TEXT DEFAULT 'not_started', -- 'not_started', 'in_progress', 'completed', 'on_hold'
    is_completed BOOLEAN DEFAULT 0,
    completed_at TIMESTAMP,
    estimated_hours REAL,
    actual_hours REAL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)
);

-- ============================================================================
-- Subtasks
-- ============================================================================
CREATE TABLE subtasks (
    subtask_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT,
    created_at TIMESTAMP NOT NULL,
    due_date DATE,
    is_completed BOOLEAN DEFAULT 0,
    completed_at TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id)
);

-- ============================================================================
-- Comments / Stories (activity and discussion)
-- ============================================================================
CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    is_edited BOOLEAN DEFAULT 0,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ============================================================================
-- Custom Field Values
-- ============================================================================
CREATE TABLE custom_field_values (
    value_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    field_id TEXT NOT NULL,
    value TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id),
    UNIQUE(task_id, field_id)
);

-- ============================================================================
-- Task-Tag Associations
-- ============================================================================
CREATE TABLE task_tags (
    task_tag_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    added_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
    UNIQUE(task_id, tag_id)
);

-- ============================================================================
-- Task Dependencies
-- ============================================================================
CREATE TABLE task_dependencies (
    dependency_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    depends_on_task_id TEXT NOT NULL,
    dependency_type TEXT DEFAULT 'blocks', -- 'blocks', 'is_blocked_by', 'related_to'
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks(task_id),
    UNIQUE(task_id, depends_on_task_id)
);

-- ============================================================================
-- Attachments
-- ============================================================================
CREATE TABLE attachments (
    attachment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_size INTEGER,
    file_url TEXT,
    uploaded_by_user_id TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (uploaded_by_user_id) REFERENCES users(user_id)
);

-- ============================================================================
-- Indexes for Performance
-- ============================================================================
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_assignee ON tasks(assignee_id);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
CREATE INDEX idx_tasks_section ON tasks(section_id);
CREATE INDEX idx_subtasks_task ON subtasks(task_id);
CREATE INDEX idx_comments_task ON comments(task_id);
CREATE INDEX idx_team_memberships_user ON team_memberships(user_id);
CREATE INDEX idx_team_memberships_team ON team_memberships(team_id);
CREATE INDEX idx_custom_field_values_task ON custom_field_values(task_id);
CREATE INDEX idx_task_tags_task ON task_tags(task_id);
CREATE INDEX idx_projects_team ON projects(team_id);
CREATE INDEX idx_users_org ON users(org_id);
CREATE INDEX idx_teams_org ON teams(org_id);
