import math

class rayshnakht_v1:
    def __init__(self):
        # The AirNaks
        self.AirNak_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.AirNak_2 = [11, 22, 33, 44, 55, 66, 77, 88, 99]
        self.AirNak_3 = [111, 222, 333, 444, 555, 666, 777, 888, 999]
        self.AirNak_4 = [1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999]
        self.AirNak_5 = [11111, 22222, 33333, 44444, 55555, 66666, 77777, 88888, 99999]
        self.AirNak_6 = [111111, 222222, 333333, 444444, 555555, 666666, 777777, 888888, 999999]
        self.AirNak_7 = [1111111, 2222222, 3333333, 4444444, 5555555, 6666666, 7777777, 8888888, 9999999]
        self.AirNak_8 = [11111111, 22222222, 33333333, 44444444, 55555555, 66666666, 77777777, 88888888, 99999999]
        self.AirNak_9 = [111111111, 222222222, 333333333, 444444444, 555555555, 666666666, 777777777, 888888888, 999999999]
        
        # The Positions
        self.P1 = {'A': 11, 'B': 22, 'C': 33, 'D': 44, 'E': 55, 'F': 66, 'G': 77, 'H': 88, 'I': 99, 
                   'J': 111, 'K': 222, 'L': 222, 'M': 333, 'N': 444, 'O': 555, 'P': 666, 'Q': 777, 
                   'R': 888, 'S': 999, 'T': 1111, 'U': 2222, 'V': 3333, 'W': 4444, 'X': 5555, 'Y': 6666, 'Z': 7777}
        
        self.P2 = {'a': 12, 'b': 23, 'c': 34, 'd': 45, 'e': 56, 'f': 67, 'g': 78, 'h': 89, 'i': 100, 
                   'j': 112, 'k': 223, 'l': 223, 'm': 334, 'n': 445, 'o': 556, 'p': 667, 'q': 778, 
                   'r': 889, 's': 1000, 't': 1112, 'u': 2223, 'v': 3334, 'w': 4445, 'x': 5556, 'y': 6667, 'z': 7778}
        
        self.P3 = {'0': 13, '1': 24, '2': 35, '3': 46, '4': 57, '5': 68, '6': 79, '7': 90, '8': 101, '9': 1113}
        
        self.P4 = {'@': 14, '#': 25, '$': 36, '%': 47, '^': 58, '&': 69, '*': 80, '(': 91, ')': 102, 
                   '-': 114, '_': 225, '=': 336, '+': 447, '[': 558, ']': 669, '{': 780, '}': 891, 
                   '|': 1002, '\\': 1114, ':': 2225, ';': 3336, '"': 4447, "'": 5558, '<': 6669, '>': 7779}

    def swap_input(self, input_string):
        swapped_values = {
            'P1': [],
            'P2': [],
            'P3': [],
            'P4': []
        }

        for char in input_string:
            if char in self.P1:
                swapped_values['P1'].append(self.P1[char])
            elif char in self.P2:
                swapped_values['P2'].append(self.P2[char])
            elif char in self.P3:
                swapped_values['P3'].append(self.P3[char])
            elif char in self.P4:
                swapped_values['P4'].append(self.P4[char])
            # If character is not in any position, we'll ignore it

        return swapped_values
    
    def get_next_airnak(self, current_airnak):
        airnaks = [self.AirNak_1, self.AirNak_2, self.AirNak_3, self.AirNak_4, 
                   self.AirNak_5, self.AirNak_6, self.AirNak_7, self.AirNak_8, self.AirNak_9]
        if not current_airnak:
            return self.AirNak_1
        try:
            current_index = airnaks.index(current_airnak)
            return airnaks[min(current_index + 1, len(airnaks) - 1)]
        except ValueError:
            return self.AirNak_1

    def repair_positions(self, swapped_values):
        all_values = [value for position in swapped_values.values() for value in position]
        max_value = max(all_values) if all_values else 0
        
        current_airnak = next((airnak for airnak in [self.AirNak_1, self.AirNak_2, self.AirNak_3, self.AirNak_4, 
                               self.AirNak_5, self.AirNak_6, self.AirNak_7, self.AirNak_8, self.AirNak_9] 
                               if max_value <= airnak[-1]), self.AirNak_1)
        current_airnak = self.get_next_airnak(current_airnak)

        max_length = max(len(values) for values in swapped_values.values())
        target_length = ((max_length - 1) // 9 + 1) * 9

        repaired_values = {}
        airnak_values = []
        while len(airnak_values) < target_length:
            airnak_values.extend(current_airnak)
            if len(airnak_values) < target_length:
                current_airnak = self.get_next_airnak(current_airnak)

        for position, values in swapped_values.items():
            repaired_values[position] = values.copy()
            repaired_values[position].extend(airnak_values[len(values):target_length])

        return repaired_values

    def generate_dualities(self, repaired_positions):
        dualities = []
        max_length = max(len(values) for values in repaired_positions.values())
        
        for i in range(max_length - 1):
            d = {}
            for j in range(1, 5):
                position_key = f'P{j}'
                if i < len(repaired_positions[position_key]) - 1:
                    d[position_key] = (repaired_positions[position_key][i], repaired_positions[position_key][i+1])
            if d:
                dualities.append(d)
        
        return dualities
    
    def generate_sub_rayshnakht_v1(self, dualities):
        sub_rayshnakhts = []
        pi = 3.14  # As specified in your instructions

        for duality in dualities:
            sub_rayshnakht = []
            for position, values in duality.items():
                radius = (values[0] + values[1]) * 10
                area = round(pi * (radius ** 2))  # Rounding to the nearest integer
                sub_rayshnakht.append(int(area))  # Convert to integer to remove scientific notation
            sub_rayshnakhts.append(sub_rayshnakht)

        return sub_rayshnakhts
    
    def rayshnakht_v1(self, input_string):
        swapped = self.swap_input(input_string)
        repaired = self.repair_positions(swapped)
        dualities = self.generate_dualities(repaired)
        sub_rayshnakhts = self.generate_sub_rayshnakht_v1(dualities)
        
        # Combine all sub_raynakhts into one string
        hash_string = ''
        for sub_rayshnakht in sub_rayshnakhts:
            hash_string += ''.join(str(value) for value in sub_rayshnakht)
        
        return hash_string


class rayshnakht_mtstr:
    def __init__(self, string1, string2, mode):
        self.string1 = string1
        self.string2 = string2
        self.mode = mode

    def match_strings(self):
        if len(self.string1) != len(self.string2):
            if self.mode == 1:
                return False
            elif self.mode == 0:
                return f"STR_NOT_MATCHED_F(len1={len(self.string1)}, len2={len(self.string2)})"

        for char1, char2 in zip(self.string1, self.string2):
            if char1 != char2:
                if self.mode == 1:
                    return False
                elif self.mode == 0:
                    return f"STR_NOT_MATCHED_F({char1},{char2})"

        if self.mode == 1:
            return True
        elif self.mode == 0:
            return "STR_MATCHED_SEC"