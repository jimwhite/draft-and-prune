from z3 import *

# Movie indices: horror=0, mystery=1, romance=2, sci-fi=3, western=4
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
H, M, R, S, W = range(5)

# Position variables: each movie gets a unique position 0-4
pos = [Int(f"pos_{m}") for m in movies]

# Base solver
solver = Solver()

# All positions distinct and in range [0,4]
solver.add(Distinct(pos))
for i in range(5):
    solver.add(pos[i] >= 0, pos[i] <= 4)

# Map positions to (screen, time):
# pos=0: screen1@7, pos=1: screen2@7, pos=2: screen3@8, pos=3: screen1@9, pos=4: screen2@9
def get_screen(p):
    return If(p == 0, 1,
           If(p == 1, 2,
           If(p == 2, 3,
           If(p == 3, 1, 2))))

def get_time(p):
    return If(p == 0, 7,
           If(p == 1, 7,
           If(p == 2, 8,
           If(p == 3, 9, 9))))

# Screen assignment constraints via position mapping
for i in range(5):
    solver.add(get_screen(pos[i]) == If(pos[i] == 0, 1,
                                      If(pos[i] == 1, 2,
                                      If(pos[i] == 2, 3,
                                      If(pos[i] == 3, 1, 2)))))
    solver.add(get_time(pos[i]) == If(pos[i] == 0, 7,
                                    If(pos[i] == 1, 7,
                                    If(pos[i] == 2, 8,
                                    If(pos[i] == 3, 9, 9)))))

# Ordering constraint: western before horror
solver.add(pos[W] < pos[H])

# Screen-specific constraints:
# sci-fi not on screen 3 → position cannot be 2
solver.add(pos[S] != 2)

# romance not on screen 2 → position cannot be 1 or 4
solver.add(pos[R] != 1)
solver.add(pos[R] != 4)

# horror and mystery on different screens
# screen = 1 if pos in {0,3}, 2 if pos in {1,4}, 3 if pos == 2
def same_screen(p1, p2):
    return Or(
        And(p1 == 0, p2 == 0),
        And(p1 == 3, p2 == 3),
        And(Or(p1 == 0, p1 == 3), Or(p2 == 0, p2 == 3)),
        And(Or(p1 == 1, p1 == 4), Or(p2 == 1, p2 == 4)),
        And(And(p1 != 0, p1 != 3, p1 != 1, p1 != 4), And(p2 != 0, p2 != 3, p2 != 1, p2 != 4))
    )

# Simpler: compute screen directly from position
screen_of = [If(pos[i] == 0, 1,
             If(pos[i] == 1, 2,
             If(pos[i] == 2, 3,
             If(pos[i] == 3, 1, 2)))) for i in range(5)]

solver.add(screen_of[H] != screen_of[M])

# Answer choices: each is (7PM, 9PM) on screen1
answer_choices = [
    ("sci-fi", "horror"),  # index 0: sci-fi at pos=0, horror at pos=3
    ("sci-fi", "mystery"), # index 1: sci-fi at pos=0, mystery at pos=3
    ("western", "horror"), # index 2: western at pos=0, horror at pos=3
    ("western", "mystery"),# index 3: western at pos=0, mystery at pos=3
    ("western", "sci-fi")  # index 4: western at pos=0, sci-fi at pos=3
]

# Map movie names to indices
movie_idx = {"horror": H, "mystery": M, "romance": R, "sci-fi": S, "western": W}

answer_index_list = []
for idx, (first, second) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints: first movie at 7PM (pos=0), second at 9PM (pos=3) on screen1
    s_chk.add(pos[movie_idx[first]] == 0)
    s_chk.add(pos[movie_idx[second]] == 3)
    
    # Check if feasible
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)