# pygmalion

A proof-of-concept game+engine built on pygame.

##### TODO:
 - isolate particular test game from general mechanics
   - `pygmalion.py` for engine and `game.py` for game
 - rework camera ontology
   - either bound to movable or stationary
   - enable dynamic switching between the modes
 - break apart main loop
   - pass `interval` to `on_tick`
   - bind inputs to callbacks
     - _nice to have: `diradd`/`dirsub` controls model_
 - chunk/tile highlighting (for removed obsolete marker feature)
 - additional ways to render a tile
