## Baseball:
1. Make so that if a game has not started or is over Ball, Strike, Error and Bases don't show
2. If a game is complete have the final score of the winner be black on white
3. Make it more of a cli with optional things
  1. turn off team colors
  2. filter by team name (Abbreviation, team, city)
  3. filter by league
  4. filter by division
  5. filter by combo of above
    

This is from mlb.com what a weird url
https://statsapi.mlb.com/api/v1/schedule?language=en&sportId=1&date=05/10/2019&sortBy=gameDate&hydrate=game(content(summary,media(epg))),linescore(runners),flags,team,review

This is also something that is worth digging into it is neet the string after game is a game id of which you can get from the above url payload
https://statsapi.mlb.com/api/v1.1/game/565143/feed/live/diffPatch?language=en&startTimecode=20190510_202935
