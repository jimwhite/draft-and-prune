from z3 import *

# Movie indices: horror=0, mystery=1, romance=2, sci-fi=3, western=4
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
movie_idx = {m: i for i, m in enumerate(movies)}

# Slot indices: 0=screen1_7pm, 1=screen1_9pm, 2=screen2_7pm, 3=screen2_9pm, 4=screen3_8pm
slot = [Int(f"slot_{m}") for m in movies]

# Base solver
solver = Solver()

# Domain constraints: each movie assigned to exactly one slot (0-4)
solver.add(Distinct(slot))
for i in range(5):
    solver.add(slot[i] >= 0, slot[i] <= 4)

# Helper function to get screen number from slot index
def get_screen(slot_idx):
    if slot_idx == 0 or slot_idx == 1:
        return 1
    elif slot_idx == 2 or slot_idx == 3:
        return 2
    else:  # slot_idx == 4
        return 3

# Ordering constraints
# Western before horror: western slot < horror slot
solver.add(slot[movie_idx["western"]] < slot[movie_idx["horror"]])

# Sci-fi not on screen3 (slot 4)
solver.add(slot[movie_idx["sci-fi"]] != 4)

# Romance not on screen2 (slots 2 and 3 are screen2)
solver.add(Or(slot[movie_idx["romance"]] == 0, 
             slot[movie_idx["romance"]] == 1,
             slot[movie_idx["romance"]] == 4))

# Horror and mystery on different screens
horror_screen = If(slot[movie_idx["horror"]] == 0, 1,
                   If(slot[movie_idx["horror"]] == 1, 1,
                      If(slot[movie_idx["horror"]] == 2, 2,
                         If(slot[movie_idx["horror"]] == 3, 2, 3))))
mystery_screen = If(slot[movie_idx["mystery"]] == 0, 1,
                    If(slot[movie_idx["mystery"]] == 1, 1,
                       If(slot[movie_idx["mystery"]] == 2, 2,
                          If(slot[movie_idx["mystery"]] == 3, 2, 3))))
solver.add(horror_screen != mystery_screen)

# Answer choices (screen1: slot0=7pm, slot1=9pm)
answer_choices = [
    ("sci-fi", "horror"),   # choice0: sci-fi at 7pm, horror at 9pm
    ("sci-fi", "mystery"),  # choice1: sci-fi at 7pm, mystery at 9pm
    ("western", "horror"),  # choice2: western at 7pm, horror at 9pm
    ("western", "mystery"), # choice3: western at 7pm, mystery at 9pm
    ("western", "sci-fi")   # choice4: western at 7pm, sci-fi at 9pm
]

# Check each answer choice
answer_index_list = []
for idx, (first_movie, second_movie) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint for screen1 assignment
    s_chk.add(slot[movie_idx[first_movie]] == 0)   # 7pm slot
    s_chk.add(slot[movie_idx[second_movie]] == 1)  # 9pm slot
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)