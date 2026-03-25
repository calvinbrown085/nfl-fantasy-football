# Project Overview

This project provides two Python scripts for fetching and parsing NFL Fantasy Football league data directly from the NFL.com Fantasy website. It allows users to view their personal team's schedule and results, or get a comprehensive overview of all league matchups, including past results and current week starting lineups.

# Architecture

The system follows a client-side scraping architecture. Two primary scripts, `my_team_schedule.py` and `league_matchups.py`, act as entry points. Both scripts leverage `nfl_common.py`, a shared utility module, to handle the underlying web scraping logic.

1.  **HTML Fetching**: `nfl_common.py` uses the `requests` library to fetch HTML content from specified NFL.com Fantasy URLs, including cookie-based authentication.
2.  **HTML Parsing**: `nfl_common.py` then uses `BeautifulSoup4` (with `lxml` for performance) to parse the fetched HTML, extracting structured data such as team names, IDs, scores, player rosters, and owner names.
3.  **Data Processing & Display**: The main scripts (`my_team_schedule.py` and `league_matchups.py`) take the parsed data from `nfl_common.py` and apply specific logic to format and display it to the console, catering to their respective features (personal schedule vs. league-wide matchups).

This modular approach separates the concerns of web interaction and generic parsing from application-specific display logic.

# Key Files

*   `my_team_schedule.py`:
    *   **Purpose**: Focuses on a single fantasy team.
    *   **Functionality**: Fetches the specified team's full season schedule, displaying past game results, the current week's matchup, and upcoming games.
    *   **Key Functions**: `parse_schedule_data` (extracts individual team schedule from HTML), `display_schedule` (formats and prints the schedule).
*   `league_matchups.py`:
    *   **Purpose**: Provides a league-wide view of matchups.
    *   **Functionality**: Fetches and displays previous week's results and current week's matchups for all teams, including owner names, final scores (for past games), and detailed starting lineups with projected points for current week games.
    *   **Key Functions**: `get_current_week_number` (determines current week), `fetch_previous_week_matchups` (retrieves prior week's data), `display_week_matchups` (formats and prints league matchups with optional roster details).
*   `nfl_common.py`:
    *   **Purpose**: Contains common, reusable functions for web scraping NFL.com Fantasy.
    *   **Functionality**:
        *   `fetch_schedule_html`: Performs HTTP GET requests with user-agent and cookies.
        *   `extract_team_ids_from_matchups`: Maps team names to their numerical IDs from matchup data.
        *   `parse_team_roster`: Extracts player positions, names, IDs, and fantasy points for starters and bench from a team's roster page.
        *   `extract_team_owner`: Retrieves the owner's name from a team's page.
        *   `fetch_team_roster`: Combines fetching and parsing to get a team's full roster and owner.
        *   `parse_current_week_matchups`: Extracts matchup details (teams, scores, links) for a given week.
        *   `extract_team_name`: Retrieves the main team name from the HTML.
*   `pyproject.toml`: Defines project metadata and lists required Python dependencies (`requests`, `beautifulsoup4`, `lxml`). Used by `uv` for package management.
*   `resources/`: Contains local HTML files (`schedule.html`, `team.html`) which can be used for testing parsing logic without live network requests, aiding in development and debugging.

# How to Run

## Prerequisites

*   Python 3.10 or higher.
*   `uv` for dependency management (recommended).

## Installation

1.  **Install `uv` (if not already installed):**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  **Install project dependencies:**
    ```bash
    uv sync
    ```
    Alternatively, using pip:
    ```bash
    pip install requests beautifulsoup4 lxml
    ```

## Usage

### Personal Team Schedule (`my_team_schedule.py`)
Displays your team's season schedule with past results and upcoming games.
```bash
uv run my_team_schedule.py
```

### League-Wide Matchups (`league_matchups.py`)
Shows previous week results and current week matchups for all teams, including rosters and owner names.
```bash
uv run league_matchups.py
```

# Configuration

The scripts require direct modification for authentication and target league settings.

*   **Authentication Cookies**: Both `my_team_schedule.py` and `league_matchups.py` contain a `cookies` variable (an empty string by default). For the scripts to successfully fetch data from NFL.com, this variable must be updated with a valid session cookie from your NFL.com Fantasy account.
*   **League ID**: The `base_url` variable in both scripts currently points to league ID `12698811`. To use the scripts with a different league, modify the URL in `my_team_schedule.py` and `league_matchups.py` to replace `12698811` with your desired NFL Fantasy league ID.

# How to Test

The parsing functions within `nfl_common.py` (e.g., `parse_schedule_data`, `parse_team_roster`, `parse_current_week_matchups`) can be tested independently using the local HTML files located in the `resources/` directory. You can import these functions into a separate test script or a Python interactive session and pass the content of `schedule.html` or `team.html` to them to verify parsing logic without making live network requests.