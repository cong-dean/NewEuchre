class Player():
    def __init__(self,name,number):
        self.name = name
        self.number = number
        self.voids = 4*[4*[0]]
        self.handvalue = 0
        self.handbu = []
        self.cards_outbu = []
    def getcards(self,replay):
        self.hand=[]
        if replay:
            self.hand=self.handbu[:]
            self.cards_out=self.cards_outbu[:]
        else:
            for card in range(5):
                self.hand.append(shuffledcards.pop())
            self.cards_out=card_values[:]
            for card in self.hand:
                del self.cards_out[self.cards_out.index(card)]

        self.handbu=self.hand[:]
        self.cards_outbu=self.cards_out[:]
        
    #Get all cards in a a given suit. Can be either in player's own hand or in known cards out.
    def setpartner(self,partner):
        self.partner=partner
    def setteam(self,team):
        self.team=team
    def setopposingteam(self,team):
        self.opposingteam=team
    def updatecards_out(self,card):
        del self.cards_out[self.cards_out.index(card)]
    def getleftbauer(trump_local)
        trumplist=[0,1,2,3]
        trumplist=trumplist[trump_local:]+trumplist[:trump_local]
        return (trumplist[2],2)
    def getsuit(self,suit,cards,trump_local):
        self.cardlist=[]
        for card in self.hand:
            if card == getleftbauer(trump_local):
                if suit == trump_local:
                    self.cardlist.append(card)
            else:
                if card[0]==suit:
                    self.cardlist.append(card)
        return self.cardlist

    def calc_card_point_value(trump_local,card_local):
        trumpvalues = [1,2,10,3,4,5] #bonus for 9, 10, jack, queen, king, ace
        if card_local = getleftbauer(trump_local):
            return 13    
        return (card_local[1] + 1) + (card_local[0]==trump_local) * trumpvalues(card_local[1]) #test how different values do in self-play mode


    def calc_handvalue(self,trump_local,upcard,bidding_round):
        #Total up hand value based on particular assumption of trump.
        #
        handvalue=0
        trial_hand=self.hand[:]
        if bidding_round==0 && self.number==dealer_num:
            trial_hand.append(upcard)
            trial_hand.remove(optimaldiscard(trial_hand)) #Note: Need to write this function.
        #If bidding round is 0, add/subtract to hand value based on partner dealer or opposing team dealer and value of upcard*
        if bidding_round==0:
            handvalue += (self.partner==Players[dealer_num])*calc_card_point_value(upcard[0],upcard)
            handvalue -= (self.team!=Players[dealer_num].team)*upcard[1]
        #Calculate cards in each suit
        suitcounts=4*[0]
        for suit in suitcounts:
            suitcounts[suit] = len(getsuit(suit),self,hand,trump_local)
        #Add value of cards in hand.
        for card in trial_hand:            
            handvalue+=calc_card_point_value(card)
            if card[0]!=trump_local && suitcounts[card[trump_local]] > 0 && suitcounts[card[0]] == 1: #Singleton has trump value.
                handvalue+=4 #Test this value in self-play mode.

    def showhand(self,trump_local,bidding_round):
        if isinstance(self,LivePlayer):
            print("\nYour hand:")
        else:
            print("\n"+self.name+"\'s hand:")
        self.hand.sort(key=lambda card: card[1]) #sort by position
        self.hand.sort(key=lambda card: card[0]) #sort by suit
        LB_local=(999,999)
        if bidding_round==0 and trump_local > -1: #NOTE: Bidding round is 0 in first round of bidding and after a bid is made
            LB_local=getleftbauer(trump_local)
            for card in self.hand:
                if card[0]==trump_local or card==LB_local:
                    trumpcards.append(card)
            selfhandmatch=self.hand[:]
            for card in selfhandmatch:
                if card in trumpcards: del self.hand[self.hand.index(card)] #removes trump cards from self.hand
            trumpcardvalues=[]
            trumpcards2=trumpcards[:]
            for card in trumpcards:
                trumpcardvalues.append(calc_card_point_value(trump_local,card)) #calculates values for trump cards
            def findkey(tup):
                return trumpcardvalues[trumpcards2.index(tup)]#function returns value of trump card by matching position of the card tuple (suit, position) in an unchanging master list of trump cards
            trumpcards.sort(key=findkey) #sorts trump cards according to their value
            for card in self.hand:
                trumpcards.append(card) #re-attaches cards from rest of hand to trump cards
            self.hand=trumpcards[:] #assigns new values to self.hand from foregoing
        if self.hand[0]==LB_local:
            currentsuit=trump
        else:
            currentsuit=self.hand[0][0]
        print(suitlabels[currentsuit]+": ",end="")
        for card in self.hand:
            if card==LB_local:
                if not card==self.hand[0]: print(", ",end='')
                print("Jack of "+suitlabels[card[0]]+" [left bauer]",end="")
            elif card[0]==currentsuit:
                if not card==self.hand[0]: print(", ",end='')
                print(positionlabels[card[1]]+((" of "+suitlabels[card[0]]+" [left bauer]")*(card==LB_local)),end='')
            else:
                currentsuit=card[0]
                print("\n"+suitlabels[card[0]]+": "+positionlabels[card[1]],end='')
        print("\n")

    def bid(self,bidding_round,player_position):
        self.handval=0
        #The following lowcut/highcut values are for testing optimal bid cut points in self-play mode.
        if self.team==Team1:
            lowcutR0=36
            lowcutR1=33
            highcutR0=49
            highcutR1=46
        else:
            lowcutR0=36
            lowcutR1=33
            highcutR0=49
            highcutR1=46
        if bidding_round==0:
            trump=upcard[0]
            self.handval=self.calc_handvalue(trump,0)
            if self.handval > lowcutR0:
                if self.handval > highcutR0:
                    bid_type=2
                else:
                    bid_type=1
            else:
                bid_type=0
        else: # next 7 lines will be accomplished in calc_handvalue
            x=[0,1,2,3]
            del x[upcard[0]]
            y=[0,0,0]
            count=0
            for trump in x:
                y[count]=self.calc_handvalue(trump,1)
                count +=1
            if max(y) > lowcutR1:
                if max(y) > highcutR1:
                    bid_type=2
                else:
                    bid_type=1
                trump=x[y.index(max(y))]
