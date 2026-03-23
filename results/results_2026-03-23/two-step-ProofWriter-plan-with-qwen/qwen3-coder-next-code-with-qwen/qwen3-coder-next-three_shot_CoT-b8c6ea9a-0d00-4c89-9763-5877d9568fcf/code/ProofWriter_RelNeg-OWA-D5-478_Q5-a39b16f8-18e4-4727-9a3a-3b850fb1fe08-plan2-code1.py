# --- Facts ---
facts:
is_kind("cow", True, True)
sees("cow", "mouse", True)
eats("mouse", "cow", True)
is_kind("mouse", True, True)
needs("mouse", "squirrel", True)
eats("rabbit", "mouse", True)
is_blue("rabbit", False, True)
is_blue("squirrel", False, True)
is_green("squirrel", True, True)
is_rough("squirrel", True, True)
needs("squirrel", "mouse", True)
sees("squirrel", "rabbit", True)

# --- Rules ---
rules:
foreach
    ?x sees("cow", True)
=> 
    ?x sees("squirrel", True)

foreach
    ?x sees("rabbit", True)
=> 
    ?x eats("cow", True)

foreach
    ?x needs("cow", True)
=>
    eats("cow", "mouse", True)

foreach
    ?x needs("squirrel", True)
    needs("squirrel", "cow", True)
=>
    not(needs("cow", "rabbit", True))

foreach
    eats("mouse", "rabbit", True)
    not(sees("rabbit", "mouse", True))
=>
    is_green("rabbit", True, True)

foreach
    needs("cow", "rabbit", True)
=>
    not(eats("rabbit", "mouse", True))

foreach
    ?x eats("squirrel", True)
    eats("squirrel", "cow", True)
=>
    needs(?x, "cow", True)

foreach
    ?x eats("mouse", True)
=>
    ?x eats("squirrel", True)

# --- Query ---
query:
needs("rabbit", "cow", True)