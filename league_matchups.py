#!/usr/bin/env python3
"""
League Matchups Parser

This script fetches and displays the current week's matchups for all teams
in the league, including owner names and starting lineups.
"""

import sys
from nfl_common import (
    fetch_schedule_html, extract_team_ids_from_matchups, 
    parse_current_week_matchups, fetch_team_roster, fetch_team_projections
)
import re
from typing import List, Dict

def get_current_week_number(html_content: str) -> int:
    """
    Extract the current week number from the HTML content.
    
    Args:
        html_content: HTML content from the NFL Fantasy page
        
    Returns:
        Current week number or 2 as default
    """
    # Look for the current week in the navigation
    match = re.search(r'<li class="wl wl-(\d+)[^"]*">Week (\d+)</li>', html_content)
    if match:
        return int(match.group(2))
    
    # Fallback: look in the scoreboard section
    match = re.search(r'week=(\d+)', html_content)
    if match:
        return int(match.group(1))
    
    return 2  # Default to week 2

def fetch_previous_week_matchups(base_url: str, current_week: int, cookies: str = "") -> List[Dict[str, str]]:
    """
    Fetch previous week's matchups and results.
    
    Args:
        base_url: Base URL for the league
        current_week: Current week number
        cookies: Cookie string for authentication
        
    Returns:
        List of previous week matchups with results
    """
    if current_week <= 1:
        return []
    
    prev_week = current_week - 1
    prev_week_url = f"{base_url}?scoreStripType=fantasy&week={prev_week}"
    
    try:
        prev_html = fetch_schedule_html(prev_week_url, cookies)
        return parse_current_week_matchups(prev_html)
    except Exception as e:
        print(f"Could not fetch previous week data: {e}")
        return []

def display_week_matchups(matchups: List[Dict[str, str]], week_label: str, team_rosters: Dict[str, Dict[str, any]] = None, show_rosters: bool = True) -> None:
    """
    Display week's matchups for all teams with optional roster information.
    
    Args:
        matchups: List of matchup dictionaries
        week_label: Label for the week (e.g., "CURRENT WEEK 2", "PREVIOUS WEEK 1")
        team_rosters: Optional dictionary mapping team names to roster and owner data
        show_rosters: Whether to show detailed roster information
    """
    if not matchups:
        print(f"❌ No {week_label.lower()} matchups found")
        return
    
    print(f"\n🏈 {week_label} LEAGUE MATCHUPS")
    print("=" * 90)
    
    for i, matchup in enumerate(matchups, 1):
        team1 = matchup.get('team1', 'Team 1')
        team2 = matchup.get('team2', 'Team 2')
        team1_score = matchup.get('team1_score', '0.00')
        team2_score = matchup.get('team2_score', '0.00')
        
        # Get owner names if available
        team1_display = team1
        team2_display = team2
        
        if team_rosters:
            team1_data = team_rosters.get(team1, {})
            team2_data = team_rosters.get(team2, {})
            
            team1_owner = team1_data.get('owner', '')
            team2_owner = team2_data.get('owner', '')
            
            if team1_owner:
                team1_display = f"{team1} ({team1_owner})"
            if team2_owner:
                team2_display = f"{team2} ({team2_owner})"
        
        # Determine if game is in progress or upcoming
        if team1_score == '0.00' and team2_score == '0.00':
            status = "📅 Upcoming"
        else:
            status = f"📊 {team1_score} - {team2_score}"
        
        # Compute projected totals if available
        proj_info = ""
        if team_rosters:
            def sum_proj(team_name: str) -> float:
                team_data = team_rosters.get(team_name, {})
                projections = team_data.get('projections', {})
                starters = projections.get('starters', []) if isinstance(projections, dict) else []
                total = 0.0
                for p in starters:
                    try:
                        total += float(p.get('projected_points', '0') or 0)
                    except ValueError:
                        pass
                return total
            t1p = sum_proj(team1)
            t2p = sum_proj(team2)
            if t1p > 0 or t2p > 0:
                proj_info = f" | Proj: {t1p:.2f} - {t2p:.2f}"

        print(f"\n{i:2}. {team1_display:<40} vs {team2_display:<40} {status}{proj_info}")
        
        # Display roster information if available and requested
        if show_rosters and team_rosters:
            team1_data = team_rosters.get(team1, {})
            team2_data = team_rosters.get(team2, {})
            
            team1_roster = team1_data.get('roster', {})
            team2_roster = team2_data.get('roster', {})
            
            if team1_roster and team2_roster:
                print("    " + "-" * 82)
                
                # Display starters for both teams side by side
                team1_starters = team1_roster.get('starters', [])
                team2_starters = team2_roster.get('starters', [])

                # Build projection maps keyed by player_id for easy lookup
                def build_proj_map(team_data: Dict[str, any]) -> Dict[str, str]:
                    proj_map: Dict[str, str] = {}
                    projections = team_data.get('projections', {}) if isinstance(team_data, dict) else {}
                    starters_proj = projections.get('starters', []) if isinstance(projections, dict) else []
                    for p in starters_proj:
                        pid = p.get('player_id')
                        if pid:
                            proj_map[pid] = p.get('projected_points', '')
                    return proj_map

                team1_proj_map = build_proj_map(team1_data)
                team2_proj_map = build_proj_map(team2_data)
                
                print(f"    {'STARTING LINEUP':<40} {'STARTING LINEUP':<40}")
                print(f"    {team1_display[:38]:<40} {team2_display[:38]:<40}")
                print(f"    {'-'*40} {'-'*40}")
                
                max_starters = max(len(team1_starters), len(team2_starters))
                for j in range(max_starters):
                    team1_player = ""
                    team2_player = ""
                    
                    if j < len(team1_starters):
                        p1 = team1_starters[j]
                        pos1 = p1.get('position', 'N/A')
                        name1 = p1.get('name', 'Unknown')[:18]
                        # Prefer projected points if available for this week
                        pid1 = p1.get('player_id')
                        proj1 = team1_proj_map.get(pid1) if pid1 else None
                        pts1 = proj1 if proj1 not in (None, '') else p1.get('fantasy_points', '0')
                        team1_player = f"{pos1:3} {name1:<18} ({pts1})"
                    
                    if j < len(team2_starters):
                        p2 = team2_starters[j]
                        pos2 = p2.get('position', 'N/A')
                        name2 = p2.get('name', 'Unknown')[:18]
                        pid2 = p2.get('player_id')
                        proj2 = team2_proj_map.get(pid2) if pid2 else None
                        pts2 = proj2 if proj2 not in (None, '') else p2.get('fantasy_points', '0')
                        team2_player = f"{pos2:3} {name2:<18} ({pts2})"
                    
                    print(f"    {team1_player:<40} {team2_player:<40}")
            elif team1_roster or team2_roster:
                # Show available roster info if only one team's data is available
                if team1_roster:
                    starters = team1_roster.get('starters', [])
                    if starters:
                        starter_list = ', '.join([f"{p.get('position', 'N/A')} {p.get('name', 'Unknown')[:15]}" for p in starters[:5]])
                        print(f"    {team1_display} starters: {starter_list}")
                
                if team2_roster:
                    starters = team2_roster.get('starters', [])
                    if starters:
                        starter_list = ', '.join([f"{p.get('position', 'N/A')} {p.get('name', 'Unknown')[:15]}" for p in starters[:5]])
                        print(f"    {team2_display} starters: {starter_list}")
    
    print(f"\n📈 Total matchups: {len(matchups)}")

