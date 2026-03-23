from z3 import *

# Movie indices: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
movie_idx = {m: i for i, m in enumerate(movies)}

# Slot mapping: 0=(1,7), 1=(1,9), 2=(3,8), 3=(2,7), 4=(2,9)
# time_value[slot] = actual start time in hours
time_value = [7, 9, 8, 7, 9]
# screen_value[slot] = screen number
screen_value = [1, 1, 3, 2, 2]

# pos[m] = slot index (0-4) assigned to movie m
pos = [Int(f"pos_{m}") for m in movies]

# Base solver
solver = Solver()

# Domain constraints: each movie assigned to exactly one slot (0-4)
for p in pos:
    solver.add(p >= 0, p <= 4)

# Injectivity: all movies assigned to distinct slots
solver.add(Distinct(pos))

# Western before horror (by actual time)
time_western = Int('time_western')
time_horror = Int('time_horror')
solver.add(And(pos[4] >= 0, pos[4] <= 4))
solver.add(And(pos[0] >= 0, pos[0] <= 4))
solver.add(time_western == If(pos[4] == 0, time_value[0],
                              If(pos[4] == 1, time_value[1],
                                 If(pos[4] == 2, time_value[2],
                                    If(pos[4] == 3, time_value[3], time_value[4])))))
solver.add(time_horror == If(pos[0] == 0, time_value[0],
                             If(pos[0] == 1, time_value[1],
                                If(pos[0] == 2, time_value[2],
                                   If(pos[0] == 3, time_value[3], time_value[4])))))
solver.add(time_western < time_horror)

# Sci-fi not on screen 3 ⇒ slot ≠ 2
solver.add(pos[3] != 2)

# Romance not on screen 2 ⇒ slot ∉ {3,4}
solver.add(pos[2] != 3)
solver.add(pos[2] != 4)

# Horror and mystery on different screens
screen_horror = Int('screen_horror')
screen_mystery = Int('screen_mystery')
solver.add(And(pos[0] >= 0, pos[0] <= 4))
solver.add(And(pos[1] >= 0, pos[1] <= 4))
solver.add(screen_horror == If(pos[0] == 0, screen_value[0],
                               If(pos[0] == 1, screen_value[1],
                                  If(pos[0] == 2, screen_value[2],
                                     If(pos[0] == 3, screen_value[3], screen_value[4])))))
solver.add(screen_mystery == If(pos[1] == 0, screen_value[0],
                                If(pos[1] == 1, screen_value[1],
                                   If(pos[1] == 2, screen_value[2],
                                      If(pos[1] == 3, screen_value[3], screen_value[4])))))
solver.add(screen_horror != screen_mystery)

# Answer choices (screen 1 list: [7PM movie, 9PM movie])
answer_choices = [
    ["sci-fi", "horror"],
    ["sci-fi", "mystery"],
    ["western", "horror"],
    ["western", "mystery"],
    ["western", "sci-fi"]
]

# Check each choice
answer_index_list = []
for idx, (first_movie, second_movie) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assign first_movie to slot 0 (7PM), second_movie to slot 1 (9PM)
    s_chk.add(pos[movie_idx[first_movie]] == 0)
    s_chk.add(pos[movie_idx[second_movie]] == 1)
    
    # Remaining movies must occupy slots {2,3,4} (injectively)
    remaining_movies = [m for m in movies if m != first_movie and m != second_movie]
    remaining_pos = [pos[movie_idx[m]] for m in remaining_movies]
    
    # Ensure remaining movies are assigned to distinct slots from {2,3,4}
    s_chk.add(Distinct(remaining_pos))
    for p in remaining_pos:
        s_chk.add(Or(p == 2, p == 3, p == 4))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)