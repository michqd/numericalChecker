class NFA:
    def __init__(self, Q, Sigma, Delta, S, F):
        self.Q = Q  # Set of states
        self.Sigma = Sigma  # Alphabet
        self.Delta = Delta  # Transition function as a dictionary
        self.S = S  # Set of Start states
        self.F = F  # Set of accept states

    def __repr__(self):
        return f"DFA ({self.Q}, \n\t{self.Sigma}, \n\t{self.Delta}, \n\t{self.S}, \n\t{self.F})"

    def do_delta(self, q, x):
        try:
            return self.Delta[(q, x)]
        except KeyError:
            return set({})

    def run(self, w):
        P = self.S
        while w != "":
            Pnew = set({})
            for q in P:
                Pnew = Pnew | self.do_delta(q, w[0])
            w = w[1:]
            P = Pnew
        return (P & self.F) != set({})


digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
octa_digits = {'0', '1', '2', '3', '4', '5', '6', '7'}
alphabet = {'+', '-','_','.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F'}
hex_alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F'}
octa_letters = {'o', 'O'}
binaryNums = {'0', '1'}
signsNums = {'+', '-'}
float_alphabet = {'e', 'E'}
empty_set = { }


# ACCEPTS: - + 0123456789_
# NFA for Decinteger
N0 = NFA({0, 1, 2, 3, 4, 5, 6},
         alphabet,

         {(0, '-'): {1}} | {(0, digit): {1} for digit in digits - {'0'}} | 
         {(1, digit): {1} for digit in digits} | {(1, '_'): {2}} |
         {(2, digit): {3, 1} for digit in digits} | 
         {(3, digit): {3, 1} for digit in digits} | {(0, '0'): {4}} | 
         {(4, '_'): {5}} | 
         {(5, '0'): {6, 4}} | 
         {(6, '0'): {6, 4}}, 
         
         {0},

         {1, 3, 6})

# ACCEPTS: 0x | 0X (0123456789abcdefABCDEF_)
# NFA for hexinteger
N1 = NFA({0, 1, 2, 3, 4, 5},
         alphabet,

         {(0, '0'): {1}} |
         {(1, 'x'): {2}} | {(1, 'X'): {2}} |
         {(2, digit): {3} for digit in digits} | {(2, alpha): {3} for alpha in hex_alphabet} |
         {(3, digit): {3} for digit in digits} | {(3, alpha): {3} for alpha in hex_alphabet} |
         {(3, '_'): {4}} | 
         {(4, digit): {3} for digit in digits} | {(4, alpha): {3} for alpha in hex_alphabet},

         {0},

         {3})

# ACCEPTS: 0o | 0O (01234567_)
# NFA for Octinteger
N2 = NFA({0, 1, 2, 3, 4},
         alphabet,

         {(0,'0'): {1}} | 
         {(1, letter): {2} for letter in octa_letters} | 
         {(2, num): {2, 4} for num in octa_digits} | {(2, '_'): {3}} |
         {(3, num): {4, 2} for num in octa_digits} | 
         {(4, num): {4, 2} for num in octa_digits},

         {0},

         {4})

# ACCEPTS: +- (0123456789._eE)
# NFA for float integer
N3 = NFA({0, 1, 2},
         alphabet,
        
         {(0, sign): {1} for sign in signsNums} | {(0, ''): {1}} |
         {(1, digit): {2} for digit in digits} | {(1, '.'): {13}} | 
         {(2, digit): {2} for digit in digits} | {(2, alpha): {7} for alpha in float_alphabet} | {(2, '.'): {4}} | {(2, '_'): {3}}|
         {(3, digit): {3} for digit in digits} | {(3, alpha): {7} for alpha in float_alphabet} | {(3, '.'): {5}} |
         {(4, digit): {4} for digit in digits} | {(4, alpha): {7} for alpha in float_alphabet} | {(4, '_'): {5}} |
         {(5, digit): {5} for digit in digits} | {(5, alpha): {7} for alpha in float_alphabet} | {(5, '_'): {6}}| 
         {(6, digit): {6} for digit in digits} | {(6, alpha): {7} for alpha in float_alphabet} |
         {(7, ''): {8}} | {(7, sign): {8} for sign in signsNums} |
         {(8, digit): {10} for digit in digits} | {(8, '_'): {9}} |
         {(9, digit): {10} for digit in digits} |
         {(10, digit): {10} for digit in digits} | {(10, '_'): {11}} | 
         {(11, digit): {10} for digit in digits} | 
         {(12, digit): {10} for digit in digits} |
         {(13, digit): {10} for digit in digits} | {(13, '_'): {12}},
        
         {0},

         {4, 5, 6, 10})


if __name__ == "__main__":
    input_string = input("Please enter valid integer: ")

    decint = N0.run(input_string)
    hexint = N1.run(input_string)
    octint = N2.run(input_string)
    floatint = N3.run(input_string)

    if decint:
        print("True. This is a valid decinteger.")
        
    elif hexint:
        print("True. This is a valid hexinteger.")
        
    elif octint:
        print("True. This is a valid octinteger.")

    elif floatint:
        print("True. This is a valid float integer.")

    else:
        print("False. This is not valid.")
