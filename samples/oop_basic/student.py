#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Student:
    """
    Represents a student with a name and score.
    """

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        """
        Prints the student's name and score.
        """
        print(f'{self.name}: {self.score}')

    def get_grade(self):
        """
        Returns the grade based on the student's score.
        """
        if self.score >= 90:
            return 'A'
        elif self.score >= 60:
            return 'B'
        else:
            return 'C'

bart = Student('Bart Simpson', 59)
lisa = Student('Lisa Simpson', 87)

print('bart.name:', bart.name)
print('bart.score:', bart.score)
bart.print_score()

print('Grade of Bart:', bart.get_grade())
print('Grade of Lisa:', lisa.get_grade())
