from typing import Union, Dict, Any
import json
from crewai.tools import tool
from tools.web.youtube.youtube_controller import YouTubeController

_active = {"yt": None}
def _ctrl(headless: bool = False) -> YouTubeController:
    if _active["yt"] is None:
        _active["yt"] = YouTubeController(headless=headless)
    return _active["yt"]

@tool("youtube_control")
def youtube_control(payload: Union[str, Dict[str, Any]]) -> str:
    """
    Control YouTube via Selenium.

    Pass a JSON string or dict with keys:
      action: one of [play_query, play_url, play, pause, toggle, seek, set_time,
                      next, prev, mute, volume, captions, theater, fullscreen,
                      like, subscribe, info, close]
      query: str (for play_query)
      url: str (for play_url)
      headless: bool (default False if you want audio/visible browser)
      seconds: int (for seek/set_time)
      percent: int 0..100 (for volume)

    Examples:
      {"action":"play_query","query":"Despacito","headless":false}
      {"action":"volume","percent":20}
      {"action":"info"}
      {"action":"close"}
    """
    # Normalize input
    if isinstance(payload, str):
        try:
            data = json.loads(payload)
        except Exception:
            return "Error: payload must be JSON or dict"
    else:
        data = dict(payload or {})

    action   = str(data.get("action", "")).lower()
    query    = data.get("query", "") or ""
    url      = data.get("url", "") or ""
    headless = bool(data.get("headless", False))
    seconds  = data.get("seconds", 0)
    percent  = data.get("percent", 50)

    yt = _ctrl(headless=headless)

    try:
        if action == "play_query": yt.play_query(query);                     return "Playing query."
        if action == "play_url":   yt.play_url(url);                         return "Playing URL."
        if action == "play":       yt.play();                                return "Play."
        if action == "pause":      yt.pause();                               return "Pause."
        if action == "toggle":     yt.toggle_play_pause();                   return "Toggled."
        if action == "seek":       yt.seek(int(seconds));                    return "Seeked."
        if action == "set_time":   yt.set_time_exact(float(seconds));        return "Time set."
        if action == "next":       yt.next_video();                          return "Next."
        if action == "prev":       yt.previous_video();                      return "Previous."
        if action == "mute":       yt.mute_toggle();                         return "Mute toggled."
        if action == "volume":     yt.set_volume_percent(int(percent));      return "Volume set."
        if action == "captions":   yt.captions_toggle();                     return "Captions toggled."
        if action == "theater":    yt.theater_toggle();                      return "Theater toggled."
        if action == "fullscreen": yt.fullscreen_toggle();                   return "Fullscreen toggled."
        if action == "like":       yt.like();                                return "Liked."
        if action == "subscribe":  yt.subscribe();                           return "Subscribed."
        if action == "info":       return json.dumps(yt.info())
        if action == "close":      yt.close(); _active["yt"] = None;         return "Closed."
        return f"Unknown action: {action}"
    except Exception as e:
        return f"Error: {e}"
