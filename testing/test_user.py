"""
The MIT License (MIT)

Copyright (c) 2020 Skelmis

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import logging
import sys
import unittest


from AntiSpam import User, Message
from AntiSpam.static import Static
from AntiSpam.Exceptions import DuplicateObject, ObjectMismatch


class TestUser(unittest.TestCase):
    """
    Used to test the user object
    """

    def setUp(self):
        """
        Simply setup our User obj before usage
        """
        self.user = User(
            None, 0, 3, Static.DEFAULTS, logger=logging.getLogger(__name__)
        )
        self.user.messages = Message(0, "Hello world", 0, 2, 3)
        self.user.messages = Message(1, "Foo Bar", 0, 2, 3)

    def test_botAssignment(self):
        # Given we don't want to populate an entire bot,
        # lets just check its assigned correctly
        self.assertIsNone(self.user.bot)

    def test_intAssignment(self):
        self.assertIsInstance(self.user.id, int)
        self.assertIsInstance(self.user.guildId, int)

    def test_listAssignment(self):
        self.assertIsInstance(self.user.messages, list)

    def test_dictAssignment(self):
        self.assertIsInstance(self.user.options, dict)

    def test_valueAssignment(self):
        self.assertEqual(self.user.id, 0)
        self.assertEqual(self.user.guildId, 3)
        self.assertEqual(self.user.options, Static.DEFAULTS)

        self.user.id = 10
        self.user.guildId = 10

        self.assertEqual(self.user.id, 10)
        self.assertEqual(self.user.guildId, 10)

    def test_messageAssignment(self):
        self.assertEqual(len(self.user.messages), 2)
        self.user.messages = Message(3, "Test", 0, 2, 3)
        self.assertEqual(len(self.user.messages), 3)

    def test_messageRaises(self):
        with self.assertRaises(ValueError):
            self.user.messages = 1

    def test_messageRaisesDuplicate(self):
        with self.assertRaises(DuplicateObject):
            self.user.messages = Message(1, "Testing", 0, 2, 3)

    def test_messageRaisesMismatch(self):
        with self.assertRaises(ObjectMismatch):
            self.user.messages = Message(20, "Testing", 20, 20, 20)

    def test_repr(self):
        self.assertEqual(
            repr(self.user),
            (
                f"'{self.user.__class__.__name__} object. User id: {self.user.id}, Guild id: {self.user.guildId}, "
                f"Len Stored Messages {len(self.user.messages)}'"
            ),
        )

    def test_str(self):
        self.assertEqual(
            str(self.user), f"{self.user.__class__.__name__} object for {self.user.id}."
        )

    def test_eqEqual(self):
        obj = User(None, 0, 3, Static.DEFAULTS, logger=logging.getLogger(__name__))
        self.assertTrue(self.user == obj)

    def test_eqNotEqual(self):
        obj = User(None, 2, 2, Static.DEFAULTS, logger=logging.getLogger(__name__))
        self.assertFalse(self.user == obj)

    def test_duplicateCounter(self):
        self.assertNotEqual(
            self.user.duplicateCounter, self.user.GetCorrectDuplicateCount()
        )

        self.assertEqual(
            self.user.duplicateCounter - 1, self.user.GetCorrectDuplicateCount()
        )


if __name__ == "__main__":
    unittest.main()
