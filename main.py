#!/bin/python3

import math
import os
import random
import re
import sys
from typing import Dict, Optional, Tuple, Any

Action = str

# Implement the State class here


class State:
    """
    0: unauthorized
    1: authorized
    """

    def __init__(self, authorizedFlag):
        self.name = authorizedFlag == 0 and 'unauthorized' or 'authorized'

    def __str__(self):
        return self.name


unauthorized = State(0)
authorized = State(1)

# Implement the transition_table here
# state value tuple:
# action_name
# checker: -> Tuple[bool, int, Optional]
#   action_param
#   atm_password
#   atm_current_balance
# checker_returned_tuple:
#   bool: if transition should be performed or not
#   int: new balance of the ATM after transition
#   value returned by the transition (??) [only relevant when fetching balance]
# next_state
transition_table = {
    unauthorized: [(
        'login',
        lambda ap, pw, bl: (ap == pw, bl, None),
        authorized,
    )],

    authorized: [(
        'withdraw',
        lambda ap, pw, bl: (ap <= bl, bl - ap, None),
        authorized,
    )],
}

# Implement the init_state here
init_state = unauthorized

# Look for the implementation of the ATM class in the below Tail section

if __name__ == "__main__":
    class ATM:
        def __init__(
            self,
            init_state: State,
            init_balance: int,
            password: str,
            transition_table: Dict
        ):
            self.state = init_state
            self._balance = init_balance
            self._password = password
            self._transition_table = transition_table

            # print(self.state)
            # print(self._transition_table)
            # print('========')

        def next(
            self,
            action: Action,
            param: Optional
        ) -> Tuple[bool, Optional[any]]:
            try:
                for transition_action, check, next_state in self._transition_table[self.state]:
                    if action == transition_action:
                        passed, new_balance, res = check(
                            param, self._password, self._balance)
                        if passed:
                            self._balance = new_balance
                            self.state = next_state
                            return True, res
            except KeyError:
                print('error')
            return False, None

    if __name__ == "__main__":
        fptr = open(os.environ["OUTPUT_PATH"], "w")
        password = input()
        init_balance = int(input())
        atm = ATM(init_state, init_balance, password, transition_table)
        q = int(input())
        for _ in range(q):
            action_input = input().split()
            action_name = action_input[0]
            try:
                action_param = action_input[1]
                if action_name in ['deposit', 'withdraw']:
                    action_param = int(action_param)
            except IndexError:
                action_param = None
            success, res = atm.next(action_name, action_param)
            if res is not None:
                message = f"Success={success} {atm.state} {res}\n"
                fptr.write(message)
                print(message)
            else:
                message = f"Success={success} {atm.state}\n"
                fptr.write(message)
                print(message)

        fptr.close()
