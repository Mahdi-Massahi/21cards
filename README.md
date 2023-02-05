## Rules of the game
- There is one user called Bank. 
- At most there should be 3 users called "players" per deck.
- Card's suit is not important.
- The jocker does not play.
- Card 2 to 10 has their normal point values.
- King has 3 point, Queen 2 points, and Jack 1 point.
- Ace is 1 or 11 points. 
- Ace is 11 unless it busts the hand.
- Cards must be pre-shuffeled.


## Defenitions
### stand
hold the total points and end the turn and finish playing

### hit
ask for a card  

### split
if the user holds 2 initial cards with the same points in a set, user can split it into two sets which allows player to play twice; one game per card. The bet does not split but both cards get original bet amount.  

### bust
when the user's points exceed 21

### winner
who gets the bet  


## Flow
1. game starts by giving each user (bank and players) a card.
2. players place their bets. (bank does too - equivalent to the amount which players bet)
3. players recieve their second card (but not the bank - considering programming simplicity as its not in contrast with rule no. 3 at Bank). (blackjack is ignored here)
4. players choose whether stand, hit, or split one by one as an action if they can (Player's rules), untill they stand or bust.  
    - at each hit we should check player for being bust
    - if player has more than one set, the same rules are applied for each set independently
5. bank reveals her second card (equivalet to one hit for the bank). (blackjack is ignored here)
6. bank hit if she can untill she bust or stand (Bank's rules)
7. evaluate
8. make the charges


### Evaluate
- note that some players or bank may have already bust
1. if the bank and player both bust, the bank wins.
2. if the bank bust, all standing players win and the game is over.
3. if the player's points is less than or equal to the bank's points, the bank wins. Else the the player wins.


### Bank
1. bank plays if all players are stand or bust and there are players who are not bust.
2. bank must hit when it has a total of 16 points or less.
3. bank must stand with a total of 17 points or more.


### Player
1. busted player should be skipped 


## Extra assumptions
Some points which were not included in the provided document are as follows:
1. minimum number of users is 2
2. player can split more than once 
3. ace split rule of blackjack is ignored
4. insurance is ignored
5. balckjak is ignored (winning right away by 2 cards equal to 21 before the bank reveals her second card)

-----

# How to run
simply just execute the 'main.py' file. No extra requirement is required.