# --- Knowledge Engine Setup ---
import pyke

knowledge_engine = pyke.knowledge_engine.__class__('my_knowledge_base')

# --- Facts ---
facts:
    needs("cat", "dog")
    is_kind("dog")
    needs("dog", "rabbit")
    eats("rabbit", "dog")
    is_green("rabbit")
    chases("tiger", "rabbit")
    is_big("tiger")

# --- Rules ---
rules:
    # Rule 1: If something is nice and it eats the tiger then it needs the dog
    foreach
        ?x is_nice(?x) and eats(?x, "tiger")
    assert
        needs(?x, "dog")

    # Rule 2: If something chases the cat then it eats the cat
    foreach
        ?x chases("cat")
    assert
        eats(?x, "cat")

    # Rule 3: If the dog chases the tiger then the tiger needs the rabbit
    foreach
        "dog" chases("tiger")
    assert
        needs("tiger", "rabbit")

    # Rule 4: If the rabbit chases the tiger then the rabbit chases the cat
    foreach
        "rabbit" chases("tiger")
    assert
        chases("rabbit", "cat")

    # Rule 5: If something chases the cat then the cat is kind
    foreach
        ?x chases("cat")
    assert
        is_kind("cat")

    # Rule 6: If something eats the dog then it chases the cat
    foreach
        ?x eats("dog")
    assert
        chases(?x, "cat")

    # Rule 7: If something is rough then it eats the dog
    foreach
        ?x is_rough(?x)
    assert
        eats(?x, "dog")

    # Rule 8: If something is kind then it is rough
    foreach
        ?x is_kind(?x)
    assert
        is_rough(?x)

    # Rule 9: If something eats the rabbit and the rabbit is big then it is kind
    foreach
        ?x eats("rabbit") and is_big("rabbit")
    assert
        is_kind(?x)

# --- Query ---
query:
    not is_rough("cat")