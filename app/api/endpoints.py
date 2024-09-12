from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi.responses import HTMLResponse, JSONResponse
from app.db.database import get_db
from fastapi.templating import Jinja2Templates
from app.core.game_logic import determine_winner
from app.schemas.game import GamePlay
from app.db.models import GameResult as GameResultModel
import random
from pathlib import Path

router = APIRouter()

static_dir = Path(__file__).parent.parent.parent / "static"
templates = Jinja2Templates(directory=static_dir)

# decided to make a pretty simple state machine
game_state = {
    "player1": None,
    "player2": None,
    "mode": None,
    "player1_choice": None,
    "player2_choice": None,
    "player1_score": 0,
    "player2_score": 0
}

# starting page - the only page that shows as html
# all next sending just json responses
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# starting game, checking ef users gave their names,
# game state currently have names and mode
# returning game state to a front side
@router.post("/start_game")
async def start_game(request: Request):
    data = await request.json()

    game_state["player1"] = data["player1"]
    game_state["mode"] = data["mode"]
    game_state["player2"] = data["player2"] if data["mode"] == "player" else "Computer"

    # made checking field on a backend for a purpose
    # usually it woul be done on front too, but I decided not to spent tome to make frontend scenarios
    if game_state["player1"] == "" or game_state["player2"] == "":
        return JSONResponse(content={
            "message": "Please insert names"
        })

    # rewriting scores because I have a button to start new game
    game_state["player1_score"] = 0
    game_state["player2_score"] = 0

    return JSONResponse(content={
        "message": "Game started",
        "player1_score": game_state["player1_score"],
        "player2_score": game_state["player2_score"]
    })

# playing game!

@router.post("/play")
async def play(game_play: GamePlay):
    player = game_play.player

    # adding choise
    if player == "player1":
        game_state["player1_choice"] = game_play.choice
    else:
        game_state["player2_choice"] = game_play.choice

    # if playng with computer creating computers choice
    if game_state["mode"] == "computer" and player == "player1":
        game_state["player2_choice"] = random.choice(["rock", "paper", "scissors"])

    # if have both deciding who won
    if game_state["player1_choice"] and game_state["player2_choice"]:
        result = determine_winner(game_state["player1_choice"], game_state["player2_choice"])
        # some tweacking because I don't like to return messages from separate functions, only codes
        if result == 1:
            game_state["player1_score"] += 1
            human_result = f"{game_state['player1']} wins!"
        elif result == 2:
            game_state["player2_score"] += 1
            human_result = f"{game_state['player2']} wins!"
        else:
            human_result = "It's a tie!"

        # creating right responce
        response_data = {
            "result": human_result,
            "player1_choice": game_state["player1_choice"],
            "player2_choice": game_state["player2_choice"],
            "player1": game_state["player1"],
            "player2": game_state["player2"],
            "player1_score": game_state["player1_score"],
            "player2_score": game_state["player2_score"]
        }

        # cleaning for a new potential game
        game_state["player1_choice"] = None
        game_state["player2_choice"] = None

        return response_data
    else:
        # well, whis happend a few times during debuggig, so I'll just leave it here
        return {"message": "Waiting for other player"}

# saving game into database
@router.post("/save_game")
async def save_game(db: Session = Depends(get_db)):
    new_game = GameResultModel(
        player1=game_state["player1"],
        player2=game_state["player2"],
        player1_score=game_state["player1_score"],
        player2_score=game_state["player2_score"],
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return {"message": "Game saved successfully"}

# showing the list of saving games
@router.get("/game_history")
async def game_history(db: Session = Depends(get_db)):
    # showing from new to old with filter by names
    query = db.query(GameResultModel).order_by(GameResultModel.played_at.desc())
    query = query.filter(and_(*[GameResultModel.player1.ilike(f"%{game_state["player1"]}%"),GameResultModel.player2.ilike(f"%{game_state["player2"]}%")]))
    games = query.limit(10).all()

    # creating result
    res = [{"player1": game.player1, "player2": game.player2,
             "player1_score": game.player1_score, "player2_score": game.player2_score, "played_at": game.played_at} for
            game in games]
    return res
