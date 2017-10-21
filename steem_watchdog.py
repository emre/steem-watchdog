import argparse
import logging
import time
from decimal import Decimal

from steem import Steem
from steem.commit import Commit

logger = logging.getLogger('steem-watchdog')
logger.setLevel(logging.DEBUG)
logging.basicConfig()


def reward_available(account):
    reward_steem_balance = Decimal(
        account['reward_steem_balance'].split(' ')[0])

    reward_sbd_balance = Decimal(
        account['reward_sbd_balance'].split(' ')[0])

    reward_vesting_balance = Decimal(
        account['reward_vesting_balance'].split(' ')[0])

    if any([reward_steem_balance, reward_sbd_balance, reward_vesting_balance]):
        logger.info("Found rewards.")
        return {
            "steem": reward_steem_balance,
            "sbd": reward_sbd_balance,
            "vesting": reward_vesting_balance,
        }
    else:
        logger.info("Nothing to claim. All reward balances are zero.")

    return False


def claim_rewards(steem, account_name):
    logger.info('Logged In. Checking for rewards.')
    account = steem.get_account(account_name)
    rewards = reward_available(account)
    if rewards:
        logger.info('Claiming rewards.')
        commit = Commit(steem)
        commit.claim_reward_balance(account=account_name)
        logger.info(
            'Rewards are claimed. %s STEEM, %s SBD, %s VESTS',
            rewards["steem"],
            rewards["sbd"],
            rewards["vesting"],
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("account")
    parser.add_argument("posting_key", help="Posting key of account")
    parser.add_argument("--node",
                        help="RPC node to connect")
    args = parser.parse_args()
    nodes = [args.node] if args.node else None

    steem = Steem(keys=[args.posting_key], nodes=nodes)

    while True:
        claim_rewards(steem, args.account)
        logger.info('Sleeping.')
        time.sleep(3600)  # sleep for one hour.


if __name__ == '__main__':
    main()
