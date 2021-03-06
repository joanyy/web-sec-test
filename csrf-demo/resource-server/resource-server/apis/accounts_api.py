import json
import logging

import flask


LOG = logging.getLogger(__name__)

THE_BANK = {
    'alice': 5000,
    'chuck': 1000,
}


def add_endpoints(flask_app, jinja_env):

    @flask_app.route('/accounts', methods=['GET'])
    def get_accounts():
        cookie_username = flask.request.cookies.get('username', None)
        if cookie_username is None:
            return json.dumps('unauthorized')

        global THE_BANK
        if cookie_username in THE_BANK:
            return f'hello {cookie_username}, you have ${THE_BANK[cookie_username]}'
        return f'you do not have a balance'

    @flask_app.route('/transfer', methods=['POST'])
    def post_transfer():
        from_id = flask.request.args.get('from')
        to_id = flask.request.args.get('to')
        amt = int(flask.request.args.get('amt'))

        cookie_username = flask.request.cookies.get('username', None)
        if cookie_username != from_id:
            LOG.info(
                f'unauthorized transfer: {cookie_username} trying to access'
                f' from_id'
            )
            return json.dumps('unauthorized')

        LOG.info(f'cookie username auth\'d: {cookie_username}')
        global THE_BANK
        if from_id in THE_BANK and to_id in THE_BANK and \
                THE_BANK[from_id] >= amt:
            LOG.info(f'Transfering {amt} from {from_id} to {to_id}')
            THE_BANK[from_id] = THE_BANK[from_id] - amt
            THE_BANK[to_id] = THE_BANK[to_id] + amt

        LOG.info(f'THE BANK: {json.dumps(THE_BANK, indent=2)}')

        return json.dumps(THE_BANK, indent=2)