#                print(self.name+" has hand value "+str(max(y)))
            else:
                bid_type=0
        self.team.bid = bid_type
        return trump, bid_type  
    def lead(self,trump_local):
        #picks a card for leading a trick
        lead_card_values=[0]*len(self.hand)
        count=0
        for card in self.hand:
            #This section to determine value of leading with trump cards.
            if card[0]==trump_local or card == getleftbauer(trump_local):
                if self.partner==bidmaker or self==bidmaker:
                    lead_card_values[count] += 6
                else: lead_card_values[count] -= 4
                higher=0
                trumps_out=self.getsuit(trump_local,self.cards_out,trump_local)
                for card2 in trumps_out:
                    if calc_card_point_value(trump_local,card) < calc_card_point_value(trump_local,card2): higher += 1
                if higher==0: lead_card_values[count] += 2 #card is higher than trump cards still out in other players hand (or discard pile)
                lead_card_values[count] -= higher
                lead_card_values[count] += (len(self.getsuit(trump_local,self.hand,trump_local))-1) #trump card value as lead increased by other trump in hand
                lead_card_values[count] -= 2*(sum(self.voids[self.number])) #trump card value as lead descreased by voids in hand (missed opportunity to trump opponents' high off-suit cards)
                count += 1
            #This section to determine value of leading with non-trump cards.
            else:
                lower=0
                higher=0
                for card2 in self.getsuit(card[0],self.cards_out,trump_local):
                    if calc_card_point_value(trump_local,card) < calc_card_point_value(trump_local,card2): higher += 1
                    else: lower += 1
                if higher == 0: lead_card_values[count] += 2 #Card is high in suit.
                if (lower-higher) > 1: lead_card_values[count] +=1 #Of cards in same suit that are still out there, lower cards outnumber higher by more than 1.
                if higher > lower: lead_card_values[count] -=1 #Of cards in same suit that are still out there, more are higher than lower.
                if sum(self.voids[self.partner.number])> 0 and self.voids[self.partner.number][trump_local]==0: lead_card_values[count] += 2 #My partner could trump in.
                if self.voids[self.opposingteam.playerA.number][card[0]]==1:
                    if self.voids[self.opposingteam.playerA.number][trump_local]==1:
                        lead_card_values[count] += 1 #player in opposing team cannot beat, cannot trump
                    else: lead_card_values[count] -= 1 #player in opposing team has void, could possibly trump
                if self.voids[self.opposingteam.playerB.number][card[0]]==1:
                    if self.voids[self.opposingteam.playerB.number][trump_local]==1:
                        lead_card_values[count] += 1 #player in opposing team cannot beat, cannot trump
                    else: lead_card_values[count] -= 1 #player in opposing team has void, could possibly trump
                if len(self.getsuit(card[0],self.hand,trump_local))==1 and len(self.getsuit(trump_local,self.hand,trump_local))>0: lead_card_values[count] += 1 #could create a void in own hand, then trump
                count +=1
        leadcard=self.hand[lead_card_values.index(max(lead_card_values))]
        return leadcard # NOTE-If highest value is found in more than one card, the first card in hand will be chosen. 

    def follow(self,leadsuit_local,trump_local):
            follow_card_values=[]
            validcards = self.getsuit(leadsuit_local,self.hand,trump_local)
            trumpcards = self.getsuit(trump_local,self.hand,trump_local)
            validcardvalues = []
            trumpcardvalues = []
            for validcard in validcards:
                    validcardvalues.append(calc_card_point_value(trump_local,validcard))
            for trumpcard in trumpcards:
                    trumpcardvalues.append(calc_card_point_value(trump_local,trumpcard))
            if validcards:
                lowcard = validcards[validcardvalues.index(min(validcardvalues))]
                highcard = validcards[validcardvalues.index(max(validcardvalues))]
            if trumpcards:
                lowtrump = trumpcards[trumpcardvalues.index(min(trumpcardvalues))]
                hightrump = trumpcards[trumpcardvalues.index(max(trumpcardvalues))]
            if validcards:
                if Players[currentwinner_num]==self.partner:  # If your partner is winning....
                    partnercard=played_cards[tricksequence.index(self.partner)]
                    for card in self.getsuit(leadsuit_local,self.cards_out,trump_local):
                        if calc_card_point_value(trump_local,card) > calc_card_point_value(trump_local,partnercard): # And there's a within-suit card still out that's higher than partner's.
                            # NOTE: This will sometimes lead to playing a higher card than necessary--if in last position, will play highest card even when a lower might be sure to win; and if partner is just one step below.
                            if calc_card_point_value(trump_local,highcard) > calc_card_point_value(trump_local,partnercard):
                                return highcard #... and could lose to other in-suit card, then play my high card, if it beats partner's.
                    else: return lowcard
                else: # If partner not winning....
                    # NOTE: This will sometimes lead to playing a higher card than necessary.
                    if calc_card_point_value(trump_local,highcard) > max(played_cards_values): return highcard
                    else: return lowcard
            elif trumpcards:
                if Players[currentwinner_num]==self.partner:  # If your partner is winning....
                    partnercard=played_cards[tricksequence.index(self.partner)]
                    for card in self.getsuit(leadsuit_local,self.cards_out,trump_local):
                        if calc_card_point_value(trump_local,card) > calc_card_point_value(trump_local,partnercard):
                            if calc_card_point_value(trump_local,lowtrump) > calc_card_point_value(trump_local,partnercard): return lowtrump #... and could lose to other in-suit card, then play my lowest trump card, if it beats partner's.
                            elif calc_card_point_value(trump_local,hightrump) > calc_card_point_value(trump_local,partnercard): return hightrump
                else:
                    if calc_card_point_value(trump_local,lowtrump) > max(played_cards_values):
                        return lowtrump
                    else: 
                        if calc_card_point_value(trump_local,hightrump) > max(played_cards_values): 
                            return hightrump
                                    
            # If this point reached, cannot win trick. Play lowest card.
            for card in self.hand:
                    follow_card_values.append(calc_card_point_value(trump_local,card))
                    if self.getsuit(card[0],self.hand,trump_local) == 1: follow_card_values[len(follow_card_values)] -= 4
            followcard=self.hand[follow_card_values.index(min(follow_card_values))]
            return followcard  
    def play(self,leadsuit_local,trump_local):
        if tricksequence.index(self)==0: 
            play_card=self.lead(trump_local)
        else: play_card=self.follow(leadsuit_local,trump_local)
        del self.hand[self.hand.index(play_card)]
        return play_card

