import csv

my_list = [{'players.vis_name': 'Khazri', 'players.role': 'Midfielder', 'players.country': 'Tunisia',
            'players.last_name': 'Khazri', 'players.player_id': '989', 'players.first_name': 'Wahbi',
            'players.date_of_birth': '08/02/1991', 'players.team': 'Bordeaux'},
           {'players.vis_name': 'Khazri', 'players.role': 'Midfielder', 'players.country': 'Tunisia',
            'players.last_name': 'Khazri', 'players.player_id': '989', 'players.first_name': 'Wahbi',
            'players.date_of_birth': '08/02/1991', 'players.team': 'Sunderland'},
           {'players.vis_name': 'Lewis Baker', 'players.role': 'Midfielder', 'players.country': 'England',
            'players.last_name': 'Baker', 'players.player_id': '9574', 'players.first_name': 'Lewis',
            'players.date_of_birth': '25/04/1995', 'players.team': 'Vitesse'}
           ]

# write nested list of dict to csv
def nestedlist2csv(list, out_file):
    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        fieldnames=list[0].keys()  # solve the problem to automatically write the header
        w.writerow(fieldnames)
        for row in list:
            w.writerow(row.values())

nestedlist2csv(my_list, './02.csv')