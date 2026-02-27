from sqlalchemy.orm import Session, joinedload
from app.models.template import Template, TemplateExercise, TemplateSet
from app.models.exercise import Exercise
from app.schemas.template import TemplateCreate, TemplateUpdate, TemplateSummary
from typing import List


def create_template(db: Session, payload: TemplateCreate, user_id: str) -> Template:
    """Create a new template with exercises and sets"""
    template = Template(
        user_id=user_id,
        name=payload.name,
        description=payload.description
    )
    db.add(template)
    db.flush()

    for ex in payload.exercises:
        template_ex = TemplateExercise(
            template_id=template.id,
            exercise_id=ex.exercise_id,
            order=ex.order,
            notes=ex.notes
        )
        db.add(template_ex)
        db.flush()

        for s in ex.sets:
            db.add(
                TemplateSet(
                    template_exercise_id=template_ex.id,
                    set_number=s.set_number,
                    weight=s.weight,
                    reps=s.reps,
                    unit=s.unit
                )
            )

    db.commit()
    db.refresh(template)
    return template


def get_template(db: Session, template_id: str, user_id: str) -> Template:
    """Get a single template by ID with all related data"""
    return db.query(Template).options(
        joinedload(Template.exercises).joinedload(TemplateExercise.exercise),
        joinedload(Template.exercises).joinedload(TemplateExercise.sets)
    ).filter(
        Template.id == template_id,
        Template.user_id == user_id
    ).first()


def list_templates(db: Session, user_id: str) -> List[Template]:
    """List all templates for a user"""
    return db.query(Template).options(
        joinedload(Template.exercises).joinedload(TemplateExercise.exercise),
        joinedload(Template.exercises).joinedload(TemplateExercise.sets)
    ).filter(
        Template.user_id == user_id
    ).order_by(Template.created_at.desc()).all()


def list_templates_summary(db: Session, user_id: str) -> List[dict]:
    """List templates with summary info (lighter weight)"""
    templates = db.query(Template).filter(
        Template.user_id == user_id
    ).order_by(Template.created_at.desc()).all()
    
    return [
        {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "exercise_count": len(t.exercises),
            "created_at": t.created_at,
            "updated_at": t.updated_at
        }
        for t in templates
    ]


def update_template(db: Session, template_id: str, payload: TemplateUpdate, user_id: str) -> Template:
    """Update a template"""
    template = get_template(db, template_id, user_id)
    if not template:
        return None

    # Update basic fields
    if payload.name is not None:
        template.name = payload.name
    if payload.description is not None:
        template.description = payload.description

    # If exercises are provided, replace all exercises
    if payload.exercises is not None:
        # Delete existing exercises and sets (cascade will handle sets)
        db.query(TemplateExercise).filter(
            TemplateExercise.template_id == template_id
        ).delete()
        
        # Add new exercises
        for ex in payload.exercises:
            template_ex = TemplateExercise(
                template_id=template.id,
                exercise_id=ex.exercise_id,
                order=ex.order,
                notes=ex.notes
            )
            db.add(template_ex)
            db.flush()

            for s in ex.sets:
                db.add(
                    TemplateSet(
                        template_exercise_id=template_ex.id,
                        set_number=s.set_number,
                        weight=s.weight,
                        reps=s.reps,
                        unit=s.unit
                    )
                )

    db.commit()
    db.refresh(template)
    return template


def delete_template(db: Session, template_id: str, user_id: str) -> bool:
    """Delete a template"""
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == user_id
    ).first()
    
    if not template:
        return False

    db.delete(template)
    db.commit()
    return True
