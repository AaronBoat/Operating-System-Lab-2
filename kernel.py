### Fill in the following information before submitting
# Group id: 
# Members: 



from collections import deque

# PID is just an integer, but it is used to make it clear when a integer is expected to be a valid PID.
PID = int

# This class represents the PCB of processes.
# It is only here for your convinience and can be modified however you see fit.
class PCB:
    pid: PID
    priority: int

    def __init__(self, pid: PID, priority: int):
        self.pid = pid
        self.priority = priority


# This class represents the Kernel of the simulation.
# The simulator will create an instance of this object and use it to respond to syscalls and interrupts.
# DO NOT modify the name of this class or remove it.
class Kernel:
    scheduling_algorithm: str
    ready_queue: deque[PCB]
    waiting_queue: deque[PCB]
    running: PCB
    idle_pcb: PCB

    ## add timer count for RR
    timer_count: int

    # Called before the simulation begins.
    # Use this method to initilize any variables you need throughout the simulation.
    # logger is provided which allows you to include your own print statements in the
    #   output logs. These will not impact grading. This can be done with its .log method
    #   which accepts a string.
    # DO NOT rename or delete this method. DO NOT change its arguments.
    def __init__(self, scheduling_algorithm: str, logger):
        self.scheduling_algorithm = scheduling_algorithm
        self.ready_queue = deque()
        self.waiting_queue = deque()
        self.idle_pcb = PCB(0, 0)
        self.running = self.idle_pcb
        self.timer_count = 0

    # This method is triggered every time a new process has arrived.
    # new_process is this process's PID.
    # DO NOT rename or delete this method. DO NOT change its arguments.
    def new_process_arrived(self, new_process: PID, priority: int, process_type: str) -> PID:
        self.ready_queue.append(PCB(new_process, priority))
        self.choose_next_process()
        return self.running.pid  

    # This method is triggered every time the current process performs an exit syscall.
    # DO NOT rename or delete this method. DO NOT change its arguments.
    ## Todo: 
    def syscall_exit(self) -> PID:
        self.timer_count = 0
        self.running = self.idle_pcb
        self.choose_next_process()
        return self.running.pid
    
    # This method is triggered when the currently running process requests to change its priority.
    # DO NOT rename or delete this method. DO NOT change its arguments.
    def syscall_set_priority(self, new_priority: int) -> PID:
        self.running.priority = new_priority
        self.choose_next_process()
        return self.running.pid


    # This is where you can select the next process to run.
    # This method is not directly called by the simulator and is purely for your convinience.
    # Feel free to modify this method as you see fit.
    # It is not required to actually use this method but it is recommended.
    def choose_next_process(self):
        if len(self.ready_queue) == 0:
                return
        
        if self.scheduling_algorithm == "FCFS":
            if self.running is self.idle_pcb:
                self.running = self.ready_queue.popleft()

        elif self.scheduling_algorithm == "Priority":
            candidate = self.ready_queue[0]

            for process in self.ready_queue: #find the highest priority process from the ready_queue, then compare it with the current running process
                if process.priority > candidate.priority:
                    candidate = process
                elif process.priority == candidate.priority:
                    if process.pid < candidate.pid:
                        candidate = process

            if self.running is self.idle_pcb:  #check if CPU is idle
                self.ready_queue.remove(candidate)
                self.running = candidate

            elif self.running.priority < candidate.priority: #if cpu not idle, is the current running priority smaller than the candidate priority
                self.ready_queue.remove(candidate)
                self.ready_queue.append(self.running)
                self.running = candidate

            elif self.running.priority == candidate.priority: #if same priority we need to check pid
                if candidate.pid < self.running.pid:
                    self.ready_queue.remove(candidate)
                    self.ready_queue.append(self.running)
                    self.running = candidate

        else:
            if self.scheduling_algorithm == "RR":
                if self.running is self.idle_pcb:
                    self.running = self.ready_queue.popleft()
            else:    
                print("Unknown scheduling algorithm")

    # This method represents the hardware timer interrupt.
    # It is triggered every 10 milliseconds and is the only way our kernel can track passing time.
    # Do not use real time to track how much time has passed as time is simulated.
    # DO NOT rename or delete this method. DO NOT change its arguments.
    def timer_interrupt(self) -> PID:
        if self.scheduling_algorithm == "RR":
            if self.running != self.idle_pcb:    
                self.timer_count += 1
                if(self.timer_count == 4):
                    self.timer_count = 0
                    self.ready_queue.append(self.running)
                    self.running = self.idle_pcb
                    self.choose_next_process()
            else:
                self.timer_count = 0
        return self.running.pid