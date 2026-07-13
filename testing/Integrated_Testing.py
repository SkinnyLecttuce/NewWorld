import random

from apps.services import TMDB_API_Handler
from apps.core import SetBuilder
from apps.core import Utils

def initialise_tmdb_api():
    print("initialising tmdb api...")
    TMDB_API_Handler.auth_token()  # always auth before anything

    # return raw packets for search query
    packets = TMDB_API_Handler.query_search("Star Wars", 5)

    # filtration
    packets = Utils.the_filter(packets, filters={'adult': False, 'original_language': 'en', 'genre_ids': [16, 878]})

    if (len(packets)):  # not zero packet length
        # packets to node objects
        nodes = Utils.packets_to_node_objects(packets)

        # sortation
        nodes = Utils.the_sorter(nodes, sorters={'popularity': 'asc'})  # sort popularity ascending

        for n in nodes:  # print the nodes
            print(n.out(fancify=True))
        return nodes
    return False

def standard_test(): #fulltime is 71 mins
    print("starting standard test...")
    nodes=initialise_tmdb_api()
    if(nodes):
        print("running set integrity testing")
        # set builder running on the collection of nodes
        fulltime = 71
        setz = SetBuilder.SetBuilder(fulltime, nodes, False)  # duration of movie set is 71min

        setz.select(setz.nobj[1])  # select a movie of duration 66mins

        for n in setz.nobj:
            print(n.out(fancify=True))

        assert not setz.selected == []  # must be not empty cuz 71mins>66mins - valid selection

        delta_t = fulltime - setz.selected[0].duration

        print(f"set duration set to {fulltime}mins")
        print(f"selected a {setz.selected[0]}mins film:", setz.selected[0].index)

        for n in setz.nobj:  # check if all nodes with duration <= 71-66 are active
            if (n.duration <= delta_t):
                assert n.active
            else:
                assert not n.active

        print("set integrity 50% ok")

        setz.deselect(0)  # deselect movie of duration 66mins

        for n in setz.nobj:
            print(n.out(fancify=True))

        assert setz.selected == []  # must be empty - valid deselection

        delta_t = delta_t + setz.not_selected[len(setz.not_selected) - 1].duration

        print(f"set duration remaining {delta_t}mins")
        print(f"deselected {setz.not_selected[len(setz.not_selected) - 1]}mins film:",
              setz.not_selected[len(setz.not_selected) - 1].index)

        for n in setz.nobj:  # check if all nodes with duration <= 71 are active
            if (n.duration <= delta_t):
                assert n.active
            else:
                assert not n.active

        for n in setz.nobj:
            print(n.out(fancify=True))

        print("set integrity ok, smooth sailing...")
        print("test pass")

    else:
        print("no results")

def fuzzy_test(fulltime:int):
    print("starting fuzzy test...")
    nodes=initialise_tmdb_api()

    # --- START OF RANDOMIZED INTEGRITY FUZZING TEST ---
    print("\n--- Starting Random Selection/Deselection Fuzzing Test ---")

    # Configuration for the fuzzing run
    NUMBER_OF_TEST_STEPS = 100
    setz = SetBuilder.SetBuilder(fulltime, nodes, False)  # Fresh or existing instance

    for step in range(1, NUMBER_OF_TEST_STEPS + 1):
        # Determine what actions are legally possible at this millisecond
        available_to_select = [n for n in setz.nobj if n.active]
        available_to_deselect = list(setz.selected)

        # Decide possible actions dynamically based on state
        possible_actions = []
        if available_to_select:
            possible_actions.append("SELECT")
        if available_to_deselect:
            possible_actions.append("DESELECT")

        # If the set is completely locked up and no action can be taken, break or reset
        if not possible_actions:
            print(f"Step {step}: No further valid moves possible (Set saturated). Ending loop.")
            break

        # Pick an action completely at random
        action = random.choice(possible_actions)

        if action == "SELECT":
            node_to_select = random.choice(available_to_select)
            print(
                f"[Step {step}] Randomly SELECTING node Index: {node_to_select.index} (Duration: {node_to_select.duration}m)")
            setz.select(node_to_select)

        elif action == "DESELECT":
            # Pick a random index out of the currently selected list
            random_index = random.randrange(len(setz.selected))
            node_to_deselect = setz.selected[random_index]
            print(
                f"[Step {step}] Randomly DESELECTING node Index: {node_to_deselect.index} (Duration: {node_to_deselect.duration}m)")
            setz.deselect(random_index)

        # --- INLINE INTEGRITY INVARIANT CHECKS ---
        # 1. Calculate remaining capacity dynamically
        total_selected_duration = sum(n.duration for n in setz.selected)
        current_delta_t = fulltime - total_selected_duration

        # 2. Enforce structural properties across all nodes after the random change
        for n in setz.nobj:
            # If a node is already explicitly chosen, it shouldn't be marked "active" for another selection
            if n in setz.selected:
                # Adjust this asset statement depending on whether your architecture
                # marks selected nodes as active=False or leaves active=True.
                continue

                # Global rule: Node active state MUST perfectly map to current capacity bounds
            if n.duration <= current_delta_t:
                assert n.active, f"Integrity Failure at Step {step}: Node {n.index} ({n.duration}m) should be ACTIVE for remaining {current_delta_t}m capacity!"
            else:
                assert not n.active, f"Integrity Failure at Step {step}: Node {n.index} ({n.duration}m) should be INACTIVE for remaining {current_delta_t}m capacity!"

    print(f"Successfully passed {step} chaotic randomized operations! Ultimate integrity confirmed.")
    # --- END OF RANDOMIZED INTEGRITY FUZZING TEST ---

#standard_test()
fuzzy_test(120)