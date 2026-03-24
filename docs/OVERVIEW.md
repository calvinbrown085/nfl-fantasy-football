# NFL Fantasy Football Schedule Parsers

This project provides two Python scripts for fetching and parsing NFL Fantasy Football league data directly from the NFL.com Fantasy website. It allows users to view their personal team's schedule and results, or an overview of all league matchups, including past results and current week's starting lineups with owner information.

## Architecture

The project employs a modular architecture with a clear separation of concerns:
*   **`nfl_common.py`**: This central utility module handles all low-level web scraping and HTML parsing tasks. It contains functions for fetching HTML content, extracting specific data points (like team IDs, player rosters, owner names, and matchup details) from raw HTML using `requests` and `BeautifulSoup`.
*   **`my_team_schedule.py`**: This script leverages functions from `nfl_common.py` to retrieve and parse data relevant to a single user's team. It then formats and displays the personal team's schedule, highlighting past results, the current week's game, and upcoming matchups.
*   **`league_matchups.py`**: This script also utilizes `nfl_common.py` to fetch league-wide data. It orchestrates the retrieval of previous week's results, current week's matchups, and detailed roster information (including owner names and starting lineups) for all teams in the league, presenting a comprehensive overview.

Both main scripts operate by making HTTP requests to NFL.com's fantasy pages, parsing the returned HTML, and extracting the relevant structured data for display.

## Key Files

*   **`my_team_schedule.py`**:
    *   **Purpose**: Displays your specific fantasy team's entire season schedule.
    *   **Functionality**: Fetches schedule HTML, parses it using `parse_schedule_data`, extracts your team's name, and then presents a formatted view of past game results, the current week's matchup, and upcoming games using `display_schedule`.
*   **`league_matchups.py`**:
    *   **Purpose**: Provides a league-wide view of matchups and results.
    *   **Functionality**: Fetches league HTML, determines the current week, parses current and previous week matchups (`parse_current_week_matchups`), extracts team IDs (`extract_team_ids_from_matchups`), and then fetches detailed roster and owner information for each team (`fetch_team_roster`). Finally, it displays both previous week results and current week matchups with starting lineups and projected points using `display_week_matchups`.
*   **`nfl_common.py`**:
    *   **Purpose**: Contains reusable utility functions for web scraping and HTML parsing.
    *   **Key Functions**:
        *   `fetch_schedule_html()`: Handles HTTP requests with proper headers and cookie authentication.
        *   `extract_team_ids_from_matchups()`: Maps team names to their unique IDs.
        *   `parse_team_roster()`: Extracts player data (starters, bench, position, points) from a team's roster page.
        *   `extract_team_owner()`: Retrieves the owner's name for a given team.
        *   `fetch_team_roster()`: Combines roster and owner extraction for a team ID.
        *   `parse_current_week_matchups()`: Extracts matchup details (teams, scores, links) for a given week.
        *   `extract_team_name()`: Parses the team name from the page header.
*   **`pyproject.toml`**:
    *   **Purpose**: Defines project metadata and manages core dependencies.
    *   **Content**: Specifies the project name, version, Python requirement (`>=3.10`), and lists primary libraries: `requests`, `beautifulsoup4`, and `lxml`. This file is used by `uv` for dependency management.
*   **`resources/`**:
    *   **Purpose**: Contains sample HTML files (`schedule.html`, `team.html`) that can be used for local testing of parsing functions without making live HTTP requests.

## How to Run

### Dependencies

This project uses `uv` for efficient dependency management.

1.  **Install `uv` (if not already installed):**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Install project dependencies:**
    ```bash
    uv sync
    ```

Alternatively, you can manually install the required libraries using `pip`:
```bash
pip install requests beautifulsoup4 lxml
```

### Usage Commands

Ensure your configurations (cookies, league ID) are updated within the scripts as described in the "Configuration" section below.

1.  **Run My Team Schedule script:**
    ```bash
    uv run my_team_schedule.py
    ```

2.  **Run League Matchups script:**
    ```bash
    uv run league_matchups.py
    ```

## Configuration

Both scripts require specific configuration parameters to function correctly. These are hardcoded within the scripts and need to be updated directly in the respective `.py` files.

*   **Cookies**: Authentication is handled via session cookies. Update the `cookies` variable in both `league_matchups.py` and `my_team_schedule.py` with your current NFL.com Fantasy session cookies.
    *   _Location in files_: `cookies = ''` (around line 77 in `league_matchups.py`, line 69 in `my_team_schedule.py`)

*   **League ID**: The scripts are configured for a specific league ID (`12698811`). To use them with a different league, update the `url` (or `base_url`) variable in both `league_matchups.py` and `my_team_schedule.py`.
    *   _Location in files_: `url = "https://fantasy.nfl.com/league/12698811?scheduleType=team&standingsTab=schedule"` (around line 74 in `league_matchups.py`, line 66 in `my_team_schedule.py`)

## How to Test

The parsing logic, primarily housed in `nfl_common.py`, can be tested locally without making live network requests. You can:

1.  **Use local HTML files**: The `resources/` directory contains example `schedule.html` and `team.html` files.
2.  **Directly import and call functions**: Import the parsing functions (e.g., `parse_schedule_data`, `parse_current_week_matchups`, `parse_team_roster`) from `nfl_common.py` into a separate test script or an interactive Python session.
3.  **Pass local HTML content**: Load the content of the `resources/*.html` files into a string variable and pass this string to the parsing functions to verify their output.