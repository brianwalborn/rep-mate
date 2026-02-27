from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.crud import templates as crud
from app.schemas.template import (
    TemplateCreate,
    TemplateUpdate,
    TemplateOut,
    TemplateSummary
)
from app.models.exercise import Exercise

router = APIRouter(prefix="/templates", tags=["Templates"])


@router.get("", response_model=List[TemplateOut])
def get_templates(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all templates for the current user"""
    templates = crud.list_templates(db, user.id)
    
    # Enrich template exercises with exercise details
    for template in templates:
        for template_ex in template.exercises:
            exercise = db.query(Exercise).filter(
                Exercise.id == template_ex.exercise_id
            ).first()
            if exercise:
                template_ex.exercise_name = exercise.name
                template_ex.equipment = exercise.equipment.name if exercise.equipment else None
                template_ex.muscles = exercise.muscles
    
    return templates


@router.get("/summary", response_model=List[TemplateSummary])
def get_templates_summary(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get template summaries (lightweight)"""
    return crud.list_templates_summary(db, user.id)


@router.get("/{template_id}", response_model=TemplateOut)
def get_template(
    template_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a single template by ID"""
    template = crud.get_template(db, template_id, user.id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Enrich template exercises with exercise details
    for template_ex in template.exercises:
        exercise = db.query(Exercise).filter(
            Exercise.id == template_ex.exercise_id
        ).first()
        if exercise:
            template_ex.exercise_name = exercise.name
            template_ex.equipment = exercise.equipment.name if exercise.equipment else None
            template_ex.muscles = exercise.muscles
    
    return template


@router.post("", response_model=TemplateOut)
def create_template(
    template: TemplateCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new template"""
    new_template = crud.create_template(db, template, user.id)
    
    # Enrich with exercise details
    for template_ex in new_template.exercises:
        exercise = db.query(Exercise).filter(
            Exercise.id == template_ex.exercise_id
        ).first()
        if exercise:
            template_ex.exercise_name = exercise.name
            template_ex.equipment = exercise.equipment.name if exercise.equipment else None
            template_ex.muscles = exercise.muscles
    
    return new_template


@router.put("/{template_id}", response_model=TemplateOut)
def update_template(
    template_id: str,
    template: TemplateUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a template"""
    updated_template = crud.update_template(db, template_id, template, user.id)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Enrich with exercise details
    for template_ex in updated_template.exercises:
        exercise = db.query(Exercise).filter(
            Exercise.id == template_ex.exercise_id
        ).first()
        if exercise:
            template_ex.exercise_name = exercise.name
            template_ex.equipment = exercise.equipment.name if exercise.equipment else None
            template_ex.muscles = exercise.muscles
    
    return updated_template


@router.delete("/{template_id}")
def delete_template(
    template_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a template"""
    success = crud.delete_template(db, template_id, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return {"message": "Template deleted successfully"}
