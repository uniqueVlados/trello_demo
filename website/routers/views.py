from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from . import templates
from ..database import get_db
from ..models import Board, Task

router = APIRouter(tags=["views"])


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/view_board")
async def view_board(request: Request, db: Session = Depends(get_db)):
    boards = db.query(Board).all()
    return templates.TemplateResponse("view_board.html", {"request": request, "boards": boards})


@router.post("/add_task/{board_id}")
async def add_task(board_id: int, request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    text = form.get("text")
    new_task = Task(text=text, board_id=board_id)
    db.add(new_task)
    db.commit()
    return RedirectResponse(url="/view_board", status_code=status.HTTP_302_FOUND)


@router.get("/remove_task/{task_id}")
async def remove_task(task_id: int, db: Session = Depends(get_db)):
    find_task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(find_task)
    db.commit()
    return RedirectResponse(url="/view_board", status_code=status.HTTP_302_FOUND)


@router.get("/remove_board/{board_id}")
async def remove_board(board_id: int, db: Session = Depends(get_db)):
    find_board = db.query(Board).filter(Board.id == board_id).first()
    db.delete(find_board)
    db.commit()
    return RedirectResponse(url="/view_board", status_code=status.HTTP_302_FOUND)


@router.post("/add_board")
async def add_board(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    text = form.get("board_title")
    new_board = Board(title=text)
    db.add(new_board)
    db.commit()
    return RedirectResponse(url="/view_board", status_code=status.HTTP_302_FOUND)


@router.get("/add_board")
async def add_board(request: Request):
    return templates.TemplateResponse("add_board.html", {"request": request})


@router.get("/save_checkbox/{task_id}")
async def save_checkbox(task_id: int, db: Session = Depends(get_db)):
    find_task = db.query(Task).filter(Task.id == task_id).first()
    find_task.is_complete = not find_task.is_complete
    db.commit()
    return RedirectResponse(url="/view_board", status_code=status.HTTP_302_FOUND)


# @router.get("/rename_board/{board_id}")
# async def rename_board(board_id: int, db: Session = Depends(get_db)):
#     find_board = db.query(Board).filter(Board.id == board_id).first()
#     find_board.title =
#     db.commit()
#     return RedirectResponse(url="/view_board", status_code=status.HTTP_302_FOUND)