# Developer Overview: NFL Fantasy Schedule Parsers

This project provides two Python scripts designed to fetch, parse, and display NFL Fantasy league data from the NFL.com Fantasy website. It focuses on extracting both individual team schedules and league-wide matchup details, including roster information and scores, by scraping HTML content.

## Architecture

The project follows a modular architecture, separating core web scraping and parsing logic from application-specific display functions.

1.  **Core Utilities (`nfl_common.py`):** This module acts as the backbone, handling all low-level tasks such as making HTTP requests, authenticating with cookies, and parsing specific HTML elements to extract raw data like team names, IDs, scores, and player rosters. It provides reusable functions for fetching and parsing, ensuring consistency and maintainability.
2.  **Application Scripts (`my_team_schedule.py`, `league_matchups.py`):** These are the entry points for the user. They import and orchestrate the common functions to gather the necessary data, then process and format it for console output according to their specific purpose (personal schedule vs. league matchups).
3.  **Dependency Management:** `uv` is used for efficient dependency management, ensuring all required libraries (`requests`, `beautifulsoup4`, `lxml`) are installed and managed properly.

The general data flow involves:
*   A script initiates a request to an NFL Fantasy URL.
*   `nfl_common.py` fetches the HTML content, potentially using provided cookies for authentication.
*   `nfl_common.py` then parses the HTML to extract specific data points (e.g., current week matchups, team rosters, scores).
*   The application script receives the structured data and formats it for display to the user.

## Key Files

*   **`my_team_schedule.py`**:
    *   **Purpose:** Fetches and displays a single team's full season schedule, including past game results, the current week's matchup, and upcoming games.
    *   **Key Functions:**
        *   `parse_schedule_data(html_content: str) -> List[Dict[str, str]]`: Extracts individual team schedule details from HTML.
        *   `display_schedule(schedule_data: List[Dict[str, str]], team_name: str)`: Formats and prints the personal team schedule.
*   **`league_matchups.py`**:
    *   **Purpose:** Fetches and displays previous week's results and current week's matchups for all teams in the league, including owner names and starting lineups with fantasy points/projections.
    *   **Key Functions:**
        *   `get_current_week_number(html_content: str) -> int`: Extracts the current fantasy week number from the page.
        *   `fetch_previous_week_matchups(base_url: str, current_week: int, cookies: str)`: Fetches and parses data for the week prior to the current one.
        *   `display_week_matchups(...)`: Formats and prints league-wide matchup details, including side-by-side roster comparisons.
*   **`nfl_common.py`**:
    *   **Purpose:** Contains shared utility functions for HTTP requests, HTML parsing, and data extraction, reusable by both application scripts.
    *   **Key Functions:**
        *   `fetch_schedule_html(url: str, cookies: str) -> str`: Performs authenticated HTTP GET requests to fetch HTML content.
        *   `extract_team_ids_from_matchups(html_content: str) -> Dict[str, str]`: Maps team names to their unique NFL Fantasy IDs.
        *   `parse_team_roster(html_content: str) -> Dict[str, List[Dict[str, str]]]`: Parses a team's page to extract starter and bench player data.
        *   `extract_team_owner(html_content: str) -> str`: Extracts the owner's name from a team's page.
        *   `fetch_team_roster(team_id: str, cookies: str) -> Dict[str, any]`: Combines roster and owner extraction for a given team ID.
        *   `parse_current_week_matchups(html_content: str) -> List[Dict[str, str]]`: Extracts matchup details (teams, scores) for a given week.
        *   `extract_team_name(html_content: str) -> str`: Extracts the primary team name displayed on a schedule page.
*   **`pyproject.toml`**: Defines project metadata, Python version requirement (`>=3.10`), and lists core dependencies.
*   **`resources/`**: Directory containing example HTML files (`schedule.html`, `team.html`) that can be used for local testing of parsing functions without live web requests.

## How to Run

### Prerequisites

*   Python 3.10 or higher.
*   `uv` (recommended) or `pip` for dependency management.

### Installation

1.  **Install `uv` (if not already installed):**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  **Install project dependencies:**
    ```bash
    uv sync
    ```
    Alternatively, using `pip`:
    ```bash
    pip install requests beautifulsoup4 lxml
    ```

### Usage

**1. Personal Team Schedule:**
To view your individual team's schedule:
```bash
uv run my_team_schedule.py
```

**2. League-Wide Matchups:**
To view league-wide matchups for the previous and current week, including rosters:
```bash
uv run league_matchups.py
```

## Configuration

Both scripts require specific configuration to function correctly with your NFL Fantasy league.

*   **Cookies:**
    *   The `cookies` variable in `my_team_schedule.py`, `league_matchups.py`, and `nfl_common.py` (specifically `fetch_team_roster`) must be updated with your active NFL.com fantasy session cookies for authenticated access. This typically involves copying the `cookie` header value from your browser's developer tools after logging into fantasy.nfl.com.
    *   Example: `cookies = 'NFL_FANTASY_SESSION=...; other_cookie=...;'`
*   **League ID:**
    *   The hardcoded league ID `12698811` in the `url` variables within `my_team_schedule.py`, `league_matchups.py`, and `nfl_common.py` (`fetch_team_roster` function) needs to be changed to your specific league's ID.
    *   Example: Change `https://fantasy.nfl.com/league/12698811` to `https://fantasy.nfl.com/league/YOUR_LEAGUE_ID`.

## How to Test

Parsing functions can be tested locally using the static HTML files provided in the `resources/` directory. This allows for development and debugging without making live web requests or relying on active session cookies.

1.  **Import the desired functions:**
    ```python
    from nfl_common import parse_current_week_matchups, parse_team_roster
    from my_team_schedule import parse_schedule_data
    ```
2.  **Load a local HTML file:**
    ```python
    with open('resources/schedule.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    ```
3.  **Call the parsing function with the loaded content:**
    ```python
    schedule_data = parse_schedule_data(html_content)
    print(schedule_data)
    ```