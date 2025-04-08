import math
import enum

class NoiseType(enum.Enum):
    RESISTIVE = 1
    INDUCTIVE = 2
    BOTH = 3

class Noc:
    def __init__(self, size: int, *, 
                 buffer_size: int = 4,
                 activity_thresh: int = 3,
                 injection_rate_numerator: int = 3,
                 injection_rate_denominator: int = 10,
                 resistive_noise_threshold: int = 1,
                 inductive_noise_threshold: int = 1):
        self.size = size
        self._n = int(math.sqrt(size))
        self.buffer_size = buffer_size
        self.activity_thresh = activity_thresh
        self.injection_rate_numerator = injection_rate_numerator
        self.injection_rate_denominator = injection_rate_denominator
        self.resistive_noise_threshold = resistive_noise_threshold
        self.inductive_noise_threshold = inductive_noise_threshold

    def __str__(self):
        return self.variables() \
                + self.datatypes() \
                + self.noc_init() \
                + self.functions() \
                + self.processes() \
                + self.composition()
    
    def print(self, noise_type: NoiseType, clk_low: int, clk_high: int, stride: int = 1):
        properties: str = ""
        if noise_type == NoiseType.RESISTIVE or noise_type == NoiseType.BOTH:
            properties += self.resistive_range(clk_low, clk_high, stride)
        
        if noise_type == NoiseType.INDUCTIVE or noise_type == NoiseType.BOTH:
            properties += self.inductive_range(clk_low, clk_high, stride)
        
        return self.variables() \
                + self.datatypes() \
                + properties \
                + self.noc_init() \
                + self.functions() \
                + self.processes() \
                + self.composition()
            
    def variables(self):
        return f"""\
//----- VARIABLES -----

// #MODULARIZE by setting NOC_MAX_ID to 1 less than the total number of routers and allocating spaces for more routers
const int NOC_MAX_ID = {self.size - 1};
router[] noc = array(i, NOC_MAX_ID + 1, router{{}});

// #CUSTOMIZE this value changes the buffer length of all buffers.
const int BUFFER_LENGTH = {self.buffer_size};

// #CUSTOMIZE the number of buffers a router must service before noise will be incramented.
const int ACTIVITY_THRESH = {self.activity_thresh};

// #CUSTOMIZE these values change the frequency with witch flits are injected.
const int INJECTION_RATE_NUMERATOR = {self.injection_rate_numerator};
const int INJECTION_RATE_DENOMINATOR ={self.injection_rate_denominator};

// #CUSTOMIZE this is the upper bound of cycles run before quiting.
int(0..INJECTION_RATE_DENOMINATOR) clk = 0;
transient int(0..1) clk_indicator;

// #CUSTOMIZE this is the upper threshoold for noise detected in the system.
const int RESISTIVE_NOISE_THRESH = {self.resistive_noise_threshold};
const int INDUCTIVE_NOISE_THRESH = {self.inductive_noise_threshold};

// These are for tracking resistive and inductive noise and must be initialized to 0.
int resistiveNoise = 0;
int inductiveNoise = 0;

// These values are enumerations and are NOT to be changed
const int NORTH = 0;
const int WEST = 1;
const int EAST = 2;
const int SOUTH = 3;
const int LOCAL = 4;
"""
    
    def datatypes(self):
        return f"""\
datatype buffer = {{
    int(0..NOC_MAX_ID) hd,
    buffer option tl
}};

datatype channel = {{
    buffer option buffer,
    bool serviced,
    bool isEmpty,
    bool isFull
}};

datatype router = {{
    channel[] channels,
    int(-1..NOC_MAX_ID)[] ids,
    int(0..4)[] priority_list,
    int(0..4)[] priority_list_temp,
    int(0..4) serviced_index,
    int(0..4) unserviced_index,
    int(0..5) total_unserviced,
    int thisActivity,
    int lastActivity,
    bool[] used
}};

datatype checker = {{bool[] routing}};
checker[] isRouting = [
    checker{{routing:[false, false, false, false, false]}},
    checker{{routing:[false, false, false, false, false]}}, 
    checker{{routing:[false, false, false, false, false]}},
    checker{{routing:[false, false, false, false, false]}}];
int[] states = [0, 0, 0, 0];
"""
    
    def noc_init(self):
        init: str = ""

        for y in range(self._n):
            for x in range(self._n):
                # calculate the linearized id
                id = x + y * self._n

                # calculate the id's of surrounding routers
                id_north = x + (y - 1) * self._n
                id_west = (x - 1) + y * self._n
                id_east = (x + 1) + y * self._n
                id_south = x + (y + 1) * self._n
                
                if id_north < 0 or id_north >= self.size - 1:
                    id_north = -1
                if id_west < 0 or id_west >= self.size - 1:
                    id_west = -1
                if id_east < 0 or id_east >= self.size - 1:
                    id_east = -1
                if id_south < 0 or id_south >= self.size - 1:
                    id_south = -1

                init += f"""\
noc[{id}] = router {{
channels: [
    channel {{serviced: false, isEmpty: true}},
    channel {{serviced: false, isEmpty: true}},
    channel {{serviced: false, isEmpty: true}},
    channel {{serviced: false, isEmpty: true}},
    channel {{serviced: false, isEmpty: true}}],
ids: [{id_north}, {id_west}, {id_east}, {id_south}],
priority_list: [NORTH, EAST, SOUTH, WEST, LOCAL],
total_unserviced: 0,
used: [false, false, false, false, false],
thisActivity: 0,
lastActivity: 0
}}  
"""
                
        return init
    
    def resistive_noise(self, clk: int):
        return f"""\
property resistiveNoiseProbability1RewardBounded{clk}  = Pmax(<>[S(clk_indicator)<={clk}] (resistiveNoise >= RESISTIVE_NOISE_THRESH));
"""
    
    def inductive_noise(self, clk: int):
        return f"""\
property inductiveNoiseProbability1RewardBounded{clk}  = Pmax(<>[S(clk_indicator)<={clk}]  (inductiveNoise >= INDUCTIVE_NOISE_THRESH));
"""
    
    def resistive_range(self, clk_low: int, clk_high: int, stride: int = 1):
        properties: str = ""
        for clk in range(clk_low, clk_high+1, stride):
            properties += self.resistive_noise(clk)
        return properties
    
    def inductive_range(self, clk_low: int, clk_high: int, stride: int = 1):
        properties: str = ""
        for clk in range(clk_low, clk_high+1, stride):
            properties += self.inductive_noise(clk)
        return properties
    
    def functions(self):
        return f"""\
// Calculate length of list
function int len(buffer option ls) = if ls == none then 0 else 1 + len(ls!.tl);

// Tell if the buffer is full
function bool isBufferFull(buffer option ls) = len(ls) >= BUFFER_LENGTH;

// Get the mirror direction
function int getDestinationChannel(int dir) =
    if dir == NORTH then SOUTH
    else if dir == WEST then EAST
    else if dir == EAST then WEST
    else if dir == SOUTH then NORTH
    else -1;

// Determine if the flits destination is in the same column as the current router
function int getColumnShift(int id, int dst) =
(dst % ((int)sqrt(NOC_MAX_ID + 1))) - (id % ((int)sqrt(NOC_MAX_ID + 1)));

// Return the front of the queue
function int peekFront(buffer option ls) =
    if ls == none then -1
    else if ls!.tl == none then ls!.hd
    else peekFront(ls!.tl);

// Add a flit to the buffer
function buffer option enqueue(int n, buffer option ls) =
    if len(ls) == BUFFER_LENGTH then ls
    else some(buffer {{
        hd: n,
        tl: ls
    }});

// Remove a flit from the buffer
function buffer option dequeue(buffer option ls) =
    if ls == none then none
    else if ls!.tl == none then none
    else some(buffer {{
        hd: ls!.hd,
        tl: dequeue(ls!.tl)
    }});
"""
    
    def processes(self):
        return """\
process GenerateFlits(int id){
    int(0..NOC_MAX_ID) destination;
    if(clk < INJECTION_RATE_NUMERATOR){
        // Determine a destiantion
        //palt{
            // #MODULARIZE by adding a probability for (NOC_MAX_ID - 1) destinations.
            // #CUSTOMIZE by changing the flit injection pattern. Check router IDs with if-else blocks to make more router specific changes.
        //	:(1/3): {= destination = 0 =}
        //	:(1/3): {= destination = 1 =}
        //	:(1/3): {= destination = 2 =}
        //};
        {= 
            destination = DiscreteUniform(0, NOC_MAX_ID - 1) 
        =};

        // Make sure it is not this router and add it to the local buffer.
        if(destination >= id){
            {=
                noc[id].channels[LOCAL].buffer = enqueue(destination + 1, noc[id].channels[LOCAL].buffer)
            =}
        }
        else{
            {=
                noc[id].channels[LOCAL].buffer = enqueue(destination, noc[id].channels[LOCAL].buffer)
            =}
        }
    }
    else {
        tau
    }
}

process PrepChannel(int id, int ch){
    {=
       noc[id].channels[ch].isEmpty = len(noc[id].channels[ch].buffer) == 0,
       noc[id].channels[ch].isFull = isBufferFull(noc[id].channels[ch].buffer)
    =}
}

process PrepRouter(int id){
    PrepChannel(id, 0);
    PrepChannel(id, 1);
    PrepChannel(id, 2);
    PrepChannel(id, 3);
    PrepChannel(id, 4)
}

// Send flit to northern router. src and dst are channels (ie NORTH, WEST, EAST, SOUTH, LOCAL), NOT the actual router ids!
process Send(int id, int ch, int dir){
    // We want to chech the final destination buffer of the router we are headed into, to see if it is full
    int(-1..3) dst;
    {=
        // A flit going from router 0 to router 1 leaves 0 from the SOUTH and enters 1 from the NORTH.
        dst = getDestinationChannel(dir)
    =};

    // If the destination is not full, and the channel has not been used in this cycle, then service the buffer
    if(!noc[noc[id].ids[dir]].channels[dst].isFull && !noc[id].used[dir]){
        {=
            // First set that a transaction is being made
            0: isRouting[id].routing[ch] = true,

            // First, add flit to destination buffer
            1: noc[noc[id].ids[dir]].channels[dst].buffer =
                enqueue(peekFront(noc[id].channels[ch].buffer), noc[noc[id].ids[dir]].channels[dst].buffer),

            // Then, remove it from the source buffer
            2: noc[id].channels[ch].buffer = dequeue(noc[id].channels[ch].buffer),

            // Remove the inditactor
            3: isRouting[id].routing[ch] = false,

            // Mark that output as used and that channel as serviced
            4: noc[id].used[dir] = true,
            4: noc[id].channels[ch].serviced = true,

            // Incrament the count for buffers serviced in this cycle
            4: noc[id].thisActivity++
        =}
    }
    // Otherwise, increment total unserviced buffers
    else{
        {=
            noc[id].total_unserviced++
        =}
    }
}

// Advance flits to respective buffers
process AdvanceFlits(int id, int ch){
    // If flit needs to stay on this row
    if(getColumnShift(id, peekFront(noc[id].channels[ch].buffer)) == 0){
        // Send it north
        if(peekFront(noc[id].channels[ch].buffer) < id){
            Send(id, ch, NORTH)
        }
        // Or send it south
        else{
            Send(id, ch, SOUTH)
        }
    }
    // Else, if flit needs to go west
    else if(getColumnShift(id, peekFront(noc[id].channels[ch].buffer)) < 0){
        Send(id, ch, WEST)
    }
    // Else, flit needs to go east
    else{
        Send(id, ch, EAST)
    }
}

// Update a specific channel
process AdvanceChannel(int id, int ch){
    // If this channel was not assigned a neighbor...
    if(ch != 4 && noc[id].ids[ch] == -1){
        {=
            // Mark the channel as serviced
            noc[id].channels[ch].serviced = true
        =}
    }
    // If this channel was assigned a neighbor or is local, but it is empty...
    else if(noc[id].channels[ch].isEmpty == true){
        {=
            // Mark the channel as serviced
            noc[id].channels[ch].serviced = true
        =}
    }
    // If the flit has reached its destination...
    else if(peekFront(noc[id].channels[ch].buffer) == id){
        // ... and the local channel has not been used
        if (!noc[id].used[LOCAL]){
            {=
                // Mark the channel as serviced and used
                noc[id].channels[ch].serviced = true,
                noc[id].used[LOCAL] = true,

                // Incrament the count for buffers serviced in this cycle
                noc[id].thisActivity++,

                // Remove this flit. It has reached its destination
                noc[id].channels[ch].buffer = dequeue(noc[id].channels[ch].buffer)
            =}
        }
        // Otherwise, increment total unserviced buffers
        else{
            {=
                noc[id].total_unserviced++
            =}
        }
    }

    // Otherwise, the flit must be for another router
    else{
        AdvanceFlits(id, ch)
    }
}

// Update the directions of the next flits in the buffers
process AdvanceRouter(int id){
    AdvanceChannel(id, noc[id].priority_list[0]);
    AdvanceChannel(id, noc[id].priority_list[1]);
    AdvanceChannel(id, noc[id].priority_list[2]);
    AdvanceChannel(id, noc[id].priority_list[3]);
    AdvanceChannel(id, noc[id].priority_list[4])
}

process UpdatePriorityList(int id, int i){
    if(noc[id].channels[noc[id].priority_list[i]].serviced){
        {=
            0: noc[id].priority_list_temp[noc[id].total_unserviced + noc[id].serviced_index] = noc[id].priority_list[i],
            1: noc[id].serviced_index++
        =}
    }
    else{
        {=
            0: noc[id].priority_list_temp[noc[id].unserviced_index] = noc[id].priority_list[i],
            1: noc[id].unserviced_index++
        =}
    }
}

// Update priority list
process UpdatePiority(int id){
    // Reset all of the temp values
    {=
        noc[id].priority_list_temp = [0, 0, 0, 0, 0],
        noc[id].serviced_index = 0,
        noc[id].unserviced_index = 0
    =};
    // Update the ordering of priorities in the lists
    UpdatePriorityList(id, 0);
    UpdatePriorityList(id, 1);
    UpdatePriorityList(id, 2);
    UpdatePriorityList(id, 3);
    UpdatePriorityList(id, 4);

    {=
        // Make our next priority list the current priority list
        noc[id].priority_list = noc[id].priority_list_temp,

        // Reset the used and serviced variables
        noc[id].channels[0].serviced = false,
        noc[id].channels[1].serviced = false,
        noc[id].channels[2].serviced = false,
        noc[id].channels[3].serviced = false,
        noc[id].channels[4].serviced = false,
        noc[id].total_unserviced = 0,
        noc[id].used = [false, false, false, false, false]
    =}
}

// Update the noise tracking variables for this router.
process UpdateNoiseTracking(int id){
    
    {= 
       // Update inductive noise
       inductiveNoise += abs(noc[id].lastActivity - noc[id].thisActivity) >= ACTIVITY_THRESH ? 1 : 0,
       
       // Update resistive noise
       resistiveNoise += noc[id].thisActivity >= ACTIVITY_THRESH ? 1 : 0,
       
       // Update trackers for next round
       noc[id].lastActivity = noc[id].thisActivity,
       noc[id].thisActivity = 0
    =}
}

// Process for behavior
process RouterBehavior(int id) {
    // Run
    GenerateFlits(id);
    // Determine what channels will send this cycle
    PrepRouter(id);
    do{
        sync{= states[id] = 1 =};
        // Send the flits
        AdvanceRouter(id);
        // Update the priority list
        UpdatePiority(id);
        // Update resistive and inductive values
        UpdateNoiseTracking(id);

        tick{= states[id] = 0 =};
        // Generate new flits
        GenerateFlits(id);
        // Determine what channels will send this cycle
        PrepRouter(id)
    }
}

// For syncing parallell processes
process Clock(){
    tick {= clk = (clk + 1) % INJECTION_RATE_DENOMINATOR, clk_indicator = 1 =};
    Clock()
}
"""

    def composition(self):
        composition: str = "par {\n    :: Clock()\n"
        for i in range(self.size):
            composition += f"    :: RouterBehavior({i})\n"
        composition += "}\n"

        return composition