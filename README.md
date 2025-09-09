# NFL Fantasy Schedule Parsers

Two separate Python scripts to fetch and parse NFL Fantasy league data from NFL.com Fantasy website.

## 📁 **Scripts Overview**

### 🏈 **1. My Team Schedule** (`my_team_schedule.py`)
- Shows **your personal team's full season schedule**
- Displays past results, current week, and upcoming games
- Focuses on your individual team's performance

### 👥 **2. League Matchups** (`league_matchups.py`)
- Shows **current week matchups for ALL teams** in the league
- Includes owner names for each team
- Displays starting lineups side-by-side for each matchup
- Perfect for seeing who everyone is playing this week

### 🔧 **3. Common Functions** (`nfl_common.py`)
- Shared utility functions used by both scripts
- Handles HTML fetching, parsing, and data extraction

## 📦 **Installation**

1. Install the required dependencies:
```bash
pip install -r requirements_parser.txt
```

## 🚀 **Usage**

### Personal Team Schedule
```bash
python my_team_schedule.py
```

**Example Output:**
```
🔄 Fetching your team's schedule...
📊 Parsing schedule data...

🏈 NFL Fantasy Schedule for A Five Star Team
============================================================

📅 CURRENT WEEK 2
------------------------------
vs DangerousNightsCrew - View Game Center

🔮 UPCOMING GAMES
------------------------------
Week 3: vs Game of Throws - View Game Center
Week 4: vs Snacks and sacks - View Game Center
Week 5: vs Cache Me Outside - View Game Center

✅ RECENT RESULTS
------------------------------
Week 1: vs FlyWithTheEagles - 118.16-111.10 (Win)

📈 Total games found: 18
✅ Personal schedule parsing completed!
```

### League-Wide Matchups
```bash
python league_matchups.py
```

**Example Output:**
```
🔄 Fetching NFL Fantasy league data...
📊 Parsing current week matchups...
📊 Extracting team IDs...
📊 Fetching team rosters and owners...
  Fetching data for A Five Star Team (ID: 10)...
  Fetching data for DangerousNightsCrew (ID: 13)...
  ...

🏈 WEEK 2 LEAGUE MATCHUPS
==========================================================================================

 1. A Five Star Team (Calvin)             vs DangerousNightsCrew (JJ)             📅 Upcoming
    ----------------------------------------------------------------------------------
    STARTING LINEUP                          STARTING LINEUP                        
    A Five Star Team (Calvin)                DangerousNightsCrew (JJ)              
    ---------------------------------------- ----------------------------------------
    QB  Josh Allen         (24.5)           QB  Kyler Murray       (18.3)          
    RB  Saquon Barkley     (18.2)           RB  Javonte Williams   (20.4)          
    RB  James Cook         (15.8)           RB  Kyren Williams     (13.9)          
    WR  Ja'Marr Chase      (22.1)           WR  Tee Higgins        (6.3)           
    WR  Khalil Shakir      (12.4)           WR  Justin Jefferson   (14.8)          
    TE  Dalton Kincaid     (8.9)            TE  Sam LaPorta        (13.9)          
    W/R Xavier Worthy      (11.2)           W/R D'Andre Swift      (9.5)           
    K   Chase McLaughlin   (5.0)            K   Chase McLaughlin   (5.0)           
    DEF Chicago Bears      (11.0)           DEF Chicago Bears      (11.0)          

 2. Run CMC (Owner3)                       vs Purple Reign (Owner4)               📅 Upcoming
    ...

📈 Total matchups: 7
✅ League matchups parsing completed!
```

## ⚙️ **Configuration**

### Cookies
Both scripts include cookie strings for authentication. Update the `cookies` variable in each script with your current session cookies if needed.

### League ID
Both scripts are configured for league ID `12698811`. To use with a different league, update the URLs in both scripts:
```python
url = "https://fantasy.nfl.com/league/YOUR_LEAGUE_ID?scheduleType=team&standingsTab=schedule"
```

## 📊 **Features Comparison**

| Feature | My Team Schedule | League Matchups |
|---------|------------------|-----------------|
| Personal schedule | ✅ | ❌ |
| Past results | ✅ | ❌ |
| Upcoming games | ✅ | ❌ |
| Current week all teams | ❌ | ✅ |
| Owner names | ❌ | ✅ |
| Starting lineups | ❌ | ✅ |
| Fantasy points | ❌ | ✅ |

## 🔧 **Script Structure**

### `nfl_common.py`
- `fetch_schedule_html()`: Downloads HTML content with authentication
- `extract_team_ids_from_matchups()`: Maps team names to IDs
- `parse_current_week_matchups()`: Extracts current week matchups
- `parse_team_roster()`: Parses player data from team pages
- `extract_team_owner()`: Gets owner names from team pages
- `fetch_team_roster()`: Fetches live roster and owner data
- `extract_team_name()`: Gets team name from HTML

### `my_team_schedule.py`
- `parse_schedule_data()`: Extracts individual team schedule
- `display_schedule()`: Shows personal schedule with past/future games

### `league_matchups.py`
- `display_current_week_matchups()`: Shows all matchups with rosters

## 🛠️ **Error Handling**

Both scripts include error handling for:
- Network connectivity issues
- HTML parsing errors
- Missing or changed HTML structure
- Invalid responses from the server
- Authentication failures

## 📋 **Dependencies**

- `requests`: For HTTP requests to fetch HTML
- `beautifulsoup4`: For HTML parsing
- `lxml`: For faster HTML parsing (optional but recommended)

## 🧪 **Testing**

You can test the parsing functions with local HTML files using:
```bash
python test_parser.py
```

This will demonstrate both functionalities using your existing HTML files.
