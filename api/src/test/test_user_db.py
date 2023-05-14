"""
test_user_db.py
By: Zack Bamford

Tests for the user database commands
"""

from unittest import TestCase

import api.src.main.db.generic_db as generic_db

from api.src.main.db.user_db import UserCommands, User


class TestUserCommands(TestCase):
    """
    Test the user database commands
    """

    uc: UserCommands = UserCommands(generic_db.db_obj)

    VALID_USER = User(ID="x", username="x", email="x", password="x")
    VALID_USER_2 = User(ID="", username="", email="", password="")

    VALID_USERS = [VALID_USER, VALID_USER_2]

    UPDATE_USER = User(ID="a", username="b", email="c", password="d")

    INVALID_USER = User(ID=" ", username="  ", email="   ", password="    ")

    def test_create_user(self):
        """
        Test creating a job

        :return: None
        """

        for user in self.VALID_USERS:
            # add to db
            created_job = self.uc.create_user(user.username, user.email, user.password)
            self.assertTrue(created_job.equals_no_id(user))

            # check db
            retrieved_job = self.uc.retrieve_user(created_job.ID)
            self.assertTrue(retrieved_job.equals_no_id(user))

    def test_retrieve_user(self):
        """
        Test retrieving a user

        :return:
        """
        for user in self.VALID_USERS:
            # add to db
            created_job = self.uc.create_user(user.username, user.email, user.password)

            # check db
            retrieved_job = self.uc.retrieve_user(created_job.ID)
            self.assertIsNotNone(retrieved_job)
            self.assertTrue(retrieved_job.equals_no_id(user))

    def test_retrieve_invalid_user(self):
        """
        Test receiving an invalid user

        :return:
        """
        retrieved_job = self.uc.retrieve_user(self.INVALID_USER.ID)
        self.assertIsNone(retrieved_job)

    def test_modify_user(self):
        """
        Test modifying a valid user

        :return:
        """

        # create user
        created_job = self.uc.create_user(self.VALID_USER.username, self.VALID_USER.email, self.VALID_USER.password)

        # modify
        modified_job = self.uc.modify_user(created_job.ID, self.UPDATE_USER.username, self.UPDATE_USER.email,
                                           self.UPDATE_USER.password)

        # check
        self.assertIsNotNone(modified_job)
        self.assertTrue(modified_job.equals_no_id(self.UPDATE_USER))

    def test_modify_invalid_user(self):
        """
        Test modifying an invalid user

        :return:
        """

        # create user
        self.uc.create_user(self.VALID_USER.username, self.VALID_USER.email, self.VALID_USER.password)

        # modify
        modified_job = self.uc.modify_user(self.INVALID_USER.ID, self.UPDATE_USER.username, self.UPDATE_USER.email,
                                           self.UPDATE_USER.password)

        # check
        self.assertIsNone(modified_job)

    def test_delete_user(self):
        """
        Test deleting a valid user

        :return:
        """

        # create user
        created_job = self.uc.create_user(self.VALID_USER.username, self.VALID_USER.email, self.VALID_USER.password)

        # delete and check
        self.assertTrue(self.uc.delete_user(created_job.ID))

    def test_delete_invalid_user(self):
        """
        Test deleting an invalid user

        :return:
        """

        # try to delete and check
        self.assertFalse(self.uc.delete_user(self.INVALID_USER.ID))
