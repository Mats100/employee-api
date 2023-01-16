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
    id: int
    name: str
    profession: str

class UpdateData(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    profession: Optional[str] = None

data = []

@app.get("/")
def read_api(db: Session = Depends((get_db))):
    return db.query(models.Employees).all()

@app.get("/get-employee/{data_id}")
def get_data(data_id: int = Path(None, description="The ID of the employee you would like to view", gt=0)):
    return data[data_id]

@app.get("/get-by-name")
def get_name(name: str = Query(None, title="Name", description="Name of employee")):
    for data_id in data:
        if data[data_id].name == name:
            return data[data_id]
    return {"Data": "Not Found"}

@app.post("/create-record/{data_id}")
def create_record(data_id: int, employee: Employee, db: Session = Depends(get_db)):
   Employees_model = models.Employees()
   Employees_model.id = employee.id
   Employees_model.name = employee.name
   Employees_model.profession = employee.profession
   db.add(Employees_model)
   db.commit()
   return data[data_id]

@app.put("/update-item/{data_id}")
def update_item(data_id: int, employee: Employee, db: Session = Depends(get_db)):
    Employee_model = db.query(models.Employees).filter(models.Employees.id == data_id).first()
    if Employee_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID{data_id}: Does not exist"
        )
    Employee_model.name = employee.name
    Employee_model.profession =employee.profession

    db.add(Employee_model)
    db.commit()
    return employee
@app.delete("/{delete-id}")
def delete_id(data_id: int = Query(..., description="The ID of the Employee you want to delete")):
    if data_id not in data:
        return {"Error": "ID does not exist"}
    del data[data_id]
    return {"Success": "Item deleted Successfully"}
