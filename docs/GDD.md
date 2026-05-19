Alien Mayonnaise
By GEA Innovation Studios - All rights reserved

Das hier ist das Game Design Document (GDD), hier wird das Spiel, die dev Checkliste und gameplay Strategien beschrieben. 

1. Das Spiel
In Alien Mayonnaise kann man sich mit zwei Spieler auf ein Bildshirm bewegen und schießen. Alle spieler haben maximal 10 Leben, der erste mit 0 Leben explodiert und verschwindet vom Bildschirm. Gewinner ist der, der als letztes noch am Leben bleibtBeide Spieler können auf der selben Tastatur spielen und beide Tastenbelegungen können geändert werden.

2. Dev Checkliste:
[x] Pygame Fenster
|-> [x] Das Fenster
|-> [x] Hintergrund
|-> [x] Event loop mit ticker, 50fps

[x] PlayerEntity
|-> [x] Platzierung auf dem Bildschirm
|-> [x] Custom Texturen
|-> [x] Bewegung in allen richtungen
|-> [x] Collisions check mit hitbox (Player)
|-> [ ] Collisions check mit hitbox (BlockEntities)
|-> [x] .shoot() Funktion die eine neue ProjectileEntity erstellt
|-> [x] Leben und sterben

[x] ProjectileEntity
|-> [x] Auf dem Bildschirm platzieren
|-> [x] In die richtung vom schützen fliegen
[x] PlayerEntity mit
