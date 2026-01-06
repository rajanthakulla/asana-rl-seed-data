# Quick Start Guide

Get up and running in 2 minutes.

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- ~50 MB free disk space

## Installation & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate the Database
```bash
python src/main.py
```

Default parameters:
- 500 users
- 3 projects per team  
- 12 tasks per section
- Output: `output/asana_simulation.sqlite` (2.4 MB)

**Time**: ~30 seconds

### 3. Customize (Optional)
```bash
# Generate smaller dataset (faster)
python src/main.py --num-users 100 --projects-per-team 2 --tasks-per-section 5

# Generate larger dataset (takes ~1-2 minutes)
python src/main.py --num-users 1000 --projects-per-team 5 --tasks-per-section 20

# Specify output path
python src/main.py --output /path/to/my_database.sqlite
```

### 4. Inspect the Database
```bash
sqlite3 output/asana_simulation.sqlite

# View organization
SELECT * FROM organizations;

# Count records
SELECT 'Users' as entity, COUNT(*) FROM users
UNION SELECT 'Tasks', COUNT(*) FROM tasks
UNION SELECT 'Projects', COUNT(*) FROM projects;

# View sample tasks
SELECT name, priority, status, due_date FROM tasks LIMIT 5;

# Exit
.quit
```

## Project Structure

```
.
├── src/main.py              # Run this!
├── src/generators/          # Data generation logic
├── src/models/              # Data model definitions
├── src/utils/               # Helper functions
├── schema.sql               # Database schema
├── README.md                # Full documentation
├── DOCUMENTATION.md         # Detailed methodology
└── SUBMISSION_GUIDE.md      # How to submit
```

## Key Features

✅ **Realistic Data**
- 500 users with diverse roles and seniority levels
- 500+ tasks with LLM-like generated names
- Real-world sourced patterns

✅ **Quality Assurance**
- Temporal consistency: created_at < due_date < completed_at
- Referential integrity: all foreign keys valid
- Unique constraints: no duplicate emails or project names

✅ **Easy Configuration**
- Adjust dataset size via CLI parameters
- All configuration externalized
- Reproducible results

## Database Statistics

| Entity | Count |
|--------|-------|
| Organizations | 1 |
| Users | 500 |
| Teams | 14 |
| Projects | 47 |
| Tasks | 558 |
| Subtasks | 552 |
| Comments | 329 |
| Custom Fields | 215 |
| Tags | 20 |

## Troubleshooting

**Problem**: `ModuleNotFoundError`  
**Solution**: Run from project root: `cd asana-rl-seed-data`

**Problem**: Database already exists  
**Solution**: Delete it first: `rm output/asana_simulation.sqlite`

**Problem**: Slow generation  
**Solution**: Use smaller dataset: `python src/main.py --num-users 100`

## Next Steps

1. **Review Code**: Start with `src/main.py`
2. **Explore Data**: Open database with SQLite viewer or CLI
3. **Read Documentation**: See `DOCUMENTATION.md` for full methodology
4. **Submit**: Follow `SUBMISSION_GUIDE.md`

## Support

- Full setup instructions in `README.md`
- Detailed methodology in `DOCUMENTATION.md`
- Submission help in `SUBMISSION_GUIDE.md`

---

**That's it!** You now have a realistic Asana workspace with 500+ employees worth of data. 🎉
