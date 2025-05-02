from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class BacklogItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done')
    ])
    priority = SelectField('Priority', choices=[
        (1, 'Critical'),
        (2, 'High'),
        (3, 'Medium'),
        (4, 'Low'),
        (5, 'Optional')
    ], coerce=int)
    story_points = IntegerField('Story Points', validators=[Optional(), NumberRange(min=0, max=100)])
    sprint_id = SelectField('Sprint', validators=[Optional()], coerce=int)
    submit = SubmitField('Save')

class SprintForm(FlaskForm):
    name = StringField('Sprint Name', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[Optional()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[Optional()], format='%Y-%m-%d')
    status = SelectField('Status', choices=[
        ('Planned', 'Planned'),
        ('Active', 'Active'),
        ('Completed', 'Completed')
    ])
    submit = SubmitField('Save')