class LivePlayer(Player):
    def __init__(self,name,number):
        self.name = name
        self.number = number
        self.voids = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    def bid(self,bidding_round,player_position): #Does this override bid for Player class?
        if bidding_round==0:
            trump=upcard[0]
            handval=self.calc_handvalue(trump,0)
            validbids=[0,1,2,9]
            bid_type=999
            while bid_type not in validbids:
                try: bid_type=eval(input("\nDo you want to bid? (0=no; 1=yes; 2=go alone; 9=exit)"))
                except: bid_type=999
            if bid_type == 9: exit()
            roundinfo=[bid_type,hand,bidding_round,player_position,handval,trump,upcard,self.hand]
            bidding_data.append(roundinfo)
            self.team.bid = bid_type
            return trump, bid_type
        else:
            self.showhand(-1,1)
            validbids=[0,1,2]
            bid_type=999
            while bid_type not in validbids:
                try: bid_type=eval(input("\nDo you want to bid? (0=no; 1=yes; 2=go alone)"))
                except: bid_type=999
            if bid_type > 0:
                validtrump=[0,1,2,3]
                trump=999
                del validtrump[upcard[0]]
                while trump not in validtrump:
                    try: trump=eval(input("Which suit? (hearts=0, spades=1, diamonds=2, clubs=3)"))
                    except: trump=999
                    if trump==upcard[0]: print("You cannot bid "+suitlabels[upcard[0]]+".")
                handval=self.calc_handvalue(trump,1)
            else: #Need values if liveplayer passes on second round. Trump and handval are based on the strongest hand the player could have made.
                x=[0,1,2,3]
                del x[upcard[0]]
                y=[0,0,0]
                count=0
                for trump in x:
                    y[count]=self.calc_handvalue(trump,1)
                    count +=1
                handval=max(y)
                trump=x[y.index(max(y))]
                bid_type=0
            roundinfo=[bid_type,hand,bidding_round,player_position,handval,trump,upcard,self.hand]
            bidding_data.append(roundinfo)
            self.team.bid = bid_type
            return trump, bid_type
    def play(self,leadsuit_local,trump_local):
        self.showhand(trump_local,0)
        legit=[x+1 for x in range(len(self.hand))]
        pc = 999
        while pc not in legit:
            try: pc = eval(input("Which card? (1 through "+str(len(self.hand))+"): "))
            except: pc = 999
            if pc in legit:
                if tricksequence.index(self) > 0:
                    if len(self.getsuit(leadsuit_local,self.hand,trump_local)) > 0:
                        if self.hand[pc-1] == getleftbauer(trump_local) and leadsuit==trump_local: pass
                        elif self.hand[pc-1][0] != leadsuit_local and (pc in legit):
                            print("Must follow lead suit.")
                            pc = 99
        play_card=self.hand[pc-1]
        del self.hand[pc-1]
        return play_card
                  