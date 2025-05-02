from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import BacklogItem, Sprint
from app.forms import BacklogItemForm, SprintForm
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@main_bp.route('/')
def index():
    return render_template('index.html')

# Product Backlog Routes
@main_bp.route('/product-backlog')
def product_backlog():
    items = BacklogItem.query.filter_by(sprint_id=None).order_by(BacklogItem.priority, BacklogItem.created_at).all()
    return render_template('product_backlog.html', items=items)

@main_bp.route('/backlog-item/add', methods=['GET', 'POST'])
def add_backlog_item():
    form = BacklogItemForm()
    
    # Populate sprint select field
    sprints = Sprint.query.order_by(Sprint.name).all()
    form.sprint_id.choices = [(0, 'Product Backlog')] + [(s.id, s.name) for s in sprints]
    
    if form.validate_on_submit():
        sprint_id = form.sprint_id.data if form.sprint_id.data != 0 else None
        item = BacklogItem(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            story_points=form.story_points.data,
            sprint_id=sprint_id
        )
        db.session.add(item)
        db.session.commit()
        flash('Backlog item added successfully!', 'success')
        if sprint_id:
            return redirect(url_for('main.sprint_backlog', sprint_id=sprint_id))
        return redirect(url_for('main.product_backlog'))
    
    return render_template('add_item.html', form=form, title='Add Backlog Item')

@main_bp.route('/backlog-item/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_backlog_item(item_id):
    item = BacklogItem.query.get_or_404(item_id)
    form = BacklogItemForm(obj=item)
    
    # Populate sprint select field
    sprints = Sprint.query.order_by(Sprint.name).all()
    form.sprint_id.choices = [(0, 'Product Backlog')] + [(s.id, s.name) for s in sprints]
    
    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        item.status = form.status.data
        item.priority = form.priority.data
        item.story_points = form.story_points.data
        item.sprint_id = form.sprint_id.data if form.sprint_id.data != 0 else None
        
        db.session.commit()
        flash('Backlog item updated successfully!', 'success')
        if item.sprint_id:
            return redirect(url_for('main.sprint_backlog', sprint_id=item.sprint_id))
        return redirect(url_for('main.product_backlog'))
    
    return render_template('edit_item.html', form=form, item=item, title='Edit Backlog Item')

@main_bp.route('/backlog-item/<int:item_id>/delete', methods=['POST'])
def delete_backlog_item(item_id):
    item = BacklogItem.query.get_or_404(item_id)
    sprint_id = item.sprint_id
    db.session.delete(item)
    db.session.commit()
    flash('Backlog item deleted successfully!', 'success')
    
    if sprint_id:
        return redirect(url_for('main.sprint_backlog', sprint_id=sprint_id))
    return redirect(url_for('main.product_backlog'))

# Sprint Routes
@main_bp.route('/sprints')
def sprints():
    sprints = Sprint.query.order_by(Sprint.name).all()
    return render_template('sprints.html', sprints=sprints)

@main_bp.route('/sprint/add', methods=['GET', 'POST'])
def add_sprint():
    form = SprintForm()
    
    if form.validate_on_submit():
        sprint = Sprint(
            name=form.name.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data
        )
        db.session.add(sprint)
        db.session.commit()
        flash('Sprint added successfully!', 'success')
        return redirect(url_for('main.sprints'))
    
    return render_template('add_sprint.html', form=form, title='Add Sprint')

@main_bp.route('/sprint/<int:sprint_id>')
def sprint_backlog(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    items = BacklogItem.query.filter_by(sprint_id=sprint_id).order_by(BacklogItem.status, BacklogItem.priority).all()
    return render_template('sprint_backlog.html', sprint=sprint, items=items)

@main_bp.route('/sprint/<int:sprint_id>/edit', methods=['GET', 'POST'])
def edit_sprint(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    form = SprintForm(obj=sprint)
    
    if form.validate_on_submit():
        sprint.name = form.name.data
        sprint.start_date = form.start_date.data
        sprint.end_date = form.end_date.data
        sprint.status = form.status.data
        
        db.session.commit()
        flash('Sprint updated successfully!', 'success')
        return redirect(url_for('main.sprints'))
    
    return render_template('edit_sprint.html', form=form, sprint=sprint, title='Edit Sprint')

@main_bp.route('/sprint/<int:sprint_id>/delete', methods=['POST'])
def delete_sprint(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    
    # Move all backlog items back to product backlog
    for item in sprint.backlog_items:
        item.sprint_id = None
    
    db.session.delete(sprint)
    db.session.commit()
    flash('Sprint deleted successfully!', 'success')
    return redirect(url_for('main.sprints'))

# API Routes for drag and drop functionality
@main_bp.route('/api/backlog-item/<int:item_id>/move', methods=['POST'])
def move_backlog_item(item_id):
    item = BacklogItem.query.get_or_404(item_id)
    data = request.get_json()
    
    if 'sprint_id' in data:
        item.sprint_id = data['sprint_id'] if data['sprint_id'] != 0 else None
    
    if 'status' in data:
        item.status = data['status']
    
    db.session.commit()
    return jsonify({'success': True})
