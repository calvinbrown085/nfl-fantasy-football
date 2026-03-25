# NFL Fantasy Schedule Parsers - Developer Guide

This project provides two Python scripts for scraping and parsing NFL.com Fantasy Football league data. It allows users to view their personal team's schedule, including past results and upcoming games, or to get a comprehensive league-wide overview of previous week's results and current week's matchups, complete with owner names and starting lineups.

## Architecture

The application follows a modular architecture primarily focused on web scraping.
*   **Core Logic:** Two main scripts, `my_team_schedule.py` and `league_matchups.py`, encapsulate the specific logic for personal schedules and league-wide views, respectively.
*   **Shared Utilities:** `nfl_common.py` acts as a utility module, centralizing common functionalities such as HTML fetching (`fetch_schedule_html`), team ID extraction, generic matchup parsing (`parse_current_week_matchups`), team roster parsing (`parse_team_roster`), and owner name extraction. This promotes code reuse and maintainability for the web scraping operations.
*   **Data Flow:** Both main scripts initiate by fetching HTML content via `nfl_common.py`, then parse the data using a combination of their own parsing functions and those provided by `nfl_common.py`. The parsed data is then formatted and displayed to the console.
*   **Dependencies:** `requests` handles HTTP requests, while `beautifulsoup4` (with `lxml`) is used for robust HTML parsing.

## Key Files

*   `my_team_schedule.py`: The entry point for fetching and displaying a single fantasy team's entire season schedule. It parses week-by-week data, distinguishing between completed games (with scores) and upcoming matchups.
*   `league_matchups.py`: The entry point for retrieving and presenting league-wide information. It identifies the current week, fetches previous week's results, and details current week's matchups including team owners and starting player lineups with projected points.
*   `nfl_common.py`: Contains reusable functions for interacting with NFL.com Fantasy. This includes:
    *   `fetch_schedule_html`: Handles HTTP requests with appropriate headers and cookie authentication.
    *   `extract_team_ids_from_matchups`: Maps team names to their unique numerical IDs.
    *   `parse_current_week_matchups`: Extracts matchup details (teams, scores, links) from scoreboard HTML.
    *   `parse_team_roster`: Parses a team's dedicated page to list starters and bench players with their positions and fantasy points.
    *   `extract_team_owner`: Retrieves the owner's name from a team page.
    *   `extract_team_name`: Fetches the main team name from the schedule page.
*   `pyproject.toml`: Defines project metadata and manages core Python dependencies (`requests`, `beautifulsoup4`, `lxml`).
*   `resources/`: A directory intended to hold local HTML files (`schedule.html`, `team.html`) that can be used for offline testing of parsing logic without hitting the live NFL.com servers.

## How to Run

To set up and run the NFL Fantasy Schedule Parsers:

1.  **Install `uv` (if not already installed):**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Install Project Dependencies:**
    Navigate to the project's root directory and install the required Python packages:
    ```bash
    uv sync
    ```
    *Alternatively, if not using `uv`:*
    ```bash
    pip install requests beautifulsoup4 lxml
    ```

3.  **Configure Authentication and League ID** (see "Configuration" section below).

4.  **Run Scripts:**

    *   **Personal Team Schedule:**
        ```bash
        uv run my_team_schedule.py
        ```

    *   **League-Wide Matchups:**
        ```bash
        uv run league_matchups.py
        ```

## Configuration

This project does not use environment variables. Instead, critical configuration parameters are hardcoded within the Python scripts:

*   **Authentication Cookies (`cookies` variable):** Both `my_team_schedule.py` and `league_matchups.py` contain a `cookies` variable that *must be updated* with your current NFL.com fantasy session cookies for the scripts to function correctly. This is essential for authenticated access to your league data.
*   **League ID:** The base URL for the fantasy league, e.g., `https://fantasy.nfl.com/league/12698811`, is hardcoded in both `my_team_schedule.py` and `league_matchups.py`. To use the scripts with a different league, modify `12698811` to your specific league ID within the `base_url` or `url` variables in both scripts.

## How to Test

The project supports testing of its parsing logic using local HTML files. This is particularly useful for development and debugging without making repeated requests to NFL.com.

1.  **Save HTML:** Place relevant HTML content (e.g., a schedule page, a team roster page) into the `resources/` directory. The README hints at `resources/schedule.html` and `resources/team.html`.
2.  **Direct Function Calls:** Import and call the parsing functions (e.g., `parse_schedule_data`, `parse_current_week_matchups`, `parse_team_roster`, `extract_team_owner`) from `nfl_common.py` or the main scripts directly, passing the locally saved HTML content as a string.

    *Example (conceptual):*
    ```python
    from nfl_common import parse_current_week_matchups
    
    with open('resources/schedule.html', 'r', encoding='utf-8') as f:
        local_html = f.read()
    
    matchups = parse_current_week_matchups(local_html)
    for m in matchups:
        print(m)
    ```

This allows for isolated unit testing of the parsing logic against known inputs.