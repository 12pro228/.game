import json
from datetime import datetime, timezone
from pathlib import Path


DATA_DIRECTORY = Path(__file__).resolve().parent
PLAYER_FILE = DATA_DIRECTORY / "player_name.json"
SCORES_FILE = DATA_DIRECTORY / "leaderboard.json"


def get_player_name():
    if not PLAYER_FILE.exists():
        return "Player"
    player_data = json.loads(PLAYER_FILE.read_text(encoding="utf-8"))
    name = player_data.get("name", "Player")
    return name if isinstance(name, str) and name.strip() else "Player"


def save_player_name(name):
    PLAYER_FILE.write_text(
        json.dumps({"name": name}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_scores():
    if not SCORES_FILE.exists():
        return []
    data = json.loads(SCORES_FILE.read_text(encoding="utf-8"))
    scores = data.get("scores")
    if not isinstance(scores, list):
        raise ValueError("Leaderboard data must contain a scores list.")
    return scores


def record_score(name, score, result):
    scores = load_scores()
    record = {
        "name": name,
        "score": score,
        "result": result,
        "played_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    scores.append(record)
    temporary_file = SCORES_FILE.with_suffix(".tmp")
    temporary_file.write_text(
        json.dumps({"scores": scores}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary_file.replace(SCORES_FILE)
    return record
