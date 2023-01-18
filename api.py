from fastapi import FastAPI, Query, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app = FastAPI()


class Employee(BaseModel):
    id: int
    name: str
    profession: str


class UpdateData(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    profession: Optional[str] = None



@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Employees).all()


@app.post("/create-record/")
def create_record(employee: Employee, db: Session = Depends(get_db)):
    employee_model = models.Employees(name=employee.name, profession=employee.profession)
    db.add(employee_model)
    db.commit()
    db.refresh(employee_model)


@app.put("/update-user{data_id}")
def update_user(employee: Employee, db: Session = Depends(get_db)):
    employee_model = db.query(models.Employees).filter(models.Employees.id == employee.id).first()
    if employee_model is None:
        raise HTTPException(
            status_code=404,
        )
    employee_model.name = employee.name
    employee_model.profession = employee.profession

    db.add(employee_model)
    db.commit()
    db.refresh(employee_model)
    return employee_model