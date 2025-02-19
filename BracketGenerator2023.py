import pandas as pd

def load_and_clean_espn_data(file_path):
    df = pd.read_csv(file_path)
    rounds = ['R2', 'R3', 'R4', 'R5', 'R6', 'R7']
    cleaned_data = []

    for round_name in rounds:
        for entry in df[round_name][1:]:
            if pd.notna(entry) and '-' in entry and '/' not in entry:
                try:
                    team, percent = entry.rsplit('-', 1)
                    percent = float(percent.replace('%', ''))
                    cleaned_data.append({'Team': team.strip(), 'Round': round_name, 'ESPN_Percentage': percent})
                except ValueError:
                    continue

    espn_df = pd.DataFrame(cleaned_data)
    espn_df['Team'] = espn_df['Team'].str.replace(r'^[0-9]+', '', regex=True).str.strip()
    espn_table = espn_df.pivot(index='Team', columns='Round', values='ESPN_Percentage').fillna(0).reset_index()
    return espn_table


def load_and_clean_fte_data(file_path):
    fte_table = pd.read_csv(file_path)
    probability_columns = ["team_name", "team_seed", "team_region", "rd2_win", "rd3_win", "rd4_win", "rd5_win", "rd6_win", "rd7_win"]
    fte_table = fte_table[probability_columns].copy()

    fte_table.rename(columns={
        'rd2_win': 'R2', 'rd3_win': 'R3', 'rd4_win': 'R4',
        'rd5_win': 'R5', 'rd6_win': 'R6', 'rd7_win': 'R7',
        'team_name': 'Team', 'team_seed': 'Seed', 'team_region': 'Region'
    }, inplace=True)

    fte_table[['R2', 'R3', 'R4', 'R5', 'R6', 'R7']] = fte_table[['R2', 'R3', 'R4', 'R5', 'R6', 'R7']].replace('%', '', regex=True)
    fte_table[['R2', 'R3', 'R4', 'R5', 'R6', 'R7']] = fte_table[['R2', 'R3', 'R4', 'R5', 'R6', 'R7']].apply(pd.to_numeric)
    return fte_table


def merge_tables(espn_table, fte_table, rounds):
    team_name_mapping = {
        "College of Charleston": "Charleston",
        "Miami (FL)": "Miami",
        "Michigan State": "Michigan St",
        "Kansas State": "Kansas St",
        "Boise State": "Boise St",
        "Kennesaw State": "Kennesaw St",
        "Louisiana-Lafayette": "Louisiana",
        "North Carolina State": "NC State",
        "North Carolina-Asheville": "UNC Asheville",
        "Northern Kentucky": "N Kentucky",
        "Saint Mary's (CA)": "Saint Mary's",
        "San Diego State": "San Diego St",
        "Southern California": "USC",
        "Texas Christian": "TCU",
        "UC-Santa Barbara": "UCSB",
        "Virginia Commonwealth": "VCU",
        "Connecticut": "UConn",
        "Florida Atlantic": "FAU",
        "Montana State": "Montana St",
    }

    espn_table["Team"] = espn_table["Team"].replace(team_name_mapping)
    fte_table["Team"] = fte_table["Team"].replace(team_name_mapping)

    fte_table = fte_table.rename(columns={'Seed': 'Seed_538', 'Region': 'Region_538'})
    merged_table = pd.merge(espn_table, fte_table, on='Team', how='outer', suffixes=("_ESPN", "_538"))

    if 'Region_538' in merged_table.columns:
        merged_table['Region'] = merged_table['Region_538'].fillna("Unknown").astype(str)
    else:
        print("Warning: Region_538 column not found in merged_table")

    merged_table['Seed'] = merged_table['Seed_538'].fillna(0).astype(str)
    merged_table['Region'] = merged_table['Region_538'].fillna(0).astype(str)

    merged_table = merged_table[['Team', 'Seed', 'Region'] + [f'{r}_ESPN' for r in rounds] + [f'{r}_538' for r in rounds]]
    merged_table.fillna(0, inplace=True)
    
    return merged_table

def calculate_leverage(merged_table):
    leverage = pd.DataFrame()
    leverage['Team'] = merged_table['Team']
    leverage['Seed'] = merged_table['Seed']
    leverage['Region'] = merged_table['Region']
    leverage['R64_Lev'] = (merged_table['R2_538'] - merged_table['R2_ESPN']) * merged_table['R2_538']
    leverage['R32_Lev'] = (merged_table['R3_538'] - merged_table['R3_ESPN']) * merged_table['R3_538']
    leverage['S16_Lev'] = (merged_table['R4_538'] - merged_table['R4_ESPN']) * merged_table['R4_538']
    leverage['E8_Lev'] = (merged_table['R5_538'] - merged_table['R5_ESPN']) * merged_table['R5_538']
    leverage['F4_Lev'] = (merged_table['R6_538'] - merged_table['R6_ESPN']) * merged_table['R6_538']
    leverage['NCG_Lev'] = (merged_table['R7_538'] - merged_table['R7_ESPN']) * merged_table['R7_538']
    return leverage


