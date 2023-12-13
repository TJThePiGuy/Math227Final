from pybaseball import batting_stats, cache, playerid_reverse_lookup

fields = ['IDfg','Season','Name','PA','OBP','O-Swing%','Z-Swing%','Swing%','Zone%']

for i in range(2002, 2024):
    fangraphsData = batting_stats(i,ind=1)


    trimData = fangraphsData[fields]

    IDrs = playerid_reverse_lookup([row['IDfg'] for idx,row in trimData.iterrows()],key_type='fangraphs')
    trimData['IDrs'] = trimData['IDfg'].map(IDrs.set_index('key_fangraphs')['key_retro'])

    with open(f'playerData\{i}.csv', 'w') as f:
        trimData.to_csv(f,lineterminator='\n')