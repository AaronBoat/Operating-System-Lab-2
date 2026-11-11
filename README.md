# CS 143A Project 3

## 1. Introduction

In this programming assignment, you will be building off your previous implementation in project 2. You must implement additional kernel syscalls and cpu interrupts. By the end of the project, you will implement synchronization primitives.

**Programming language:** The assignment will be implemented in Python.

**Cooperation and third party code:** This is a **group** programming assignment, and your group should implement the code on your own. Your group may not share final solutions with anyone outside of your group, and your group must write up your own work, expressing it in your own words/notation. Third party code including libraries are not allowed (built in python libraries are fine).

## 2. Environment setup

The simulator runs using standard Python without any installed libraries. Your code will be graded with **Python 3.10.12**, so we recommend using [conda](https://docs.conda.io/en/latest/) to create an environment with exactly that version. If you do not have conda yet, install [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

If you already created the `cs143a` environment for project 1 or 2, you can reuse it: just run `conda activate cs143a`. Otherwise, from the project folder (the one containing `requirements.txt`), create and activate the environment:

```
conda create --name cs143a --file requirements.txt
conda activate cs143a
python --version   # should print Python 3.10.12
```

Activate the environment (`conda activate cs143a`) every time you open a new terminal to work on the project.

You should avoid writing any code that is OS dependent as no test will require this and it could cause problems when grading.

## 3. Updating your code base

### 3.0 Starting point

Since this project builds on the previous one, you may use your old code as a starting point. If you do this, you must make some changes described in the next section. If you were unable to complete the second project or do not wish to use your original code, you may use the provided **`kernel.py`** in this folder, which is an implementation of project 2 with the changes from section 3.2 already made. It is highly recommended that you use your own code as a starting point as this will likely be easier.

### 3.1 Downloading the code

This project uses an upgraded simulator and has new simulations. The previous simulator **will not** be compatible with these new simulations. The new simulator (**`simulator.py`**), the new simulations (`simulations/`) and their correct output (`correct_output/`) are included in this folder. If you start from your own project 2 code, copy your **`kernel.py`** into this folder (replacing the provided one) and use the new **`simulator.py`**, simulations and correct output here instead of the ones from project 2.

### 3.2 Updates to `kernel.py`

There are a few changes that need to be made to your **`kernel.py`** file. If these changes are not made, the simulator **will not** work. All changes are for the `Kernel` class in **`kernel.py`**. (If you use the provided implementation of project 2, all of the following changes will have been made already.)

The list of changes include a set of new methods:

- `syscall_init_semaphore`
- `syscall_semaphore_p`
- `syscall_semaphore_v`
- `syscall_init_mutex`
- `syscall_mutex_lock`
- `syscall_mutex_unlock`

The actual changes:

**Entirely new methods (copy paste them at the bottom of your `kernel.py` class):**

```python
# This method is triggered when the currently running process requests to initialize a new semaphore.
# DO NOT rename or delete this method. DO NOT change its arguments.
def syscall_init_semaphore(self, semaphore_id: int, initial_value: int):
    return

# This method is triggered when the currently running process calls p() on an existing semaphore.
# DO NOT rename or delete this method. DO NOT change its arguments.
def syscall_semaphore_p(self, semaphore_id: int) -> PID:
    return self.running.pid

# This method is triggered when the currently running process calls v() on an existing semaphore.
# DO NOT rename or delete this method. DO NOT change its arguments.
def syscall_semaphore_v(self, semaphore_id: int) -> PID:
    return self.running.pid

# This method is triggered when the currently running process requests to initialize a new mutex.
# DO NOT rename or delete this method. DO NOT change its arguments.
def syscall_init_mutex(self, mutex_id: int):
    return

# This method is triggered when the currently running process calls lock() on an existing mutex.
# DO NOT rename or delete this method. DO NOT change its arguments.
def syscall_mutex_lock(self, mutex_id: int) -> PID:
    return self.running.pid

# This method is triggered when the currently running process calls unlock() on an existing mutex.
# DO NOT rename or delete this method. DO NOT change its arguments.
def syscall_mutex_unlock(self, mutex_id: int) -> PID:
    return self.running.pid
```

## 4. What to implement

### 4.1 Semaphore / Mutex

You must implement semaphores and mutexes for **FCFS**, **Priority**, and **RR** scheduling. (Note: This does not include the Multilevel scheduling algorithm. You will not need to implement semaphores or mutexes for this algorithm.)

Before a semaphore or mutex is used, some process will call `syscall_init_semaphore` with the id of the new semaphore and its initial value. The same is true for mutexes (`syscall_init_mutex`), but they do not have an initial value.

After being initialized, processes will call `p` and `v` for semaphores (`syscall_semaphore_p` / `syscall_semaphore_v`) or `lock` and `unlock` for mutexes (`syscall_mutex_lock` / `syscall_mutex_unlock`). According to the rules of semaphores and mutexes, processes should be prevented from executing appropriately: a process that is blocked must not run until it is released, and while it is blocked the kernel should run another process chosen by the current scheduling algorithm.

When it comes time to continue the execution of a process according to the rules of semaphores and mutexes, the different scheduling algorithms have different rules:

- **FCFS and RR:** release the process with the **lowest PID** that is blocked by this semaphore/mutex.
- **Priority:** release the process that has the **highest priority** according to Priority scheduling (as in project 2, the highest priority is the **highest** priority number; ties are broken by the lowest PID).

What happens after a process is released also depends on the scheduling algorithm:

- **FCFS:** semaphores should be **non-preemptive**. Meaning, if a process that arrived before the currently running process is released, there should not be an immediate context switch to it. (Note: Mutexes will not be tested with FCFS as it does not really make sense. We will leave you to consider why that is true.)
- **Priority:** the scheduler is still preemptive. The released process becomes ready again, and if it should now be running according to the Priority rules from project 2, switch to it immediately.
- **RR:** the released process joins the **back** of the ready queue (it does not preempt the running process). When it is later scheduled, it starts a fresh 40 millisecond quantum.

You can assume that no process will call `lock` on a mutex twice before calling `unlock`, and you can assume that `unlock` will only be called by a process that has previously locked the mutex.

## 5. Submitting

When submitting your code you should ONLY submit **`kernel.py`**. It must have this exact name. Upload this file to Gradescope. If after submitting you are unsatisfied with your score, you may submit again as many times as you like. We will only grade the most recent submission.
