from fastapi import FastAPI
from api import v1_device, v1_task, v1_log,v1_inventory

app = FastAPI(title="Ticket Cluster System")

# 像拼积木一样把各模块插入
app.include_router(v1_device.router, prefix="/api/v1")
app.include_router(v1_task.router, prefix="/api/v1")
app.include_router(v1_log.router, prefix="/api/v1")

app.include_router(v1_inventory.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "running", "service": "Ticket Cluster API"}