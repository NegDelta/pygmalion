# pygmalion

A proof-of-concept game+engine built on pygame.

##### TODO:
 - isolate particular test game from general mechanics
   - `pygmalion.py` for engine and `game.py` for game
   - master game object with initialization checklist 
   - `Asset` class
     - disallow registering assets after game init 
   - encapsulated tiletype list
 - rework camera ontology
   - either bound to movable or stationary
   - enable dynamic switching between the modes
 - chunk/tile highlighting (for removed obsolete marker feature)
 - additional ways to render a tile
