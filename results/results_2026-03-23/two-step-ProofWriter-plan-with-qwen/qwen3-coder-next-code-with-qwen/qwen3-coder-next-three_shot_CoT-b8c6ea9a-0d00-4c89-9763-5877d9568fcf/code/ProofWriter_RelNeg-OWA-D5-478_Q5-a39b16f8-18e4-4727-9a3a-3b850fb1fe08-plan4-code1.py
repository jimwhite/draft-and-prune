# --- Facts ---
facts:
is_kind("cow", True)
sees("cow", "mouse", True)
eats("mouse", "cow", True)
is_kind("mouse", True)
needs("mouse", "squirrel", True)
eats("rabbit", "mouse", True)
is_blue("rabbit", False)
is_blue("squirrel", False)
is_green("squirrel", True)
is_rough("squirrel", True)
needs("squirrel", "mouse", True)
sees("squirrel", "rabbit", True)

# --- Rules ---
rules:
foreach
    ?x sees("cow")
=> 
    ?x sees("squirrel")

foreach
    ?x sees("rabbit")
=> 
    ?x eats("cow")

foreach
    ?x needs("cow")
=> 
    eats("cow", "mouse", True)

foreach
    ?x needs("squirrel")
    needs("squirrel", "cow", True)
=> 
    not(needs("cow", "rabbit", True))

foreach
    eats("mouse", "rabbit", True)
    not(sees("rabbit", "mouse", True))
=> 
    is_green("rabbit", True)

foreach
    needs("cow", "rabbit", True)
=> 
    not(eats("rabbit", "mouse", True))

foreach
    ?x eats("squirrel")
    eats("squirrel", "cow", True)
=> 
    ?x needs("cow")

foreach
    ?x eats("mouse")
=> 
    ?x eats("squirrel")

# --- Query ---
query:
needs("rabbit", "cow", True)