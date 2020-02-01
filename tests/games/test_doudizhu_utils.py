import unittest

from rlcard.games.doudizhu.utils import CARD_TYPE, DoudizhuRule
from rlcard.games.doudizhu.judger import DoudizhuJudger as Judger

class TestDoudizhuUtils(unittest.TestCase):

    def test_DoudizhuRule_get_solo(self):
        #solo
        hand = '334445555689JQBR'
        in_cards = ('3', '4', '5', '6', '8', '9', 'J', 'Q', 'B', 'R')
        playable_cards = DoudizhuRule(hand).playable_cards('solo')
        for e in in_cards:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards)

    def test_DoudizhuRule_get_pair(self):
        #pair
        hand = '334445555689JQBR'
        in_cards  = ('33', '44', '55')
        playable_cards = DoudizhuRule(hand).playable_cards('pair')
        for e in in_cards:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards)

    def test_DoudizhuRule_get_trio(self):
        #trio
        hand = '334445555689JQBR'
        in_cards = ('444', '555')
        playable_cards = DoudizhuRule(hand).playable_cards('trio')
        for e in in_cards:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards)

    def test_DoudizhuRule_get_bomb(self):
        #bomb
        hand = '334445555689JJJJQBR'
        in_cards = ('5555', 'JJJJ')
        playable_cards = DoudizhuRule(hand).playable_cards('bomb')
        for e in in_cards:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards)

    def test_DoudizhuRule_get_rocket(self):
        #rocket
        hand = '334445555689JQBR'
        in_cards = ('BR', )
        playable_cards = DoudizhuRule(hand).playable_cards('rocket')
        for e in in_cards:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards)

    def test_DoudizhuRule_get_solo_chain(self):
        hand = '3344455556789TJQKA2BR'

        #solo_chain_5 -- #solo_chain_12 
        in_cards_5 = ('34567', '45678', '56789', '6789T', '789TJ', 
            '89TJQ', '9TJQK', 'TJQKA')
        playable_cards = DoudizhuRule(hand).playable_cards('solo_chain_5')
        for e in in_cards_5:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_5)

        in_cards_6 = ('345678', '456789', '56789T', '6789TJ', '789TJQ', 
            '89TJQK', '9TJQKA')
        playable_cards = DoudizhuRule(hand).playable_cards('solo_chain_6')
        for e in in_cards_6:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_6)

        in_cards_7 = ('3456789', '456789T', '56789TJ', '6789TJQ', '789TJQK', 
            '89TJQKA')
        playable_cards = DoudizhuRule(hand).playable_cards('solo_chain_7')
        for e in in_cards_7:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_7)

        in_cards_8 = ('3456789T', '456789TJ', '56789TJQ', '6789TJQK', '789TJQKA')
        playable_cards = DoudizhuRule(hand).playable_cards('solo_chain_8')
        for e in in_cards_8:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_8)

        in_cards_9 = ('3456789TJ', '456789TJQ', '56789TJQK', '6789TJQKA')
        playable_cards = DoudizhuRule(hand).playable_cards('solo_chain_9')
        for e in in_cards_9:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_9)

        in_cards_10 = ('3456789TJQ', '456789TJQK', '56789TJQKA')
        playable_cards = DoudizhuRule(hand).playable_cards('solo_chain_10')
        for e in in_cards_10:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_10)

        in_cards_11 = ('3456789TJQK', '456789TJQKA')
        playable_cards = DoudizhuRule(hand).playable_cards('solo_chain_11')
        for e in in_cards_11:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_11)

        in_cards_12 = ('3456789TJQKA', )
        playable_cards = DoudizhuRule(hand).playable_cards('solo_chain_12')
        for e in in_cards_12:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_12)

    def test_DoudizhuRule_get_pair_chain(self):
        hand =  '33444555566778899TTJJQQKKAA22'

        #pair_chain_3 -- #pair_chain_10
        in_cards_3 = ('334455','445566', '556677', '667788', '778899', 
            '8899TT', '99TTJJ', 'TTJJQQ', 'JJQQKK', 'QQKKAA') 
        playable_cards = DoudizhuRule(hand).playable_cards('pair_chain_3')
        for e in in_cards_3:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_3)
        
        in_cards_4 = ('33445566','44556677', '55667788', '66778899', '778899TT', 
            '8899TTJJ', '99TTJJQQ', 'TTJJQQKK', 'JJQQKKAA')
        playable_cards = DoudizhuRule(hand).playable_cards('pair_chain_4')
        for e in in_cards_4:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_4)

        in_cards_5 = ('3344556677','4455667788', '5566778899', '66778899TT', 
            '778899TTJJ', '8899TTJJQQ', '99TTJJQQKK', 'TTJJQQKKAA')
        playable_cards = DoudizhuRule(hand).playable_cards('pair_chain_5')
        for e in in_cards_5:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_5)

        in_cards_6 = ('334455667788','445566778899', '5566778899TT', 
            '66778899TTJJ', '778899TTJJQQ', '8899TTJJQQKK', '99TTJJQQKKAA')
        playable_cards = DoudizhuRule(hand).playable_cards('pair_chain_6')
        for e in in_cards_6:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_6)

        in_cards_7 = ('33445566778899','445566778899TT', '5566778899TTJJ', 
            '66778899TTJJQQ', '778899TTJJQQKK', '8899TTJJQQKKAA')
        playable_cards = DoudizhuRule(hand).playable_cards('pair_chain_7')
        for e in in_cards_7:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_7)

        in_cards_8 = ('33445566778899TT','445566778899TTJJ', '5566778899TTJJQQ', 
            '66778899TTJJQQKK', '778899TTJJQQKKAA')
        playable_cards = DoudizhuRule(hand).playable_cards('pair_chain_8')
        for e in in_cards_8:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_8)

        in_cards_9 = ('33445566778899TTJJ','445566778899TTJJQQ', '5566778899TTJJQQKK', 
            '66778899TTJJQQKKAA')
        playable_cards = DoudizhuRule(hand).playable_cards('pair_chain_9')
        for e in in_cards_9:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_9)

        in_cards_10 = ('33445566778899TTJJQQ','445566778899TTJJQQKK', 
            '5566778899TTJJQQKKAA')
        playable_cards = DoudizhuRule(hand).playable_cards('pair_chain_10')
        for e in in_cards_10:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_10)

    def test_DoudizhuRule_get_trio_chain(self):
        hand =  '333444455556667778889999TTTJJJQQQKKKAAA222BR'

        #trio_chain_2 -- #trio_chain_6
        in_cards_2 = ('333444', '444555', '555666', '666777', '777888', 
        '888999', '999TTT', 'TTTJJJ', 'JJJQQQ', 'QQQKKK', 'KKKAAA')
        playable_cards = DoudizhuRule(hand).playable_cards('trio_chain_2')
        for e in in_cards_2:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_2)

        in_cards_3 = ('333444555', '444555666', '555666777', '666777888',
        '777888999', '888999TTT', '999TTTJJJ', 'TTTJJJQQQ', 'JJJQQQKKK', 
        'QQQKKKAAA')
        playable_cards = DoudizhuRule(hand).playable_cards('trio_chain_3')
        for e in in_cards_3:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_3)

        in_cards_4 = ('333444555666', '444555666777', '555666777888', 
        '666777888999', '777888999TTT', '888999TTTJJJ', '999TTTJJJQQQ', 
        'TTTJJJQQQKKK', 'JJJQQQKKKAAA')
        playable_cards = DoudizhuRule(hand).playable_cards('trio_chain_4')
        for e in in_cards_4:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_4)

        in_cards_5 = ('333444555666777', '444555666777888', '555666777888999', 
        '666777888999TTT', '777888999TTTJJJ', '888999TTTJJJQQQ', '999TTTJJJQQQKKK', 
        'TTTJJJQQQKKKAAA')
        playable_cards = DoudizhuRule(hand).playable_cards('trio_chain_5')
        for e in in_cards_5:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_5)

        in_cards_6 = ('333444555666777888', '444555666777888999', '555666777888999TTT', 
        '666777888999TTTJJJ', '777888999TTTJJJQQQ', '888999TTTJJJQQQKKK', 
        '999TTTJJJQQQKKKAAA')
        playable_cards = DoudizhuRule(hand).playable_cards('trio_chain_6')
        for e in in_cards_6:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards_6)

    def test_DoudizhuRule_get_trio_solo(self):
        hand =  '34455677778889T2222BR'

        #trio_solo
        in_cards = ('3777', '4777', '5777', '6777', '7778', 
            '7779', '777T', '7772', '777B', '777R',
            '3222', '4222', '5222', '6222', '7222', 
            '8222', '9222', 'T222', '222B', '222R',
            '3888', '4888', '5888', '6888', '7888', 
            '8889', '888T', '8882', '888B', '888R')
        playable_cards = DoudizhuRule(hand).playable_cards('trio_solo')
        for e in in_cards:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards)

    def test_DoudizhuRule_get_trio_pair(self):
        hand =  '34455677778889T2222BR'

        #trio_pair
        in_cards = ('44777', '55777', '77788', '77722',
            '44222', '55222', '77222', '88222',
            '44888', '55888', '77888', '88822')
        playable_cards = DoudizhuRule(hand).playable_cards('trio_pair')
        for e in in_cards:
            self.assertIn(e, playable_cards)
        for e in playable_cards:
            self.assertIn(e, in_cards)

    def test_DoudizhuRule_get_trio_solo_chain(self):
        hand =  '34556677778888999TTTTJJJJQQQQKA2BR'
        #trio_solo_chain_2 -- trio_solo_chain_5
        in_cards_2 = ('34777888', '3777888T', '66777888')
        not_in_cards_2 = ('37777888', )
        playable_cards = DoudizhuRule(hand).playable_cards('trio_solo_chain_2')
        for e in in_cards_2:
            self.assertIn(e, playable_cards)
        for e in not_in_cards_2:
            self.assertNotIn(e, playable_cards)

        in_cards_4 = ('3456777888999TTT', )
        not_in_cards_4 = ('6777888999TTTJJJ', )
        playable_cards = DoudizhuRule(hand).playable_cards('trio_solo_chain_4')
        for e in in_cards_4:
            self.assertIn(e, playable_cards)
        for e in not_in_cards_4:
            self.assertNotIn(e, playable_cards)

        in_cards_5 = ('3456777888999TTTJJJQ', )
        not_in_cards_5 = ('777888999TTTJJJQK2BR', '3456777888999TTTJJJJ')
        playable_cards = DoudizhuRule(hand).playable_cards('trio_solo_chain_5')
        for e in in_cards_5:
            self.assertIn(e, playable_cards)
        for e in not_in_cards_5:
            self.assertNotIn(e, playable_cards)

    def test_DoudizhuRule_get_trio_pair_chain(self):
        hand =  '34556677778888999TTTTJJJJQQQQKA2BR'

        #trio_pair_chain_2 -- #trio_pair_chain_4
        in_cards_2 = ('5566777888', '55777888TT')
        not_in_cards_2 = ('777888QQQQ', )
        playable_cards = DoudizhuRule(hand).playable_cards('trio_pair_chain_2')
        for e in in_cards_2:
            self.assertIn(e, playable_cards)
        for e in not_in_cards_2:
            self.assertNotIn(e, playable_cards)

    def test_DoudizhuRule_get_four_two_solo(self):
        hand =  '34556677778888999TTTTJJJJQQQQKA2BR'

        #four_two_solo, #four_two_pair
        in_cards = ('357777', '557777', '567777', '777788')
        not_in_cards = ()
        playable_cards = DoudizhuRule(hand).playable_cards('four_two_solo')
        for e in in_cards:
            self.assertIn(e, playable_cards)
        for e in not_in_cards:
            self.assertNotIn(e, playable_cards)

    def test_DoudizhuRule_get_four_two_pair(self):
        hand =  '34556677778888999TTTTJJJJQQQQKA2BR'

        #four_two_solo, #four_two_pair
        in_cards = ('55667777', '66777799', '557777TT', '55777788')
        not_in_cards = ('77778888', )
        playable_cards = DoudizhuRule(hand).playable_cards('four_two_pair')
        for e in in_cards:
            self.assertIn(e, playable_cards)
        for e in not_in_cards:
            self.assertNotIn(e, playable_cards)
        

    def test_DoudizhuRule_playable_cards(self):
        playable_cards = list(DoudizhuRule('3333444455556666777788889999TTTTJJJJQQQQKKKKAAAA2222BR').playable_cards())
        all_cards_list = CARD_TYPE[1]
        for c in playable_cards:
            # if (c not in all_cards_list):
            #     print(c)
            self.assertIn(c, all_cards_list)
        for c in all_cards_list:
            # if (c not in playable_cards):
            #     print('\t' + c)
            self.assertIn(c, playable_cards)
        self.assertEqual(len(playable_cards), len(all_cards_list))

if __name__ == '__main__':
    unittest.main()
