# NFL Fantasy Football Schedule Parsers - Developer Overview

This project provides two Python scripts for scraping and parsing NFL.com Fantasy Football league data. It allows users to view their personal team's season schedule and results, or get a league-wide overview of past week's results and current week's matchups, including detailed starting lineups and owner information. The core functionality relies on web scraping NFL.com Fantasy pages to extract and display relevant fantasy football data.

## Architecture

The project employs a modular architecture centered around a common utility module (`nfl_common.py`) which handles the heavy lifting of web scraping and HTML parsing using `requests` and `BeautifulSoup4`. Two main application scripts (`my_team_schedule.py` and `league_matchups.py`) then import and utilize these common functions to fetch specific types of data (individual team schedules or league-wide matchups) and present them to the user. This design separates data acquisition and parsing logic from application-specific display logic, promoting reusability and maintainability. Data is primarily extracted from HTML content, meaning the system is dependent on the consistent structure of NFL.com's fantasy football pages.

## Key Files

*   **`my_team_schedule.py`**:
    *   **Purpose**: Fetches and displays a specific user's fantasy team schedule, including past results, the current week's matchup, and upcoming games.
    *   **Key Functions**:
        *   `parse_schedule_data(html_content: str) -> List[Dict[str, str]]`: Parses the HTML of a team's schedule page to extract individual game details (week, opponent, scores, status, result). It identifies current, past, and future games.
        *   `display_schedule(schedule_data: List[Dict[str, str]], team_name: str) -> None`: Formats and prints the extracted schedule data to the console, categorizing games into current week, upcoming, and recent results.
    *   **Dependencies**: Relies on `nfl_common.fetch_schedule_html` to get page content and `nfl_common.extract_team_name` for display. Uses `BeautifulSoup4` internally for its specific parsing needs.

*   **`league_matchups.py`**:
    *   **Purpose**: Fetches and displays previous week's results and the current week's matchups for all teams in a league, complete with owner names and detailed starting lineups, including projected points.
    *   **Key Functions**:
        *   `get_current_week_number(html_content: str) -> int`: Extracts the current week number from the main league page HTML to navigate correctly for past/current week data.
        *   `fetch_previous_week_matchups(base_url: str, current_week: int, cookies: str) -> List[Dict[str, str]]`: Constructs a URL for the previous week and fetches its matchup data using `nfl_common` functions.
        *   `display_week_matchups(matchups: List[Dict[str, str]], week_label: str, team_rosters: Dict[str, Dict[str, any]] = None, show_rosters: bool = True) -> None`: Formats and prints matchups. It can enrich the display with owner names, final scores/upcoming status, and detailed side-by-side starting lineups with player points/projections.
    *   **Dependencies**: Heavily uses `nfl_common` for `fetch_schedule_html`, `extract_team_ids_from_matchups`, `parse_current_week_matchups`, `fetch_team_roster`, and `fetch_team_projections` (though `fetch_team_projections` is present in `league_matchups.py` import, its actual implementation or usage for `fetch_team_projections` is not fully shown in `nfl_common.py` or `league_matchups.py` snippet).

*   **`nfl_common.py`**:
    *   **Purpose**: A shared utility module containing common functions for HTTP requests, HTML parsing, and data extraction, used by both `my_team_schedule.py` and `league_matchups.py`.
    *   **Key Functions**:
        *   `fetch_schedule_html(url: str, cookies: str) -> str`: Performs an authenticated HTTP GET request to the specified URL using `requests`, setting a User-Agent header and including provided cookies for session authentication. Raises `requests.RequestException` on failure.
        *   `extract_team_ids_from_matchups(html_content: str) -> Dict[str, str]`: Parses HTML to map team names to their numerical team IDs, crucial for constructing team-specific URLs.
        *   `parse_team_roster(html_content: str) -> Dict[str, List[Dict[str, str]]]:` Extracts a team's full roster (starters and bench) from a team-specific page, including player position, name, ID, team, and fantasy points.
        *   `extract_team_owner(html_content: str) -> str`: Retrieves the owner's name from a team's page.
        *   `fetch_team_roster(team_id: str, cookies: str) -> Dict[str, any]`: Orchestrates fetching a team's specific page, then parses its roster and owner name.
        *   `parse_current_week_matchups(html_content: str) -> List[Dict[str, str]]`: Extracts general matchup data (team names, scores/status, week) for all games displayed on a scoreboard section.
        *   `extract_team_name(html_content: str) -> str`: Identifies and returns the user's team name from the HTML content.
    *   **Dependencies**: `requests` for HTTP and `beautifulsoup4` (with `lxml` for performance) for HTML parsing.

*   **`pyproject.toml`**: Defines project metadata and dependencies. It specifies `requests`, `beautifulsoup4`, and `lxml` as core requirements, along with a Python version constraint.

## How to Run

This project uses `uv` for dependency management, which is recommended for faster operations.

1.  **Install `uv` (if not already installed)**:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Install project dependencies**:
    ```bash
    uv sync
    ```
    Alternatively, if not using `uv`:
    ```bash
    pip install requests beautifulsoup4 lxml
    ```

3.  **Run the scripts**:

    *   **Personal Team Schedule**:
        ```bash
        uv run my_team_schedule.py
        ```

    *   **League-Wide Matchups**:
        ```bash
        uv run league_matchups.py
        ```

## Configuration

The scripts require specific configuration parameters that are currently **hardcoded** within `my_team_schedule.py` and `league_matchups.py`:

*   **Cookies**: Both scripts contain a `cookies` variable (e.g., `cookies = ''`). This string needs to be updated with your current NFL.com Fantasy session cookies for successful authentication and data fetching. Without valid cookies, the scripts will likely fail to retrieve personalized or league-specific data.
*   **League ID**: The `base_url` or `url` variables in both scripts point to a specific league ID (e.g., `12698811`). To use the scripts with a different fantasy league, update the `league/YOUR_LEAGUE_ID` segment in the URL definitions within each script.

These parameters are *not* environment variables; they must be changed directly in the Python source files.

## How to Test

The `README.md` suggests testing by importing and utilizing functions from `nfl_common.py` directly with local HTML files. This allows for isolated testing of the parsing logic without making live HTTP requests to NFL.com.

To do this:
1.  Save relevant NFL Fantasy page HTML (e.g., `schedule.html`, `team.html` as indicated in `resources/`) locally.
2.  In a separate Python script or interactive session, import functions from `nfl_common.py`.
3.  Load the local HTML content from your saved files.
4.  Call the `nfl_common` parsing functions (e.g., `parse_schedule_data`, `parse_team_roster`, `parse_current_week_matchups`) with the loaded HTML content as input.
5.  Verify the output matches expected data structures.