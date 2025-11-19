"""Helper functions for instantiating NoCs in Modest"""

def noc_init(dimension) -> str:
    """Returns initialization for a dimension x dimension NoC"""
    num_nodes = dimension*dimension
    init: str = "router[] noc = [\n"

    for y in range(dimension):
        for x in range(dimension):
            # calculate the linearized id
            id = x + y * dimension

            # calculate the id's of surrounding routers
            id_north = x + (y - 1) * dimension
            id_west = (x - 1) + y * dimension
            id_east = (x + 1) + y * dimension
            id_south = x + (y + 1) * dimension

            if y - 1 < 0:
                id_north = "NO_CONNECT"
            if x - 1 < 0:
                id_west = "NO_CONNECT"
            if x + 1 >= dimension:
                id_east = "NO_CONNECT"
            if y + 1 >= dimension:
                id_south = "NO_CONNECT"

            init += f"""\
router {{
    channels: [
        channel {{buffer: none, serviced: false, isEmpty: true, isFull: false}},
        channel {{buffer: none, serviced: false, isEmpty: true, isFull: false}},
        channel {{buffer: none, serviced: false, isEmpty: true, isFull: false}},
        channel {{buffer: none, serviced: false, isEmpty: true, isFull: false}},
        channel {{buffer: none, serviced: false, isEmpty: true, isFull: false}}],
    ids: [{id_north}, {id_west}, {id_east}, {id_south}],
    priority_list: [NORTH, EAST, SOUTH, WEST, LOCAL],
    priority_list_temp: [0, 0, 0, 0, 0],
    serviced_index: 0,
    unserviced_index: 0,
    total_unserviced: 0,
    thisActivity: 0,
    lastActivity: 0,
    used: [false, false, false, false, false]
}}"""
            if id < num_nodes - 1:
                init += ",\n"
            else:
                init += "];\n"
            
    return init

def noise_tracking_init() -> str:
    """Returns initialization for resistive and inductive noise"""
    return """\
int resistiveNoise = 0;
int inductiveNoise = 0;
"""

def composition(dimension) -> str:
    """Returns the composition of Clock with Router for a dimension x dimension NoC"""
    num_nodes = dimension*dimension
    composition: str = "par {\n    :: Clock()\n"
    for i in range(num_nodes):
        composition += f"    :: Router({i})\n"
    composition += "}\n"

    return composition

def property(name: str, prop: int) -> str:
    """Returns a Modest property"""
    return f"""\
property {name} = {prop};
"""

__all__ = ["property", "composition", "noise_tracking_init", "noc_init"]