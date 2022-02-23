class Range:
    """
    Defines a range of poker hands at any given spot. Based on all 1326 combos for each different suit
    """
    
    class Hand:

        def __init__(self, range, hand_str):
            self.range = range
            self.frequency = 0.0
            self.hand_str = hand_str
            assert len(hand_str) == 4
            self.suit_one = hand_str[1]
            self.suit_two = hand_str[3]
            self.big_rank = hand_str[0] if Range.rank_map[hand_str[0]] > Range.rank_map[hand_str[2]] else hand_str[2]
            self.small_rank = hand_str[0] if Range.rank_map[hand_str[0]] <= Range.rank_map[hand_str[2]] else hand_str[2]
        
        def set_frequency(self, frequency: float):
            self.range.total_frequency -= self.frequency
            self.frequency = frequency
            self.range.total_frequency += self.frequency

        def get_frequency(self):
            return self.frequency

        def is_offsuit(self) -> bool:
            return self.suit_one != self.suit_two
        
        def is_suited(self) -> bool:
            return self.suit_one == self.suit_two

        def __str__(self):
            return self.hand_str + ': ' + str(self.frequency)

        def __repr__(self):
            return self.__str__()

        
    
    ranks = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    rank_map = {'2': 0, '3': 1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7,'T':8, 'J':9, 'Q': 10, 'K':11, 'A': 12}
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
        To-do: Add support for parent range (i.e. have another argument as gtoplus_parent_string = 'full')
            Default range will be 100% of all hands.
        """
        
        self.hands = {}
        self.total_frequency = 0
        for i in range(len(Range.cards) - 1, -1, -1):
            self.hands[Range.cards[i]] = {}
            for j in range(i - 1, -1, -1):
                self.hands[Range.cards[i]][Range.cards[j]] = Range.Hand(self, Range.cards[i] + Range.cards[j])

        gto_array = gtoplus_string.split(',')
        for data in gto_array:
            print(data)
            hands, freq = data.split(':')
            freq = float(freq)
            hands_objects = self.enumerate_hands(hands)
            for hand_object in hands_objects:
                hand_object.set_frequency(round(freq, 2))
                print(hand_object)

    def get_hand(self, hand_str: str) -> Hand:
        """
        Returns the object representation of a specific Hand
        """
        card_one = hand_str[:2]
        card_two = hand_str[2:4]
        if card_two in self.hands[card_one]:
            return self.hands[card_one][card_two]
        elif card_one in self.hands[card_two]:
            return self.hands[card_two][card_one]
        else:
            print('Invalid hand' + hand_str)
            return None

    def get_frequency(self, hand_str: str) -> float:
        hand = self.get_hand(hand_str)
        if hand is None:
            return None
        return hand.get_frequency()

    def enumerate_hand(self, hand_class:str) -> list:
        """
        Converts notation like 'AJo' or '22' or 'JTs' or '72' into its hand class.
        To-do: Add support for input like JcTs.
        """

        #Should be a preflop query i.e. JTs, JTo, or 72
        if (len(hand_class) == 2 or len(hand_class) == 3):
            rank_one = hand_class[0]
            rank_two = hand_class[1]
            #Dont check for offsuit combinations if we specify suited
            no_offsuit_query = hand_class[-1] == 's'
            #Dont check for suited combinations if we specify offsuit OR pocket pair
            no_suited_query = hand_class[-1] == 'o' or rank_one == rank_two
            return_hands = set()

            for suit_one in Range.suits:
                for suit_two in Range.suits:
                    #Do offsuit queries iff we are doing 
                    if suit_one != suit_two and not no_offsuit_query:
                        return_hands.add(self.get_hand(rank_one + suit_one + rank_two + suit_two))
                    elif suit_one == suit_two and not no_suited_query:
                        return_hands.add(self.get_hand(rank_one + suit_one + rank_two + suit_two))
            return return_hands
        #Should be of format JcTh
        elif len(hand_class) == 4:
            return [self.get_hand(hand_class)]
        

    def enumerate_hands(self, hands_class: str) -> list:
        """
        Converts notation like 'AJo+', 'A8s-A3s', 'AK,' 'JJ+' to a list of all hands in satisfying that class 
        """
        width_hands = hands_class.split('-')
        #Format 'AK', 'AJo', 'A5s+', 'AT+', '22+'
        if len(width_hands) == 1:
            #Case 1: One hand (i.e. 'AK' or 'AJo')
            if not hands_class[-1] == '+':
                return self.enumerate_hand(hands_class)
            #Case 2: Range of hands with + symbol (i.e  AJo+, 22+)
            else:
                return_hands = []
                first_index = Range.rank_map[hands_class[0]]
                second_index = Range.rank_map[hands_class[1]]
                paired = first_index == second_index
                #Non-paired
                if not paired:
                    for i in range(second_index, first_index):
                        return_hands.extend(self.enumerate_hand(hands_class[0] + Range.ranks[i] + hands_class[2:-1]))
                #Paired
                else:
                    for i in range(first_index, Range.rank_map['A'] + 1):
                        return_hands.extend(self.enumerate_hand(Range.ranks[i] + Range.ranks[i]))                        
                return return_hands
        elif len(width_hands) == 2:
            rank_zero_zero = width_hands[0][0]
            rank_zero_one = width_hands[0][1]
            rank_one_zero = width_hands[1][0]
            rank_one_one = width_hands[1][1]
            paired = rank_zero_zero == rank_zero_one
            #Case 1: Pairs
            return_hands = []
            if paired:
                print(Range.rank_map[rank_one_zero], Range.rank_map[rank_zero_zero] + 1)
                for i in range(Range.rank_map[rank_one_zero], Range.rank_map[rank_zero_zero] + 1):
                    return_hands.extend(self.enumerate_hand(Range.ranks[i] + Range.ranks[i]))
            else:
                for i in range(Range.rank_map[rank_one_one], Range.rank_map[rank_zero_one] + 1):
                    return_hands.extend(self.enumerate_hand(rank_zero_zero + Range.ranks[i] + width_hands[0][2:]))
            return return_hands


    def get_range_frequency(self) -> float:
        return self.total_frequency / 1326
    
        
def test_lj():
    lj_string = '22:0.518,33:0.430,44:0.501,AA:0.999,QQ:0.999,99:0.999,66-55:0.999,ATo+:0.999,KQo:0.999,AJs+:0.999,A8s-A3s:0.999,K8s+:0.999,K6s:0.999,T9s:0.999,QTs:0.999,QJs:0.999,TT:1.000,77:1.000,A9s:1.000,ATs:1.000,Q9s:1.000,KK:0.998,JJ:0.998,88:0.998,JTs:0.998,A2s:0.493,54s:0.011,65s:0.330,76s:0.030,K7s:0.730,98s:0.452,T8s:0.329,J9s:0.360,QTo:0.328,KTo:0.394,QJo:0.237,KJo:0.668'
    lj_range = Range(lj_string)
    print(lj_range.get_range_frequency())

def test_hj():
    hj_string = '22:0.607,33:0.882,KK+:0.998,JJ-44:0.998,ATo:0.998,AQo:0.998,KJo:0.998,AJs+:0.998,KTs-K8s:0.998,Q8s+:0.998,A3s:0.998,A4s:0.998,A6s:0.998,A8s:0.998,A9s:0.998,K5s:0.998,76s:0.998,K6s:0.998,87s:0.998,98s:0.998,T8s:0.998,T9s:0.998,JTs:0.998,KQs:0.998,A2s:1.000,ATs:1.000,65s:1.000,K7s:1.000,QQ:0.996,AJo:0.996,AKo:0.996,KQo:0.996,A5s:0.996,A7s:0.996,J9s:0.996,KJs:0.996,A9o:0.064,54s:0.242,86s:0.050,97s:0.802,QTo:0.846,KTo:0.820,QJo:0.693'
    hj_range = Range(hj_string)
    print(hj_range.get_range_frequency())

def test_co():
    co_string = 'KK:1.000,JJ:1.000,77:1.000,22:1.000,A5s:1.000,A7s:1.000,AQs:1.000,65s:1.000,86s:1.000,96s:1.000,K6s:1.000,Q8s:1.000,Q9s:1.000,K9s:1.000,QQ:0.998,99-88:0.998,66-33:0.998,A9:0.998,JT:0.998,QT:0.998,KJ:0.998,AKo:0.998,KQo:0.998,T7s+:0.998,A2s:0.998,A3s:0.998,A8s:0.998,AJs:0.998,54s:0.998,K4s:0.998,K5s:0.998,76s:0.998,Q6s:0.998,87s:0.998,97s:0.998,Q7s:0.998,K7s:0.998,98s:0.998,K8s:0.998,J9s:0.998,KTs:0.998,QJs:0.998,AA:0.996,TT:0.996,AQo-ATo:0.996,KTo:0.996,QJo:0.996,A4s:0.996,A6s:0.996,ATs:0.996,AKs:0.996,75s:0.996,J8s:0.996,KQs:0.996,A5o:0.615,A8o:0.595,K3s:0.559,64s:0.146,Q5s:0.711,T6s:0.008,T9o:0.529,K9o:0.004'
    co_range = Range(co_string)
    print(co_range.get_range_frequency())

def test_bu():
    bu_string = 'JJ+:0.996,99:0.996,22:0.996,A4:0.996,A8:0.996,QT:0.996,KTo+:0.996,AKo:0.996,98o:0.996,J9o:0.996,JTo:0.996,QJo:0.996,Q6s-Q4s:0.996,J9s-J7s:0.996,T7s+:0.996,97s-95s:0.996,A6s:0.996,74s:0.996,75s:0.996,T5s:0.996,K5s:0.996,76s:0.996,K6s:0.996,87s:0.996,Q8s:0.996,K9s:0.996,KJs:0.996,TT:0.994,77:0.994,44-33:0.994,A5:0.994,A9:0.994,Q9:0.994,AJo:0.994,T8o:0.994,K9o:0.994,K4s-K2s:0.994,A3s:0.994,AQs:0.994,53s:0.994,Q3s:0.994,T4s:0.994,86s:0.994,T6s:0.994,J6s:0.994,Q7s:0.994,K7s:0.994,K8s:0.994,QJs:0.994,55:0.992,A2s:0.992,65s:0.992,98s:0.992,KTs:0.992,88:0.998,66:0.998,AT:0.998,A6o:0.998,AQo:0.998,T9o:0.998,A7s:0.998,AJs:0.998,AKs:0.998,54s:0.998,64s:0.998,85s:0.998,J5s:0.998,JTs:0.998,KQs:0.998,A3o:0.713,A7o:1.000,Q2s:0.018,J4s:0.871,K6o:0.012,87o:0.213,K8o:0.404'
    bu_range = Range(bu_string)
    print(bu_range.get_range_frequency())

def test_sb_limp():
    sb_limp_string = '22:0.551,33:0.504,44:0.461,55:0.448,66:0.418,77:0.414,88:0.388,99:0.277,AA:0.128,A2s:0.646,A2o:0.049,A3s:0.535,A3o:1.000,Q2s:1.000,J3s:1.000,A4s:0.489,A4o:0.611,A5s:0.587,A5o:0.144,Q7s:0.144,A6s:0.666,A6o:0.375,K6s:0.375,A7s:0.536,A7o:0.349,A8s:0.073,A8o:0.108,A9s:0.026,A9o:0.117,ATs:0.022,ATo:0.314,AJs:0.199,AJo:0.268,AQs:0.201,AQo:0.163,AKs:0.025,TT:0.221,AKo:0.221,52s:0.217,J2s:0.807,K2s:0.196,43s:0.333,53s:0.214,63s:0.451,T3s:0.111,QTo:0.432,Q3s:0.432,K3s:0.125,54s:0.289,54o:0.057,64s:0.080,74s:0.284,K4s:0.284,84s:0.215,T4s:0.993,J4s:0.595,Q4s:0.242,65s:0.177,65o:0.364,75s:0.169,85s:0.088,95s:0.629,T5s:0.722,J5s:0.428,Q5s:0.216,K5s:0.358,76s:0.251,96s:0.251,76o:0.567,86s:0.254,T6s:0.011,J6s:0.136,Q6s:0.156,K6o:0.261,KTo:0.439,87s:0.439,87o:0.501,97s:0.228,97o:0.296,T7s:0.312,J7s:0.007,K7s:0.434,K7o:0.921,98s:0.733,98o:0.338,T8s:0.594,T8o:0.392,J8s:0.474,J8o:0.511,Q8s:0.487,Q8o:0.823,K8s:0.470,K8o:0.507,T9s:0.382,T9o:0.336,J9s:0.630,J9o:0.435,Q9s:0.645,Q9o:0.352,K9s:0.381,K9o:0.173,JTs:0.044,JTo:0.433,QTs:0.047,KTs:0.033,JJ:0.194,QJs:0.036,QJo:0.387,KJs:0.064,KJo:0.344,QQ:0.204,KQs:0.200,KQo:0.281,KK:0.327'
    sb_limp_range = Range(sb_limp_string)
    print(sb_limp_range.get_range_frequency())

def test_sb_vs_bu_3bet_range():
    sb_raise_string = '55:0.336,66:0.718,77:0.834,88:0.852,99:0.842,AA:1.000,JJ:1.000,AK:1.000,AQs:1.000,A4s:0.638,KK-QQ:0.998,A5s:0.998,KQs:0.998,A6s:0.008,A7s:0.806,A8s:0.404,A9s:0.658,ATs:0.764,98s:0.764,ATo:0.946,AJs:0.986,AJo:0.942,AQo:0.896,65s:0.022,76s:0.072,87s:0.126,K7s:0.004,T8s:0.968,K8s:0.048,T9s:0.958,J9s:0.944,Q9s:0.700,K9s:0.874,TT:0.954,JTs:0.924,QTs:0.854,KTs:0.850,KTo:0.624,QJs:0.714,KJs:0.908,KJo:0.326,KQo:0.904'
    sb_raise_range = Range(sb_raise_string)
    print(sb_raise_range.get_range_frequency())

def test_bu_call_vs_sb_3bet_range():
    bu_call_3bet_string = '22:0.412,33:0.722,44:0.680,55:0.611,66:0.873,77:0.706,AJo:0.706,88:0.863,99:0.775,A4s:0.356,A5s:0.797,A8s:0.425,A9s:1.000,ATs:0.938,AJs:0.958,KTs:0.958,AQ:0.984,65s:0.771,76s:0.961,87s:0.389,98s:0.725,T8s:0.268,T9s:0.899,J9s:0.781,Q9s:0.033,K9s:0.732,TT:0.497,JTs:0.987,QTs:0.977,JJ:0.141,QJs:0.542,KJs:0.967,KQs:0.876,KQo:0.761'
    bu_call_range = Range(bu_call_3bet_string)
    print(bu_call_range.get_range_frequency())

def test_bu_4bet_vs_sb_range():
    bu_4bet_string = '44:0.035,55:0.279,66:0.051,77:0.192,88:0.090,99:0.151,J9s:0.151,AA:0.929,A3s:0.372,A4s:0.519,A5s:0.106,A7s:0.016,A8s:0.465,A9s:0.064,ATo:0.529,AJo:0.234,AKs:0.971,AKo:0.968,54s:0.003,65s:0.003,QTs:0.003,K6s:0.010,98s:0.237,T8s:0.112,K8s:0.048,Q9s:0.340,K9s:0.231,TT:0.497,JJ:0.814,QJs:0.413,KJo:0.218,QQ:0.926,KQo:0.205,KK:1.000'
    bu_4bet_range = Range(bu_4bet_string)
    print(bu_4bet_range.get_range_frequency())
