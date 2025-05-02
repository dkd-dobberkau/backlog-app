from datetime import datetime
from app import db

class BacklogItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='To Do')  # To Do, In Progress, Done
    priority = db.Column(db.Integer, default=3)  # 1 (Highest) to 5 (Lowest)
    story_points = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprint.id'), nullable=True)
    
    def __repr__(self):
        return f'<BacklogItem {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'story_points': self.story_points,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'sprint_id': self.sprint_id
        }

class Sprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='Planned')  # Planned, Active, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    backlog_items = db.relationship('BacklogItem', backref='sprint', lazy='dynamic')
    
    def __repr__(self):
        return f'<Sprint {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'status': self.status,
            'created_at': self.created_at,
            'items': [item.to_dict() for item in self.backlog_items]
        }
