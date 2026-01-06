#!/usr/bin/env python3
"""
Main orchestration script for Asana RL Seed Data Generation

This script coordinates the entire data generation pipeline, ensuring:
1. Realistic data generation across all entities
2. Referential integrity and consistency
3. Temporal consistency
4. Distribution-based realism

Usage:
    python src/main.py --org-size large --num-projects 50 --tasks-per-section 15
"""

import sqlite3
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import generators
from generators.organizations import generate_single_large_organization
from generators.users import generate_users, ensure_role_distribution
from generators.teams import generate_teams, generate_team_memberships
from generators.projects import generate_projects, generate_all_sections
from generators.tasks import generate_tasks, generate_subtasks, generate_comments
from generators.tags import (
    generate_tags, generate_custom_fields, generate_custom_field_values,
    generate_task_tags, generate_task_dependencies
)

class AsanaDataGenerator:
    """Main data generator orchestrator"""
    
    def __init__(self, db_path: str = "output/asana_simulation.sqlite"):
        self.db_path = db_path
        self.connection = None
        self.base_datetime = datetime.now()
        
    def setup_database(self):
        """Create and initialize SQLite database"""
        logger.info(f"Setting up database at {self.db_path}")
        
        # Create output directory if needed
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Read and execute schema
        schema_path = Path("schema.sql")
        if not schema_path.exists():
            raise FileNotFoundError("schema.sql not found")
        
        self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()
        
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        cursor.executescript(schema)
        self.connection.commit()
        logger.info("Database schema created successfully")
    
    def insert_organizations(self, orgs):
        """Insert organizations into database"""
        cursor = self.connection.cursor()
        for org in orgs:
            cursor.execute("""
                INSERT INTO organizations 
                (org_id, name, domain, is_verified, created_at, employee_count, industry)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                org.org_id, org.name, org.domain, org.is_verified,
                org.created_at.isoformat(), org.employee_count, org.industry
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(orgs)} organization(s)")
    
    def insert_users(self, users):
        """Insert users into database"""
        cursor = self.connection.cursor()
        for user in users:
            cursor.execute("""
                INSERT INTO users
                (user_id, org_id, email, full_name, first_name, last_name,
                 profile_picture_url, role, seniority_level, created_at, is_active, department)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user.user_id, user.org_id, user.email, user.full_name,
                user.first_name, user.last_name, user.profile_picture_url,
                user.role, user.seniority_level, user.created_at.isoformat(),
                user.is_active, user.department
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(users)} users")
    
    def insert_teams(self, teams):
        """Insert teams into database"""
        cursor = self.connection.cursor()
        for team in teams:
            cursor.execute("""
                INSERT INTO teams
                (team_id, org_id, name, description, team_type, created_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                team.team_id, team.org_id, team.name, team.description,
                team.team_type, team.created_at.isoformat(), team.is_active
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(teams)} teams")
    
    def insert_team_memberships(self, memberships):
        """Insert team memberships"""
        cursor = self.connection.cursor()
        for membership in memberships:
            cursor.execute("""
                INSERT INTO team_memberships
                (membership_id, team_id, user_id, joined_at, is_lead, role_in_team)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                membership.membership_id, membership.team_id, membership.user_id,
                membership.joined_at.isoformat(), membership.is_lead, membership.role_in_team
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(memberships)} team memberships")
    
    def insert_projects(self, projects):
        """Insert projects"""
        cursor = self.connection.cursor()
        for project in projects:
            cursor.execute("""
                INSERT INTO projects
                (project_id, org_id, team_id, name, description, project_type,
                 status, created_at, start_date, target_end_date, owner_user_id, visibility)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                project.project_id, project.org_id, project.team_id,
                project.name, project.description, project.project_type,
                project.status, project.created_at.isoformat(),
                project.start_date.isoformat() if project.start_date else None,
                project.target_end_date.isoformat() if project.target_end_date else None,
                project.owner_user_id, project.visibility
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(projects)} projects")
    
    def insert_sections(self, sections):
        """Insert project sections"""
        cursor = self.connection.cursor()
        for section in sections:
            cursor.execute("""
                INSERT INTO sections
                (section_id, project_id, name, description, display_order, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                section.section_id, section.project_id, section.name,
                section.description, section.display_order, section.created_at.isoformat()
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(sections)} sections")
    
    def insert_tasks(self, tasks):
        """Insert tasks"""
        cursor = self.connection.cursor()
        for task in tasks:
            cursor.execute("""
                INSERT INTO tasks
                (task_id, project_id, section_id, name, description, assignee_id,
                 created_by_user_id, created_at, due_date, start_date, priority,
                 status, is_completed, completed_at, estimated_hours, actual_hours)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.task_id, task.project_id, task.section_id, task.name,
                task.description, task.assignee_id, task.created_by_user_id,
                task.created_at.isoformat(), task.due_date.isoformat() if task.due_date else None,
                task.start_date.isoformat() if task.start_date else None,
                task.priority, task.status, task.is_completed,
                task.completed_at.isoformat() if task.completed_at else None,
                task.estimated_hours, task.actual_hours
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(tasks)} tasks")
    
    def insert_subtasks(self, subtasks):
        """Insert subtasks"""
        cursor = self.connection.cursor()
        for subtask in subtasks:
            cursor.execute("""
                INSERT INTO subtasks
                (subtask_id, task_id, name, description, assignee_id, created_at,
                 due_date, is_completed, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                subtask.subtask_id, subtask.task_id, subtask.name,
                subtask.description, subtask.assignee_id, subtask.created_at.isoformat(),
                subtask.due_date.isoformat() if subtask.due_date else None,
                subtask.is_completed, subtask.completed_at.isoformat() if subtask.completed_at else None
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(subtasks)} subtasks")
    
    def insert_comments(self, comments):
        """Insert comments"""
        cursor = self.connection.cursor()
        for comment in comments:
            cursor.execute("""
                INSERT INTO comments
                (comment_id, task_id, user_id, content, created_at, updated_at, is_edited)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                comment.comment_id, comment.task_id, comment.user_id,
                comment.content, comment.created_at.isoformat(),
                comment.updated_at.isoformat() if comment.updated_at else None,
                comment.is_edited
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(comments)} comments")
    
    def insert_tags(self, tags):
        """Insert tags"""
        cursor = self.connection.cursor()
        for tag in tags:
            cursor.execute("""
                INSERT INTO tags
                (tag_id, org_id, name, color, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                tag.tag_id, tag.org_id, tag.name, tag.color, tag.created_at.isoformat()
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(tags)} tags")
    
    def insert_custom_fields(self, fields):
        """Insert custom field definitions"""
        cursor = self.connection.cursor()
        for field in fields:
            cursor.execute("""
                INSERT INTO custom_field_definitions
                (field_id, project_id, name, field_type, description, is_required, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                field.field_id, field.project_id, field.name, field.field_type,
                field.description, field.is_required, field.created_at.isoformat()
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(fields)} custom field definitions")
    
    def insert_custom_field_values(self, values):
        """Insert custom field values"""
        cursor = self.connection.cursor()
        for value in values:
            cursor.execute("""
                INSERT INTO custom_field_values
                (value_id, task_id, field_id, value, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                value.value_id, value.task_id, value.field_id, value.value,
                value.created_at.isoformat(), value.updated_at.isoformat() if value.updated_at else None
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(values)} custom field values")
    
    def insert_task_tags(self, task_tags):
        """Insert task-tag associations"""
        cursor = self.connection.cursor()
        for task_tag in task_tags:
            cursor.execute("""
                INSERT INTO task_tags
                (task_tag_id, task_id, tag_id, added_at)
                VALUES (?, ?, ?, ?)
            """, (
                task_tag.task_tag_id, task_tag.task_id, task_tag.tag_id,
                task_tag.added_at.isoformat()
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(task_tags)} task-tag associations")
    
    def insert_task_dependencies(self, dependencies):
        """Insert task dependencies"""
        cursor = self.connection.cursor()
        for dep in dependencies:
            cursor.execute("""
                INSERT INTO task_dependencies
                (dependency_id, task_id, depends_on_task_id, dependency_type, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                dep.dependency_id, dep.task_id, dep.depends_on_task_id,
                dep.dependency_type, dep.created_at.isoformat()
            ))
        self.connection.commit()
        logger.info(f"Inserted {len(dependencies)} task dependencies")
    
    def generate_all(self, num_users: int = 500, projects_per_team: int = 3,
                    tasks_per_section: int = 15):
        """Generate entire dataset"""
        try:
            logger.info("=" * 60)
            logger.info("Starting Asana Seed Data Generation")
            logger.info("=" * 60)
            
            # 1. Organizations
            logger.info("\n[1/11] Generating organizations...")
            orgs = [generate_single_large_organization(base_datetime=self.base_datetime)]
            self.insert_organizations(orgs)
            org = orgs[0]
            
            # 2. Users
            logger.info("\n[2/11] Generating users...")
            users = generate_users(org.org_id, org.domain, num_users, self.base_datetime)
            users = ensure_role_distribution(users)
            self.insert_users(users)
            
            # 3. Teams
            logger.info("\n[3/11] Generating teams...")
            teams = generate_teams(org.org_id, self.base_datetime)
            self.insert_teams(teams)
            
            # 4. Team Memberships
            logger.info("\n[4/11] Generating team memberships...")
            memberships = generate_team_memberships(teams, users, self.base_datetime)
            self.insert_team_memberships(memberships)
            
            # 5. Projects
            logger.info("\n[5/11] Generating projects...")
            projects = generate_projects(org.org_id, teams, users, self.base_datetime, projects_per_team)
            self.insert_projects(projects)
            
            # 6. Sections
            logger.info("\n[6/11] Generating sections...")
            sections = generate_all_sections(projects, self.base_datetime)
            self.insert_sections(sections)
            
            # 7. Tasks
            logger.info("\n[7/11] Generating tasks...")
            tasks = generate_tasks(projects, sections, users, self.base_datetime, tasks_per_section)
            self.insert_tasks(tasks)
            
            # 8. Subtasks
            logger.info("\n[8/11] Generating subtasks...")
            subtasks = generate_subtasks(tasks, users, self.base_datetime)
            self.insert_subtasks(subtasks)
            
            # 9. Comments
            logger.info("\n[9/11] Generating comments...")
            comments = generate_comments(tasks, users, self.base_datetime)
            self.insert_comments(comments)
            
            # 10. Tags and Custom Fields
            logger.info("\n[10/11] Generating tags and custom fields...")
            tags = generate_tags(org.org_id, self.base_datetime)
            self.insert_tags(tags)
            
            custom_fields = generate_custom_fields(projects, self.base_datetime)
            self.insert_custom_fields(custom_fields)
            
            custom_field_values = generate_custom_field_values(tasks, custom_fields, self.base_datetime)
            self.insert_custom_field_values(custom_field_values)
            
            task_tags = generate_task_tags(tasks, tags, self.base_datetime)
            self.insert_task_tags(task_tags)
            
            # 11. Task Dependencies
            logger.info("\n[11/11] Generating task dependencies...")
            dependencies = generate_task_dependencies(tasks, self.base_datetime)
            self.insert_task_dependencies(dependencies)
            
            # Summary
            logger.info("\n" + "=" * 60)
            logger.info("Data Generation Complete!")
            logger.info("=" * 60)
            logger.info(f"Database saved to: {self.db_path}")
            logger.info(f"Total organizations: 1")
            logger.info(f"Total users: {len(users)}")
            logger.info(f"Total teams: {len(teams)}")
            logger.info(f"Total projects: {len(projects)}")
            logger.info(f"Total tasks: {len(tasks)}")
            logger.info(f"Total subtasks: {len(subtasks)}")
            logger.info(f"Total comments: {len(comments)}")
            logger.info(f"Total tags: {len(tags)}")
            logger.info(f"Total custom fields: {len(custom_fields)}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Error during generation: {e}", exc_info=True)
            raise
        finally:
            if self.connection:
                self.connection.close()

def main():
    parser = argparse.ArgumentParser(
        description="Generate realistic Asana seed data for RL environment"
    )
    parser.add_argument(
        "--num-users",
        type=int,
        default=500,
        help="Number of users to generate (default: 500)"
    )
    parser.add_argument(
        "--projects-per-team",
        type=int,
        default=3,
        help="Average projects per team (default: 3)"
    )
    parser.add_argument(
        "--tasks-per-section",
        type=int,
        default=15,
        help="Average tasks per section (default: 15)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/asana_simulation.sqlite",
        help="Output database path (default: output/asana_simulation.sqlite)"
    )
    
    args = parser.parse_args()
    
    generator = AsanaDataGenerator(db_path=args.output)
    generator.setup_database()
    generator.generate_all(
        num_users=args.num_users,
        projects_per_team=args.projects_per_team,
        tasks_per_section=args.tasks_per_section
    )

if __name__ == "__main__":
    main()
