#
# This file is the REST API for our frontend to get data from. Please DO NOT modify anything in the file other than the
# populate_database() method below.
#
# To run the backend server locally, please run the following from the /backend directory
#
# $ export FLASK_APP=main/api/backend_rest_api.py
# $ flask run
#

from flask import request
import backend.main.api.balloting as balloting
import backend.main.api.registry as registry
from backend.main.objects.voter import Voter, BallotStatus
from backend.main.objects.ballot import Ballot
from flask_api import FlaskAPI, status
import jsons
from flask_cors import CORS

app = FlaskAPI(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:*", "http://127.0.0.1:*"]}})


@app.route('/')
def ping():
    return 'pong'


@app.route('/api/count_ballot', methods=["POST"])
def count_ballot():
    req_data = request.get_json()
    ballot_number = req_data['ballot_number']
    chosen_candidate_id = req_data['chosen_candidate_id']
    voter_comments = req_data['voter_comments']
    voter_national_id = req_data['voter_national_id']

    ballot = Ballot(ballot_number, chosen_candidate_id, voter_comments)
    result = balloting.count_ballot(ballot, voter_national_id)
    return {"status": jsons.dumps(result.value)}, \
        status.HTTP_202_ACCEPTED if result == BallotStatus.BALLOT_COUNTED else status.HTTP_409_CONFLICT


@app.route('/api/get_all_candidates')
def get_all_candidates():
    return jsons.dumps(registry.get_all_candidates())


def populate_database():
    """
    This method is for you as a developer. This is where you can add more candidates for the election,
    register voters for the election and issue ballots. This method is strictly for your convenience, and
    is not part of the rubric for the final project.
    """

    # Adding Candidates for the election. These should be reflected in the frontend.
    registry.register_candidate("Joseph Klimek")
    registry.register_candidate("Rose Hervey")
    registry.register_candidate("Yeong Qi")
    registry.register_candidate("Karthik Banerjee")
    registry.register_candidate("Courtney Yu")
    registry.register_candidate("Hugo Jennings")
    registry.register_candidate("Maia Kift")
    registry.register_candidate("Arnav Arora")

    # TODO: Feel free to add voters to the voter registry, and issue ballots


populate_database()
