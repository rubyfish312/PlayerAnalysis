# PlayerAnalysis
tools for analysis players' behavior


## Player_Performance:
- criterias to filt some dangerous bet

## bokeh_app
- data visualization

# SA Treeline Check
check the P&L in each SA treeline in 3 months
look for strange PT setting or changing on CA's PT

## check 3 months P&L in each SA treeline
- match_treeline.py
find 'snkhkd14' with strang P&L changing between CA & SA
->check 'snkhkd14' treeline

## check selected SA treeline
### number of players changing in 3 months
- sa_player_check.py
check number of players in each month
->'snkhkd14' Aug:164, Sep:172, Oct:143
### check players winloss / CA P&L / SA P&L in Aug & Sep
classify players by keep playing or not
check CA P&L / SA P&L strange changing
->SA's PT has advantage in Sep
