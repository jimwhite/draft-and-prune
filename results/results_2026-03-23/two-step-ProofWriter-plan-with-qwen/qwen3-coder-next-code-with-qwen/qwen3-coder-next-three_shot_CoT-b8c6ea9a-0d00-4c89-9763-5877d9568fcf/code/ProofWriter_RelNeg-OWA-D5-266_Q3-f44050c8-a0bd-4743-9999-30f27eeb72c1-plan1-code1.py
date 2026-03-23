from pyke import knowledge_engine

# Create knowledge base instance
engine = knowledge_engine.engine(__file__)

Facts:
    is_rough(bald_eagle, True)
    eats(bald_eagle, cow, True)
    sees(cow, bald_eagle, True)
    visits(cow, bald_eagle, True)
    visits(cow, lion, True)
    is_round(cow, True)
    is_rough(dog, True)
    is_young(lion, True)
    sees(lion, cow, True)

Rules:
    # If someone is green and they eat the bald eagle then the bald eagle is not rough.
    rule(green_and_eats_bald_eagle_not_rough):
        foreach
            is_green(person, True)
            eats(person, bald_eagle, True)
        then
            is_rough(bald_eagle, False)

    # If someone is big and they do not see the bald eagle then the bald eagle is rough.
    rule(big_and_not_see_bald_eagle_rough):
        foreach
            is_big(person, True)
            not sees(person, bald_eagle, True)
        then
            is_rough(bald_eagle, True)

    # If someone is big then they visit the dog.
    rule(big_visits_dog):
        foreach
            is_big(person, True)
        then
            visits(person, dog, True)

    # If someone eats the lion and they are big then the lion eats the dog.
    rule(eats_lion_and_big_eats_dog):
        foreach
            eats(person, lion, True)
            is_big(person, True)
        then
            eats(lion, dog, True)

    # If someone visits the dog then the dog eats the cow.
    rule(visits_dog_eats_cow):
        foreach
            visits(person, dog, True)
        then
            eats(dog, cow, True)

    # If someone is rough and they eat the cow then they are young.
    rule(rough_and_eats_cow_is_young):
        foreach
            is_rough(person, True)
            eats(person, cow, True)
        then
            is_young(person, True)

    # If the lion eats the cow then the lion visits the bald eagle.
    rule(lion_eats_cow_visits_bald_eagle):
        foreach
            eats(lion, cow, True)
        then
            visits(lion, bald_eagle, True)

    # If someone is big and they see the lion then they are green.
    rule(big_and_sees_lion_is_green):
        foreach
            is_big(person, True)
            sees(person, lion, True)
        then
            is_green(person, True)

    # If someone is young then they are big.
    rule(young_is_big):
        foreach
            is_young(person, True)
        then
            is_big(person, True)

Query:
    is_big(lion, True)