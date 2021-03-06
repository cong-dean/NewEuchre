# This section is for setting global variables and importing methods.
# Change from github.com

card_values=[(x, y) for x in range(4) for y in range(6)]
suitlabels=['Hearts','Spades','Diamonds','Clubs'] #Having same-color suits two apart enables actions recognizing their complementary relationship in Euchre.
positionlabels=['9','10','Jack','Queen','King','Ace']
Playernames=['Sam','Kim','Sue','Tim']
realplayer=99
realplayer_responses=[0,1,9]
name = ""
hands=0
hand=0
bidding_data=[]
games = 0
game = 0
leadsuit = -1
lpactive = 0 # By default, there's no live player.
bidding_round = 0 #NOTE: With respect to the function showhand, bidding_round just serves to distinguish between when trump is known (0) and when it isn't (1).
replay = 1 # 1 == "no"
upcard =[]

from random import shuffle
from random import randint
from player import Player, LivePlayer
from team import Team

def labelcard(suit,position):
    'Labels cards in a way comprehensible to user.'
    return str('the '+positionlabels[position]+' of '+suitlabels[suit])

def calc_card_point_value(trump_local,card_local): #calculates card point value at bid time
            value = card_local[1]
            if card_local[0]==trump_local:
                if card_local[1]==2:
                    value += 16
                else: value += 6
            if abs(card_local[0]-trump_local)==2 and card_local[1]==2:
                value += 13 #Sets value of left bauer.
            return value


while realplayer not in realplayer_responses:
    try: realplayer = eval(input("Do you want to be a player? 1=yes, 0= no): "))
    except: realplayer==99
    if realplayer==1:
        Player0=LivePlayer("You",0)
        lpactive=1
    elif realplayer==0:
        Player0=Player(Playernames[0],0)

Player1=Player(Playernames[1],1)
Player2=Player(Playernames[2],2)
Player3=Player(Playernames[3],3)
Players=[Player0, Player1, Player2, Player3]

Team1 = Team(1)
Team2 = Team(2)

Team1.setopposingteam(Team2)
Team2.setopposingteam(Team1)

Teams=[Team1,Team2]

while not games:
    try: games = eval(input("How many games?"))
    except: games=0
    if games>200 and lpactive:
        games=0
        print("Too many!")
    if games<0: games=0

# Start game.

if lpactive: print("Your partner is Sue.")

positions = [0,1,2,3]
nextdealer_num = randint(0,3)

team1score=0
team2score=0
teamscores=[team1score,team2score]

