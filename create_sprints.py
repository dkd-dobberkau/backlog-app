from app import create_app, db
from app.models import Sprint
from datetime import datetime, timedelta

def create_sprints():
    """Create 10 sprints named after pairs of calendar weeks."""
    app = create_app()
    with app.app_context():
        # Clear existing sprints if needed
        # Sprint.query.delete()
        # db.session.commit()
        
        # Start from the current week
        current_date = datetime.utcnow()
        # Find the start of the current week (Monday)
        start_of_week = current_date - timedelta(days=current_date.weekday())
        
        # Create 10 sprints
        for i in range(10):
            # Calculate dates for this sprint
            sprint_start = start_of_week + timedelta(weeks=i*2)
            sprint_end = sprint_start + timedelta(days=13)  # 2 weeks - 1 day
            
            # Determine the calendar week numbers
            start_week_num = sprint_start.isocalendar()[1]
            end_week_num = sprint_end.isocalendar()[1]
            
            # Create sprint name with format "CW XX-YY"
            sprint_name = f"CW {start_week_num:02d}-{end_week_num:02d}"
            
            # Create the sprint
            sprint = Sprint(
                name=sprint_name,
                start_date=sprint_start,
                end_date=sprint_end,
                status='Planned'
            )
            
            db.session.add(sprint)
            print(f"Added sprint: {sprint_name} ({sprint_start.date()} - {sprint_end.date()})")
        
        # Commit all changes
        db.session.commit()
        print("All sprints created successfully!")

if __name__ == "__main__":
    create_sprints()