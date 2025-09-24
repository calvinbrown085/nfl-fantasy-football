#!/usr/bin/env python3
"""
My Team Schedule Parser

This script fetches and displays your individual team's schedule,
showing past results, current week, and upcoming games.
"""

import sys
from nfl_common import fetch_schedule_html, extract_team_name
from bs4 import BeautifulSoup
from typing import List, Dict

def parse_schedule_data(html_content: str) -> List[Dict[str, str]]:
    """
    Parse the HTML content to extract schedule information.
    
    Args:
        html_content: HTML content from the NFL Fantasy page
        
    Returns:
        List of dictionaries containing schedule data
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    schedule_data = []
    
    # Find the schedule table
    schedule_table = soup.find('table', class_='tableType-weeks')
    if not schedule_table:
        print("Could not find schedule table in HTML")
        return schedule_data
    
    # Find all schedule rows
    schedule_rows = schedule_table.find('tbody').find_all('tr', class_=lambda x: x and 'weeks-' in x)
    
    for row in schedule_rows:
        week_data = {}
        
        # Extract week number
        week_cell = row.find('td', class_='weekName')
        if week_cell:
            week_data['week'] = week_cell.get_text(strip=True)
        
        # Extract opponent information
        opponent_cell = row.find('td', class_='teamImageAndName')
        if opponent_cell:
            team_name_link = opponent_cell.find('a', class_='teamName')
            if team_name_link:
                week_data['opponent'] = team_name_link.get_text(strip=True)
                week_data['opponent_id'] = team_name_link.get('href', '').split('/')[-1] if team_name_link.get('href') else ''
            
            # Check if it's playoffs
            playoff_label = opponent_cell.find('span', class_='plabel')
            if playoff_label:
                week_data['opponent'] = playoff_label.get_text(strip=True)
        
        # Extract result/status information
        result_cell = row.find('td', class_='weekTeamMatchupResult')
        if result_cell:
            result_div = result_cell.find('div', class_='result')
            if result_div:
                # Check if it's a completed game with score
                team_totals = result_div.find_all('em', class_='teamTotal')
                if len(team_totals) == 2:
                    week_data['home_score'] = team_totals[0].get_text(strip=True)
                    week_data['away_score'] = team_totals[1].get_text(strip=True)
                    result_text = result_div.find('em', class_='resultText')
                    if result_text:
                        week_data['result'] = result_text.get_text(strip=True)
                else:
                    # Future game or view game center
                    link = result_div.find('a')
                    if link:
                        week_data['status'] = link.get_text(strip=True)
        
        # Check if this is the current/selected week
        if 'selected' in row.get('class', []):
            week_data['current_week'] = True
        
        schedule_data.append(week_data)
    
    return schedule_data

def display_schedule(schedule_data: List[Dict[str, str]], team_name: str = "Your Team") -> None:
    """
    Display the schedule in a formatted manner.
    
    Args:
        schedule_data: List of schedule dictionaries
        team_name: Name of the team (extracted from HTML if possible)
    """
    print(f"\n🏈 NFL Fantasy Schedule for {team_name}")
    print("=" * 60)
    
    current_week = None
    upcoming_games = []
    completed_games = []
    
    for game in schedule_data:
        if game.get('current_week'):
            current_week = game
        elif game.get('result'):
            completed_games.append(game)
        else:
            upcoming_games.append(game)
    
    # Show current week
    if current_week:
        print(f"\n📅 CURRENT WEEK {current_week.get('week', 'N/A')}")
        print("-" * 30)
        opponent = current_week.get('opponent', 'TBD')
        status = current_week.get('status', 'Pending')
        print(f"vs {opponent} - {status}")
    
    # Show upcoming games
    if upcoming_games:
        print(f"\n🔮 UPCOMING GAMES")
        print("-" * 30)
        for game in upcoming_games[:5]:  # Show next 5 games
            week = game.get('week', 'N/A')
            opponent = game.get('opponent', 'TBD')
            status = game.get('status', 'Scheduled')
            print(f"Week {week}: vs {opponent} - {status}")
    
    # Show recent completed games
    if completed_games:
        print(f"\n✅ RECENT RESULTS")
        print("-" * 30)
        for game in completed_games[-3:]:  # Show last 3 games
            week = game.get('week', 'N/A')
            opponent = game.get('opponent', 'N/A')
            result = game.get('result', 'N/A')
            home_score = game.get('home_score', '0')
            away_score = game.get('away_score', '0')
            print(f"Week {week}: vs {opponent} - {home_score}-{away_score} ({result})")

def main():
    """Main function to run the personal team schedule parser."""
    url = "https://fantasy.nfl.com/league/12698811?scheduleType=team&standingsTab=schedule"
    
    # Cookie string for authentication - update this with your actual cookies
    cookies = ''
    try:
        print("🔄 Fetching your team's schedule...")
        html_content = fetch_schedule_html(url, cookies)
        
        print("📊 Parsing schedule data...")
        schedule_data = parse_schedule_data(html_content)
        
        if not schedule_data:
            print("❌ No schedule data found. The page structure may have changed.")
            return
        
        # Extract team name
        team_name = extract_team_name(html_content)
        
        # Display the schedule
        display_schedule(schedule_data, team_name)
        
        print(f"\n📈 Total games found: {len(schedule_data)}")
        print("✅ Personal schedule parsing completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
