#!/usr/bin/env python3
"""
Common functions shared between NFL Fantasy schedule parsers.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

def fetch_schedule_html(url: str, cookies: str = "") -> str:
    """
    Fetch the HTML content from the NFL Fantasy schedule URL.
    
    Args:
        url: The NFL Fantasy schedule URL
        cookies: Cookie string for authentication
        
    Returns:
        HTML content as string
        
    Raises:
        requests.RequestException: If the request fails
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    if cookies:
        headers['cookie'] = cookies
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching schedule: {e}")
        raise

def extract_team_ids_from_matchups(html_content: str) -> Dict[str, str]:
    """
    Extract team IDs and names from the current week matchups.
    
    Args:
        html_content: HTML content from the NFL Fantasy page
        
    Returns:
        Dictionary mapping team names to team IDs
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    team_mapping = {}
    
    # Find the scoreboard section with current week matchups
    scoreboard = soup.find('ul', class_='ss ss-7')
    if not scoreboard:
        return team_mapping
    
    # Find all matchup items
    matchup_items = scoreboard.find_all('li')
    
    for item in matchup_items:
        # Extract team names and IDs from the spans
        team_spans = item.find_all('span', class_=lambda x: x and 'teamTotal teamId-' in str(x))
        team_ems = item.find_all('em')
        
        if len(team_spans) == 2 and len(team_ems) >= 2:
            # First team
            team1_span = team_spans[0]
            team1_em = team_ems[0] if len(team_ems) > 0 else None
            if team1_span and team1_em:
                team1_classes = team1_span.get('class', [])
                for cls in team1_classes:
                    if 'teamId-' in str(cls):
                        team1_id = str(cls).split('teamId-')[1]
                        team1_name = team1_em.get_text(strip=True)
                        team_mapping[team1_name] = team1_id
                        break
            
            # Second team
            team2_span = team_spans[1]
            team2_em = team_ems[1] if len(team_ems) > 1 else None
            if team2_span and team2_em:
                team2_classes = team2_span.get('class', [])
                for cls in team2_classes:
                    if 'teamId-' in str(cls):
                        team2_id = str(cls).split('teamId-')[1]
                        team2_name = team2_em.get_text(strip=True)
                        team_mapping[team2_name] = team2_id
                        break
    
    return team_mapping

def parse_team_roster(html_content: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Parse team roster from team HTML page.
    
    Args:
        html_content: HTML content from the NFL Fantasy team page
        
    Returns:
        Dictionary with 'starters' and 'bench' lists containing player data
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    roster = {'starters': [], 'bench': []}
    
    # Find all player rows
    player_rows = soup.find_all('tr', class_=lambda x: x and ('player-' in str(x) and 'benchLabel' not in str(x)))
    
    is_bench = False
    
    for row in player_rows:
        # Check if we've hit the bench section
        if row.find_previous_sibling('tr', class_='benchLabel'):
            is_bench = True
        
        player_data = {}
        
        # Extract position
        pos_cell = row.find('td', class_='teamPosition')
        if pos_cell:
            pos_span = pos_cell.find('span', class_='pre')
            if pos_span:
                player_data['position'] = pos_span.get_text(strip=True)
        
        # Extract player name and info
        name_cell = row.find('td', class_='playerNameAndInfo')
        if name_cell:
            player_link = name_cell.find('a', class_='playerCard')
            if player_link:
                player_data['name'] = player_link.get_text(strip=True)
                
                # Extract player ID from the link
                href = player_link.get('href', '')
                if 'playerId=' in href:
                    player_id = href.split('playerId=')[1].split('&')[0]
                    player_data['player_id'] = player_id
            
            # Extract team and position info
            em_tag = name_cell.find('em')
            if em_tag:
                team_pos_info = em_tag.get_text(strip=True)
                player_data['team_position'] = team_pos_info
        
        # Extract fantasy points
        points_cell = row.find('td', class_='statTotal')
        if points_cell:
            points_span = points_cell.find('span', class_='playerSeasonTotal')
            if points_span:
                player_data['fantasy_points'] = points_span.get_text(strip=True)
        
        # Only add if we have essential data
        if player_data.get('name') and player_data.get('position'):
            if is_bench:
                roster['bench'].append(player_data)
            else:
                roster['starters'].append(player_data)
    
    return roster

def extract_team_owner(html_content: str) -> str:
    """
    Extract team owner name from team HTML page.
    
    Args:
        html_content: HTML content from the NFL Fantasy team page
        
    Returns:
        Owner name or empty string if not found
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Look for owner information
    owner_span = soup.find('span', class_='userName')
    if owner_span:
        return owner_span.get_text(strip=True)
    
    return ""

