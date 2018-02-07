# pygmalion

A proof-of-concept game+engine built on pygame.

###### TODO:
 - isolate particular test game from general mechanics
 - isolate stuck-to-player and stationary modes from general camera class
 - remove floating-point calculations, 'cause you don't really need millionths of pixels (10ths or 16ths, maybe even 100ths, right, but not _that_)
    - change display scaling to use target sizes instead of factors
    - bug: chunks overlapping by 1px
 - debug feature: chunk/tile highlighting (for removed obsolete marker feature)
