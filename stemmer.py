class PorterStemmer:
    def vc(self, word: str):
        word = word.lower()
        vc = ""
        for letter in word:
            if letter in "aeiouy":
                vc += "V"
            else:
                vc += "C"
        return vc

    def measure(self, word: str):
        word = word.lower()
        vc = self.vc(word)
        return vc.count("VC")

    def contain_vowel_check(self, word: str):
        word = word.lower()
        word_vc = self.vc(word)
        if "V" in word_vc:
            if word_vc.find("V") == word_vc.rfind("V") == (len(word_vc)-1):
                return False
            return True
        else:
            return False


    def cc_check(self, word: str):
        word = word.lower()
        if self.vc(word).endswith("CC"):
            if word[-1] == word[-2]:
                return True
        return False

    def star_check(self, word: str):
        word = word.lower()
        if self.vc(word).endswith("CVC"):
            if not(word[-1] in "wxy"):
                return True
        return False

    def step_1a(self, word: str):
        word = word.lower()

        if word.endswith("sses"):
           word = word[:len(word)-2]

        elif word.endswith("ies"):
            word = word[:len(word)-2]

        elif word.endswith("ss"):
            word = word

        elif word.endswith("s"):
            word = word[:len(word)-1]

        return word

    def step_1b_helper(self, word: str):
        word = word.lower()
        if word.endswith("at"):
            word = word + "e"

        elif word.endswith("bl"):
            word = word + "e"

        elif (self.cc_check(word) and not((word.endswith("l")or(word.endswith("s")or(word.endswith("z")))))):
            word = word[:len(word)-1]

        elif self.measure(word) == 1 and self.star_check(word):
            word = word + "e"

        return word

    def step_1b(self, word: str):
        word = word.lower()
        need_to_clean = False

        if self.measure(word) > 1:
            if word.endswith("eed"):
               word = word[:len(word)-1]

            elif self.contain_vowel_check(word):
                if word.endswith("ed"):
                    word = word[:len(word)-2]
                    need_to_clean = True

                elif word.endswith("ing"):
                    word = word[:len(word)-3]
                    need_to_clean = True

        if need_to_clean:
            word = self.step_1b_helper(word)
        return word

    def step_1c(self, word: str):
        word = word.lower()
        if self.contain_vowel_check(word):
            if word.endswith("y"):
                word = word[:len(word)-1]
                word = word + "i"
        return word

    def step_2(self, word: str):
        word = word.lower()

        if self.measure(word) > 0:
            if word.endswith("ational"):
                    word = word[:len(word)-5]
                    word = word + "e"

            elif word.endswith("ization"):
                    word = word[:len(word)-5]
                    word = word + "e"
            elif word.endswith("biliti"):
                    word = word[:len(word)-5]
                    word = word + "le"

        return word

    def step_3(self, word: str):
        word = word.lower()

        if self.measure(word) > 0:
            if word.endswith("icate"):
                    word = word[:len(word)-3]
            elif word.endswith("ful"):
                    word = word[:len(word)-3]
            elif word.endswith("ness"):
                    word = word[:len(word)-4]

        return word

    def step_4(self, word: str):
        word = word.lower()

        if self.measure(word) > 0:
            if word.endswith("ance"):
                    word = word[:len(word)-4]

            elif word.endswith("ent"):
                    word = word[:len(word)-3]


            elif word.endswith("ive"):
                    word = word[:len(word)-3]

        return word

    def step_5a(self, word: str):
        word = word.lower()

        if self.measure(word) > 1:
            if word.endswith("e"):
                    word = word[:len(word)-1]
            elif ((self.measure(word))and(not(self.star_check(word)))) ==1 and word.endswith("ness") :
                word = word[:len(word)-4]

        return word

    def step_5b(self, word: str):
        word = word.lower()
        if self.measure(word) > 1 and self.cc_check(word) and word.endswith("l"):
            word = word[:len(word)-1]
        return word


    def stem(self, word:str):
        word = word.lower()
        word = self.step_1a(word)
        word = self.step_1b(word)
        word = self.step_1b_helper(word)
        word = self.step_1c(word)
        word = self.step_2(word)
        word = self.step_3(word)
        word = self.step_4(word)
        word = self.step_5a(word)
        word = self.step_5b(word)
        return word