def fetch_team_roster(team_id: str, cookies: str = "") -> Dict[str, any]:
    """
    Fetch team roster and owner info from NFL Fantasy API.
    
    Args:
        team_id: The team ID to fetch roster for
        cookies: Cookie string for authentication
        
    Returns:
        Dictionary with roster data and owner info
    """
    url = f"https://fantasy.nfl.com/league/12698811/team/{team_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    if cookies:
        headers['cookie'] = cookies
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        roster_data = parse_team_roster(response.text)
        owner_name = extract_team_owner(response.text)
        
        return {
            'roster': roster_data,
            'owner': owner_name
        }
    except requests.RequestException as e:
        print(f"Error fetching team {team_id} roster: {e}")
        return {'roster': {'starters': [], 'bench': []}, 'owner': ''}

def parse_current_week_matchups(html_content: str) -> List[Dict[str, str]]:
    """
    Parse the HTML content to extract current week's matchups for all teams.
    
    Args:
        html_content: HTML content from the NFL Fantasy page
        
    Returns:
        List of dictionaries containing matchup data for all teams
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    matchups = []
    
    # Find the scoreboard section with current week matchups
    scoreboard = soup.find('ul', class_='ss ss-7')
    if not scoreboard:
        print("Could not find scoreboard section in HTML")
        return matchups
    
    # Find all matchup items
    matchup_items = scoreboard.find_all('li')
    
    for item in matchup_items:
        matchup = {}
        
        # Get the title attribute which contains the full matchup info
        link = item.find('a')
        if link:
            title = link.get('title', '')
            if ' vs. ' in title:
                teams = title.split(' vs. ')
                matchup['team1'] = teams[0].strip()
                matchup['team2'] = teams[1].strip()
        
        # Extract team names and scores from the divs
        team_divs = item.find_all('div', class_=['first', 'last'])
        if len(team_divs) == 2:
            # First team
            team1_em = team_divs[0].find('em')
            team1_score = team_divs[0].find('span', class_='teamTotal')
            if team1_em:
                matchup['team1'] = team1_em.get_text(strip=True)
            if team1_score:
                matchup['team1_score'] = team1_score.get_text(strip=True)
            
            # Second team  
            team2_em = team_divs[1].find('em')
            team2_score = team_divs[1].find('span', class_='teamTotal')
            if team2_em:
                matchup['team2'] = team2_em.get_text(strip=True)
            if team2_score:
                matchup['team2_score'] = team2_score.get_text(strip=True)
        
        # Extract game center link for week info
        if link:
            href = link.get('href', '')
            if 'week=' in href:
                week_param = href.split('week=')[-1]
                matchup['week'] = week_param.split('&')[0] if '&' in week_param else week_param
        
        # Only add if we have both teams
        if matchup.get('team1') and matchup.get('team2'):
            matchups.append(matchup)
    
    return matchups

def extract_team_name(html_content: str) -> str:
    """
    Extract the team name from the HTML content.
    
    Args:
        html_content: HTML content from the NFL Fantasy page
        
    Returns:
        Team name or default string
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Try to find team name from the selected option
    selected_option = soup.find('option', selected=True)
    if selected_option:
        return selected_option.get_text(strip=True)
    
    # Fallback: try to find from page title or other elements
    title = soup.find('title')
    if title and 'Fantasy' in title.get_text():
        return "Your Team"
    
    return "Unknown Team"