def print_bracket(champion, finals, final_four, elite_eight, sweet_sixteen, round_of_32):
    print("\n=== March Madness Bracket ===")
    print("\n Champion:")
    print(champion)
    print("\n Finals:")
    print(", ".join(sorted(finals)))
    print("\n Final Four:")
    print(", ".join(sorted(final_four)))
    print("\n Elite Eight:")
    print(", ".join(sorted(elite_eight)))
    print("\n Sweet Sixteen:")
    print(", ".join(sorted(sweet_sixteen)))
    print("\n Round of 32:")
    print(", ".join(sorted(round_of_32)))

def main():
    rounds = ['R2', 'R3', 'R4', 'R5', 'R6', 'R7']  # Define rounds here
    espn_table = load_and_clean_espn_data("Copy of 2023 March Madness Optimal Bracket - ESPN.csv")
    fte_table = load_and_clean_fte_data("FiveThirtyEight Data - 538.csv")
    merged_table = merge_tables(espn_table, fte_table, rounds)  # Pass rounds as an argument
    leverage = calculate_leverage(merged_table)

    #Pick Champion
    # Sort by NCG_Lev from greatest to least
    leverage = leverage.sort_values(by='NCG_Lev', ascending=False)

    # Clean 'Seed' column by removing non-numeric characters
    leverage['Seed'] = leverage['Seed'].str.extract('(\d+)').astype(int)

    original_leverage = leverage.copy()

    champion = leverage.loc[leverage['NCG_Lev'].idxmax(), 'Team']
    leverage = leverage[leverage['Team'] != champion]

    #Pick Finalist
    leverage = leverage.sort_values(by='F4_Lev', ascending=False)

    champion_region = original_leverage.loc[original_leverage['Team'] == champion, 'Region'].values[0]  # Get region directly
    opposite_regions = {'South', 'East'} if champion_region in {'Midwest', 'West'} else {'Midwest', 'West'}
    finalist_candidates = leverage[leverage['Region'].isin(opposite_regions)]

    if not finalist_candidates.empty:
        finalist = finalist_candidates.loc[finalist_candidates['F4_Lev'].idxmax(), 'Team']
        leverage = leverage[leverage['Team'] != finalist]
    else:
        finalist = None  # Edge case if no valid finalist exists

    finals = set()
    finals.add(champion)
    finals.add(finalist)

    #Pick Final Four
    final_four = finals.copy()

    leverage = leverage.sort_values(by='E8_Lev', ascending=False)
    while len(final_four) < 4:
        for _, row in leverage.iterrows():
            # Get the seeds of all eliminated teams from the original data
            eliminated_reg = set(original_leverage.loc[original_leverage['Team'].isin(list(final_four)), 'Region'])
            
            # Only add the candidate if its seed is not already in the eliminated set
            if row['Region'] not in eliminated_reg:
                final_four.add(row['Team'])
                leverage = leverage[leverage['Team'] != row['Team']]
                break

    #Pick Elite Eight   
    elite_eight = final_four.copy()
    region_counts = {region: 0 for region in leverage['Region'].unique()}  # Track teams per region in Elite Eight

    # Pick remaining Elite Eight teams
    leverage = leverage.sort_values(by='S16_Lev', ascending=False)
    while len(elite_eight) < 8:
        for _, row in leverage.iterrows():
            team_region = row['Region']
            region_teams = [
                team for team in elite_eight 
                if (not original_leverage[original_leverage['Team'] == team].empty and 
                    original_leverage[original_leverage['Team'] == team]['Region'].values[0] == team_region)
            ]
            if len(region_teams) < 2:
                #Checks for conflicting seeds
                region_seeds = [
                    original_leverage[original_leverage['Team'] == team]['Seed'].values[0]
                    for team in region_teams
                    if not original_leverage[original_leverage['Team'] == team].empty
                ]
                group1 = {1, 16, 8, 9, 5, 12, 4, 13}
                group2 = {2, 15, 7, 10, 3, 14, 6, 11}
                conflicting_seeds = group1 if row['Seed'] in group1 else group2
                if not any(seed in conflicting_seeds for seed in region_seeds):
                    elite_eight.add(row['Team'])
                    region_counts[team_region] += 1
                    leverage = leverage[leverage['Team'] != row['Team']]
                    break


    #Pick Sweet Sixteen
    leverage = leverage.sort_values(by='R32_Lev', ascending=False)

    sweet_sixteen = elite_eight.copy()

    region_seed_groups = {}  # Maps each region to the seed groups already selected in Elite Eight

    for team in elite_eight:
        team_region = original_leverage.loc[original_leverage['Team'] == team, 'Region'].values[0]
        team_seed = original_leverage.loc[original_leverage['Team'] == team, 'Seed'].values[0]
        # Determine seed group
        if team_seed in {1, 16, 8, 9}:
            seed_group = 1
        elif team_seed in {5, 12, 4, 13}:
            seed_group = 2
        elif team_seed in {6, 11, 3, 14}:
            seed_group = 3
        elif team_seed in {7, 10, 2, 15}:
            seed_group = 4
        else:
            print(f"Unexpected seed: {team_seed} for team {row['Team']}")  # Debugging statement
            continue  

        if team_region not in region_seed_groups:
            region_seed_groups[team_region] = set()
        region_seed_groups[team_region].add(seed_group)
        

    while len(sweet_sixteen) < 16:
        candidate_found = False
        for _, row in leverage.iterrows():
            team_region = row['Region']
            team_seed = int(row['Seed'])
            region_teams = [
                team for team in sweet_sixteen
                if original_leverage.loc[original_leverage['Team'] == team, 'Region'].values[0] == team_region
            ]
            
            # Ensure no more than 4 teams per region
            if len(region_teams) < 4:
                # Determine seed group
                if team_seed in {1, 16, 8, 9}:
                    candidate_group = 1
                elif team_seed in {5, 12, 4, 13}:
                    candidate_group = 2
                elif team_seed in {6, 11, 3, 14}:
                    candidate_group = 3
                elif team_seed in {7, 10, 2, 15}:
                    candidate_group = 4
                else:
                    continue  # Ignore unexpected seeds

                # Check if candidate's seed group is already filled in this region
                if team_region in region_seed_groups and candidate_group in region_seed_groups[team_region]:
                    continue  # Skip candidate if seed group is full
                
                # Add the candidate to Sweet Sixteen
                sweet_sixteen.add(row['Team'])
                leverage = leverage[leverage['Team'] != row['Team']]
                
                # Update region seed group tracking
                if team_region not in region_seed_groups:
                    region_seed_groups[team_region] = set()
                region_seed_groups[team_region].add(candidate_group)

                candidate_found = True
                break

    #Pick Round of 32
    round_of_32 = sweet_sixteen.copy() # The teams moving into the Round of 32

    leverage = leverage.sort_values(by='R64_Lev', ascending=False)

    region_seed_groups = {}  # Tracks selected seed groups per region

    for team in sweet_sixteen:
        team_region = original_leverage.loc[original_leverage['Team'] == team, 'Region'].values[0]
        team_seed = original_leverage.loc[original_leverage['Team'] == team, 'Seed'].values[0]
        
        # Assign seed groups based on updated pairs
        if team_seed in {1, 16}:
            seed_group = 1
        elif team_seed in {8, 9}:
            seed_group = 2
        elif team_seed in {2, 15}:
            seed_group = 3
        elif team_seed in {3, 14}:
            seed_group = 4
        elif team_seed in {4, 13}:
            seed_group = 5
        elif team_seed in {5, 12}:
            seed_group = 6
        elif team_seed in {6, 11}:
            seed_group = 7
        elif team_seed in {7, 10}:
            seed_group = 8
        else:
            print(f"Unexpected seed: {team_seed} for team {team}")
            continue  
        
        if team_region not in region_seed_groups:
            region_seed_groups[team_region] = set()
        region_seed_groups[team_region].add(seed_group)
        
    while len(round_of_32) < 32:
        candidate_found = False
        for _, row in leverage.iterrows():
            team_region = row['Region']
            team_seed = int(row['Seed'])
            region_teams = [
                team for team in round_of_32
                if original_leverage.loc[original_leverage['Team'] == team, 'Region'].values[0] == team_region
            ]
            
            # Ensure no more than 8 teams per region
            if len(region_teams) < 8:
                # Determine seed group
                if team_seed in {1, 16}:
                    candidate_group = 1
                elif team_seed in {8, 9}:
                    candidate_group = 2
                elif team_seed in {2, 15}:
                    candidate_group = 3
                elif team_seed in {3, 14}:
                    candidate_group = 4
                elif team_seed in {4, 13}:
                    candidate_group = 5
                elif team_seed in {5, 12}:
                    candidate_group = 6
                elif team_seed in {6, 11}:
                    candidate_group = 7
                elif team_seed in {7, 10}:
                    candidate_group = 8
                else:
                    continue  # Ignore unexpected seeds
                
                # Check if seed group is already filled in this region
                if team_region in region_seed_groups and candidate_group in region_seed_groups[team_region]:
                    continue  # Skip candidate if seed group is full
                
                # Add candidate to Round of 32
                round_of_32.add(row['Team'])
                leverage = leverage[leverage['Team'] != row['Team']]
                
                # Update region seed group tracking
                if team_region not in region_seed_groups:
                    region_seed_groups[team_region] = set()
                region_seed_groups[team_region].add(candidate_group)
                
                candidate_found = True
                break

    print_bracket(champion, finals, final_four, elite_eight, sweet_sixteen, round_of_32)  



    
if __name__ == "__main__":
    main()