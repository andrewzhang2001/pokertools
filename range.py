class Range:
    """
    Defines a range of poker hands at any given spot. Based on all 1326 combos for each different suit
    """
    
    class Hand:

        def __init__(self, range, hand_str):
            self.range = range
            self.frequency = 0.0
            self.hand_str = hand_str
        
        def set_frequency(self, frequency: float):
            self.range.total_frequency -= self.frequency
            self.frequency = frequency
            self.range.total_frequency += self.frequency
            
    
    ranks = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    suits = ['c','d','h','s']
    cards = []
    
    for rank in ranks:
        for suit in suits:
            cards.append(rank + suit)


    def __init__(self, gtoplus_string: str):
        """
        Allows you to turn a GTO+ string into a range.
        Current plans are to support preflop where combos are identical. 
        May look to add support for postflop spots where this may differ in the future.
        """
        gto_array = gtoplus_string.split()
        self.hands = {}
        self.total_frequency = 0
        for i in range(len(Range.cards) - 1, -1, -1):
            self.hands[Range.cards[i]] = {}
            for j in range(i - 1, -1, -1):
                self.hands[Range.cards[i]][Range.cards[j]] = Range.Hand(self, Range.cards[i] + Range.cards[j])
        

print(Range.cards)
lj_string = '22:0.518,33:0.430,44:0.501,AA:0.999,QQ:0.999,99:0.999,66-55:0.999,ATo+:0.999,KQo:0.999,AJs+:0.999,A8s-A3s:0.999,K8s+:0.999,K6s:0.999,T9s:0.999,QTs:0.999,QJs:0.999,TT:1.000,77:1.000,A9s:1.000,ATs:1.000,Q9s:1.000,KK:0.998,JJ:0.998,88:0.998,JTs:0.998,A2s:0.493,54s:0.011,65s:0.330,76s:0.030,K7s:0.730,98s:0.452,T8s:0.329,J9s:0.360,QTo:0.328,KTo:0.394,QJo:0.237,KJo:0.668'
lj_range = Range(lj_string)