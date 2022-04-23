#
# This file is the interface between the stores and the database
#

import sqlite3
from sqlite3 import Connection

from datetime import datetime
from typing import List

from backend.main.objects.voter import Voter, VoterStatus
from backend.main.objects.candidate import Candidate


class VotingStore:
    """
    A singleton class that encapsulates the interface between the stores and the databases.

    To use, simply do:

    >>> voting_store = VotingStore.get_instance()   # this will create the stores, if they haven't been created
    >>> voting_store.add_candidate(...)  # now, you can call methods that you need here
    """

    voting_store_instance = None

    @staticmethod
    def get_instance():
        if not VotingStore.voting_store_instance:
            VotingStore.voting_store_instance = VotingStore()

        return VotingStore.voting_store_instance

    @staticmethod
    def refresh_instance():
        """
        DO NOT MODIFY THIS METHOD
        Only to be used for testing. This will only work if the sqlite connection is :memory:
        """
        if VotingStore.voting_store_instance:
            VotingStore.voting_store_instance.connection.close()
        VotingStore.voting_store_instance = VotingStore()

    def __init__(self):
        """
        DO NOT MODIFY THIS METHOD
        DO NOT call this method directly - instead use the VotingStore.get_instance method above.
        """
        self.connection = VotingStore._get_sqlite_connection()
        self.create_tables()

    @staticmethod
    def _get_sqlite_connection() -> Connection:
        """
        DO NOT MODIFY THIS METHOD
        """
        return sqlite3.connect(":memory:", check_same_thread=False)

    def create_tables(self):
        """
        Creates Tables
        """
        self.connection.execute(
            """CREATE TABLE candidates (candidate_id integer primary key autoincrement, name text)""")
        self.connection.execute(
            """
            CREATE TABLE voter(
                voter_id integer primary key autoincrement,
                first_name text,
                last_name text,
                national_id text,
                status text null,
                creation text,
                deleted boolean default false
            )
            """
        )
        self.connection.commit()

    def add_candidate(self, candidate_name: str):
        """
        Adds a candidate into the candidate table, overwriting an existing entry if one exists
        """
        self.connection.execute("""INSERT INTO candidates (name) VALUES (?)""", (candidate_name, ))
        self.connection.commit()

    def get_candidate(self, candidate_id: str) -> Candidate:
        """
        Returns the candidate specified, if that candidate is registered. Otherwise returns None.
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM candidates WHERE candidate_id=?""", (candidate_id,))
        candidate_row = cursor.fetchone()
        candidate = Candidate(candidate_id, candidate_row[1]) if candidate_row else None
        self.connection.commit()

        return candidate

    def get_all_candidates(self) -> List[Candidate]:
        """
        Gets ALL the candidates from the database
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM candidates""")
        all_candidate_rows = cursor.fetchall()
        all_candidates = [Candidate(str(candidate_row[0]), candidate_row[1]) for candidate_row in all_candidate_rows]
        self.connection.commit()

        return all_candidates
    
    # NEW METHOD
    def add_voter(self, voter: Voter) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT count(*) FROM voter WHERE national_id=?""", (voter.national_id,))
            status_voter = cursor.fetchone()
            count_voter = int(status_voter[0]) if status_voter else 0

            if count_voter == 0:
                today = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                statusVoted = VoterStatus.REGISTERED_NOT_VOTED.value
                self.connection.execute("""
                    INSERT INTO voter (
                        first_name, 
                        last_name, 
                        national_id, 
                        status, 
                        creation)
                    values (?,?,?, ?, ?)
                """, (voter.first_name , 
                    voter.last_name, 
                    voter.national_id, 
                    str(statusVoted), 
                    today))
                self.connection.commit()
                return True
            else: 
                return False
        except Exception as e:
            raise e 

    def get_voter(self, national_id:str) -> Voter:
        cursor = self.connection.cursor()
        cursor.execute("""SELECT first_name, last_name, national_id FROM voter WHERE national_id=?""", (national_id,))
        voter_row = cursor.fetchone()
        voter = Voter(voter_row[0], voter_row[1], voter_row[2]) if voter_row else None
        self.connection.commit()

        return voter

    def get_status_voter(self, national_id: str) -> str:
        cursor = self.connection.cursor()
        cursor.execute("""SELECT status FROM voter WHERE national_id=?""", (national_id,))
        status_voter = cursor.fetchone()
        status_voter = status_voter[0] if status_voter else None
        self.connection.commit()

        return status_voter

    def delete_voter(self, national_id: str) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT count(*) FROM voter WHERE national_id=?""", (national_id,))
            status_voter = cursor.fetchone()
            count_voter = int(status_voter[0]) if status_voter else 0

            if count_voter > 0:
                self.connection.execute("""
                    DELETE FROM voter 
                    WHERE national_id=?
                """, (national_id,))
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            raise e


    # TODO: If you create more tables in the create_tables method, feel free to add more methods here to make accessing
    #       data from those tables easier. See get_all_candidates, get_candidates and add_candidate for examples of how
    #       to do this.

