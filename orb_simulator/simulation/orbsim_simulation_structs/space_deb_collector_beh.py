from typing import Callable, List
from simulation.orbsim_simulation_structs.agent_behaviour import AgentBehaviour
from simulation.orbsim_simulation_structs.space_deb_collector_actions import default_collector_actions
from simulation.orbsim_simulation_structs.space_deb_collector_rules import default_collector_rules

class SpaceDebrisCollectorBeh(AgentBehaviour):

    def __init__(self, actions: List[Callable] = None, rules: List[Callable] = None) -> None:
        if not rules and not actions:
            self.actions = default_collector_actions
            self.rules = default_collector_rules
        
        elif actions and rules:
            self.actions = actions + default_collector_actions
            self.rules = rules + default_collector_rules
            super().__init__(self.actions, self.rules)





    