'''
Matt Gurgiolo
Prof Bender
CS151 SP22

lsystem.py
'''


class Lsystem:

    def __init__(self, filename=None):
        '''L-system class constructor

        Parameters:
        -----------
        filename: str. Filename of the L-system text file with the base string and 1+ replacement rules
        '''
        # Create an instance variable for the base string
        # (initialize as the empty string)
        self.basestring = ""

        # Create an instance variable for your replacement rules
        # (initialize as an empty list)
        self.rules = []
        # Check if filename passed in (i.e. parameter is not None)
        # If so, read in the L-system from the file called filename. Do this by calling the read method: self.read(filename) (you will implement this shortly)
        if filename is not None:
            self.read(filename)
        
    def read(self, filename):
        '''Reads the L-system base string and 1+ rules from a text file. Stores the data in the
        instance variables in the constructor in the format:

        base string: str.
        e.g. `'F-F-F-F'`
        replacement rules: list of 2 element sublists.
        e.g. `[['F', 'FF-F+F-F-FF']]` for one rule

        Parameters:
        -----------
        filename: str. Filename of the L-system text file with the base string and 1+ replacement
        rules
        '''
        # Open the file called filename
        # Read in the file line-by-line.
        # For each line, split it into a 2 item list.
        #   If the first list item is the string 'base', set the L-system base string
        #   to the second item in the list.
        #   If the first list item is the string 'rule', add a rule to your replacement
        #   rules consisting of the find and replace strings
        #   (2nd and 3rd items in the list).
        #   Remember: We add a rule in list format: [find str, replace str]

        # Close the file
        if filename is not None:
            file = open(filename)
            lines = file.readlines()
            for line in lines:
                linesplit = line.split()
                if linesplit[0] == 'base':
                    self.setBase(linesplit[1])
                if linesplit[0] == 'rule':
                    self.addRule(linesplit[1:])
            file.close()

    def getBase(self):
        return self.basestring

    def setBase(self, newBase):
        self.basestring = newBase
    
    def getRule(self, ruleIdx):
        return self.rules[ruleIdx]

    def addRule(self, newRule: list):
        self.rules.append(newRule)
    
    def numRules(self):
        return len(self.rules)
    
    def replace(self, currString):
        '''Applies the full set of replacement rules to current 'base' L-system string `currString`.

        Overall strategy:
        - Scan the L-system string left to right, char by char
        - Apply AT MOST ONE replacement rule to a matching character.
            Example: If the current char is 'F' and that matches a rule's find string 'F', apply
            that rule then move onto the next character in the L-system string (don't try to match
            more rules to the current char).
        - If no rule matches a rule find string, we just add the char as-is to the new string.

        Parameters:
        -----------
        currString: str. The current L-system base string.

        Returns:
        -----------
        newString: str. The base string `currString` with replacement rules applied to it.
        '''
        newString = ''

        for char in currString:
            found = False
            for rule in self.rules:
                if char == rule[0]:
                    newString += rule[1]
                    found = True
                    break
            if not found:
                newString += char

        return newString

    def buildString(self, n):
        '''Starting with the base string, apply the L-system replacement rules for `n` iterations.
        You should NOT change your base string instance variable here!

        Parameters:
        -----------
        n: int. Number of times you go through the L-system string to apply the replacement rules.

        Returns:
        -----------
        str. The L-system string after apply the replacement rules `n` times.
        '''
        newerString = ''
        newString = ''
        if n < 1:
            newString = self.basestring
        else:
            newString = self.replace(self.basestring)
            for i in range(n-1):
                newerString = self.replace(newString)
                newString = newerString
        
        return newString