while game < games:
    # Dealing
    if not(replay==2):
        dealer_num = nextdealer_num
    if lpactive: print("\n\nThe dealer is "+Players[dealer_num].name+".")
    Team1.trickcount=0
    Team2.trickcount=0
    alone=0
    shuffledcards=card_values[:]
    shuffle(shuffledcards)
    for player in range(4):
        Players[player].getcards()
    if replay == 2:
        upcard=upcardbu[:]
    else:
        upcard=shuffledcards[0]
        upcardbu=upcard[:]
    trump=upcard[0]
    if lpactive: print("The up-card is "+labelcard(upcard[0],upcard[1]))
    for player in range(4):
        if lpactive and player==0: Players[player].showhand(trump,0)
    dealers = positions[dealer_num:]+positions[:dealer_num]
    nextdealer_num = Players[dealers[1]].number
    firstbidder_num = Players[dealers[1]].number
    bidders = positions[firstbidder_num:]+positions[:firstbidder_num]    
    # Bidding
    bidding_round=0
    bid = 0
    for bidder_num in bidders:
        bid=Players[bidder_num].bid(0,bidders.index(bidder_num)) # Second parameter is "player position" in bidding order, currently stored when recording live player data. May have other uses.
        bid_type=bid[1]
        if bid_type > 0:
            bidmaker = Players[bidder_num]
            Players[dealer_num].hand.append(upcard)
            if isinstance(Players[dealer_num],LivePlayer): # If the LivePlayer needs to discard, the following is skipped. LP must be prompted to discard below.
                pass
            else:
                handbackup = Players[dealer_num].hand[:]
                discardvalues=[]
                for discard in range(6):
                    Players[dealer_num].hand=handbackup[:]
                    del(Players[dealer_num].hand[discard])
                    discardvalues.append(Players[dealer_num].calc_handvalue(trump,0))
                Players[dealer_num].hand = handbackup
                del(Players[dealer_num].hand[discardvalues.index(max(discardvalues))]) # Discards from dealers hand the card that resulted in highest hand value when discarded.
        if bid_type == 0:
            if lpactive: print(Players[bidder_num].name+" passes.")
            continue
        else:
            if bid_type==2: alone=1
            action=" orders "
            if bidder_num==dealer_num: action=" picks "
            if lpactive: print(Players[bidder_num].name+action+"up "+labelcard(upcard[0],upcard[1])+(". Going alone"*alone)+".")
            if isinstance(Players[dealer_num],LivePlayer):
                validdiscards=[1,2,3,4,5,6]
                lpdiscard=999
                Player0.showhand(trump,0)
                while lpdiscard not in validdiscards:
                    try: lpdiscard=eval(input("\nWhich card do you want to discard? (1 through 6)"))
                    except: lpdiscard=999
                del Player0.hand[lpdiscard-1]
        break
    if bid_type==0: #round of bidding in other suits, if bid_type is still 0.
        for bidder_num in bidders:
            Players[bidder_num].updatecards_out(upcard)
        for bidder_num in bidders:
            bid=Players[bidder_num].bid(1,bidders.index(bidder_num))
            trump=bid[0]
            bid_type=bid[1]
            if bid_type > 0:
                bidmaker = Players[bidder_num]
            if bid_type == 0:
                if lpactive: print(Players[bidder_num].name+" passes.")
                continue
            else:
                if bid_type==2: alone=1
                if lpactive: print(Players[bidder_num].name+" bids "+suitlabels[trump]+(" alone"*alone)+".")
                break            
    if bid_type==0:
        if lpactive: print("No one bids. Redeal!")
        continue
    else:
        trumplist=[0,1,2,3]
        trumplist=trumplist[trump:]+trumplist[:trump]
        LB=(trumplist[2],2)        
        # Playing
        trickcount=1
        Team1.trickscore=0
        Team2.trickscore=0
        for player in Players:
            player.voids=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        for trick in range(5):
            if lpactive: print("\nTrick "+str(trickcount)+": ")
            played_cards=[] # Cards played in trick
            played_cards_values=[] # Values of cards played in trick
            if trickcount==1: leader_num=firstbidder_num
            else: leader_num=currentwinner_num
            tricksequence=Players[leader_num:]+Players[0:leader_num]
            if bid_type == 2:
                tricksequence.remove(bidmaker.partner)
            for player in tricksequence:
                played_card=(player.play(leadsuit,trump))
                if player == tricksequence[0]:
                    leadsuit = played_card[0]
                    if played_card==LB: leadsuit = trump
                if lpactive: print(player.name+" plays "+labelcard(played_card[0],played_card[1])+".")
                played_cards.append(played_card)
                if not(played_card[0])==leadsuit:
                    for player2 in Players:
                        player2.voids[player.number][leadsuit]=1 # All players update their known voids if the see current player not following suit. NOTE: This would be better if it could somehow be assessed at the end of the trick. Otherwise, players are playing as if people who have already played in trick could trump in.
                for player2 in Players:
                    if not(player2==player):
                        player2.updatecards_out(played_card) # All players update the cards they know are out.
                    for suit in range(4):
                        if len(player2.getsuit(suit,player2.cards_out,trump))== 0:
                            for player3 in Players:
                                player3.voids[player2.number][suit]=1  # If player knows, based on played cards and own hand, there's a void in a suit, this is registered as a void for all players, only known to player.
                if played_card[0]==leadsuit or played_card==LB:
                    played_cards_values.append(calc_card_point_value(trump,played_card))
                elif played_card[0]==trump:
                    played_cards_values.append(calc_card_point_value(trump,played_card))
                else: played_cards_values.append(-1)
                currentwinner_num=tricksequence[played_cards_values.index(max(played_cards_values))].number #i.e., the current winner number is the number of the player in the tricksequence whose card value is currently highest among all played cards.
            Players[currentwinner_num].team.trickscore += 1
            trickcount += 1
            if lpactive: print("\n"+Players[currentwinner_num].name+" wins trick!")
        for team in Teams:
            if team.bid==0:
                if team.trickscore > 2: 
                    team.score += 2
                    roundwinner = team
            if team.bid==1:
                if team.trickscore > 2: 
                    team.score += 1
                    roundwinner = team
                if team.trickscore > 4:
                    team.score += 1
            if team.bid==2:
                if team.trickscore > 2: 
                    team.score += 1
                    roundwinner = team
                if team.trickscore > 4: team.score += 3
        # End of round
        if lpactive: print(roundwinner.name+" wins round!")
        if lpactive: print("Team 1 score: "+str(Team1.score)+"; Team 2 score: "+str(Team2.score))
        if lpactive: print("Team 1 trick count:"+str(Team1.trickscore)+"; Team 2 trick count: "+str(Team2.trickscore))
        teamscores=[Team1.score,Team2.score]
        # This is the part where I'll try to make it possible to replay a hand.
        replay=0
        while not replay:
            try: replay=eval(input("\nReplay hand? (1 = no, 2 = yes)"))
            except: lpdiscard=999
        if replay == 2:
            for team in Teams:
                if team.bid==0:
                    if team.trickscore > 2: 
                        team.score += (-2)
                if team.bid==1:
                    if team.trickscore > 2: 
                        team.score += (-1)
                    if team.trickscore > 4:
                        team.score += (-1)
                if team.bid==2:
                    if team.trickscore > 2: 
                        team.score += (-1)
                    if team.trickscore > 4: team.score += (-3)
            
        if max(teamscores)>9:
            if lpactive: print("Team "+str(teamscores.index(max(teamscores))+1)+" wins game "+str(game)+"!")
            Teams[teamscores.index(max(teamscores))].gamescore += 1
            Team1.score=0
            Team2.score=0
            game += 1
            if lpactive: print("END OF GAME "+str(game))
            if lpactive: print("Team1 game wins=",Team1.gamescore," Team2 game wins=",Team2.gamescore)

if lpactive: print("Team1 game wins=",Team1.gamescore," Team2 game wins=",Team2.gamescore)
    