def main():
    """Main function to run the league matchups parser."""
    base_url = "https://fantasy.nfl.com/league/12698811"
    url = f"{base_url}?scheduleType=team&standingsTab=schedule"
    
    # Cookie string for authentication - update this with your actual cookies
    cookies = ''
    try:
        print("🔄 Fetching NFL Fantasy league data...")
        html_content = fetch_schedule_html(url, cookies)
        
        # Get current week number
        current_week_num = get_current_week_number(html_content)
        print(f"📅 Detected current week: {current_week_num}")
        
        print("📊 Parsing current week matchups...")
        current_week_matchups = parse_current_week_matchups(html_content)
        
        print("📊 Extracting team IDs...")
        team_mapping = extract_team_ids_from_matchups(html_content)
        
        # Fetch previous week matchups
        print("📊 Fetching previous week matchups...")
        previous_week_matchups = fetch_previous_week_matchups(base_url, current_week_num, cookies)
        
        # Fetch roster data for teams in current week matchups
        team_rosters = {}
        if team_mapping and current_week_matchups:
            print("📊 Fetching team rosters and owners...")
            for matchup in current_week_matchups:
                team1 = matchup.get('team1')
                team2 = matchup.get('team2')
                
                if team1 and team1 in team_mapping and team1 not in team_rosters:
                    team_id = team_mapping[team1]
                    print(f"  Fetching data for {team1} (ID: {team_id})...")
                    team_data = fetch_team_roster(team_id, cookies)
                    # Fetch projections for starters/bench from Game Center
                    try:
                        projections = fetch_team_projections(team_id, current_week_num, cookies)
                        team_data['projections'] = projections
                    except Exception as e:
                        print(f"    Warning: could not fetch projections for {team1}: {e}")
                        team_data['projections'] = {'starters': [], 'bench': []}
                    team_rosters[team1] = team_data
                
                if team2 and team2 in team_mapping and team2 not in team_rosters:
                    team_id = team_mapping[team2]
                    print(f"  Fetching data for {team2} (ID: {team_id})...")
                    team_data = fetch_team_roster(team_id, cookies)
                    try:
                        projections = fetch_team_projections(team_id, current_week_num, cookies)
                        team_data['projections'] = projections
                    except Exception as e:
                        print(f"    Warning: could not fetch projections for {team2}: {e}")
                        team_data['projections'] = {'starters': [], 'bench': []}
                    team_rosters[team2] = team_data
        
        # Display previous week results (without rosters for cleaner display)
        if previous_week_matchups:
            display_week_matchups(
                previous_week_matchups, 
                f"PREVIOUS WEEK {current_week_num - 1} RESULTS", 
                team_rosters, 
                show_rosters=False
            )
        
        # Display current week matchups with full roster info
        if current_week_matchups:
            display_week_matchups(
                current_week_matchups, 
                f"CURRENT WEEK {current_week_num}", 
                team_rosters, 
                show_rosters=True
            )
        else:
            print("❌ No current week matchups found")
        
        print("✅ League matchups parsing completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
