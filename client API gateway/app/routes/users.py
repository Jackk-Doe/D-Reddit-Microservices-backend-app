from fastapi import APIRouter

router = APIRouter()

@router.get('')
async def testRoute():
    return {"TEST":"Hello from USER route"}