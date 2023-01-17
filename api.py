from fastapi import FastAPI, Path, Query, Depends, HTTPException
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
    name: str
    profession: str


class UpdateData(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    profession: Optional[str] = None



@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Employees).all()


@app.get("/get-employee/")
def get_data(employee: Employee = Path(None, description="The ID of the employee you would like to view", gt=0,)):
    return employee


@app.get("/get-by-name")
def get_name(name: str = Query(None, title="Name", description="Name of employee"), db: Session = Depends(get_db),):
    for data_id in data:
        if get_db() == name:
            return db.query()
    return {"Data": "Not Found"}


@app.post("/create-record/")
def create_record(employee: Employee, db: Session = Depends(get_db)):
    employee_model = models.Employees(name=employee.name, profession=employee.profession)
    db.add(employee_model)
    db.commit()
    db.refresh(employee_model)


@app.put("/update-item/{data_id}")
def update_item(employee: Employee, db: Session = Depends(get_db)):
    employee_model = db.query(models.Employees).filter(models.Employees.id == id).first()
    if employee_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID{employee}: Does not exist"
        )
    employee_model.name = employee.name
    employee_model.profession = employee.profession

    db.add(employee_model)
    db.commit()
    return employee


@app.delete("/{delete-id}")
def delete_id(employee: int = Query(..., description="The ID of the Employee you want to delete"), db: Session = Depends(get_db)):
    if Employees.id not in get_db():
        return {"Error": "ID does not exist"}
    del Employees.id
    return {"Success": "Item deleted Successfully"}
