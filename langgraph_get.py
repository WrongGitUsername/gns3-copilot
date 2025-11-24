from agent import agent
from pprint import pprint

# get the latest state snapshot
config = {"configurable": {"thread_id": "d019e0be-6970-48ae-a154-e5f566843122"}}
StateSnapshot = agent.get_state(config)
pprint(StateSnapshot.values)

# get a state snapshot for a specific checkpoint_id
#config = {"configurable": {"thread_id": "1d019e0be-6970-48ae-a154-e5f566843122", "checkpoint_id": "1f0c6b78-6d0d-6d98-8006-bc36ede00d58"}}
#pprint(agent.get_state(config))
#pprint(list(agent.get_state_history(config)))
