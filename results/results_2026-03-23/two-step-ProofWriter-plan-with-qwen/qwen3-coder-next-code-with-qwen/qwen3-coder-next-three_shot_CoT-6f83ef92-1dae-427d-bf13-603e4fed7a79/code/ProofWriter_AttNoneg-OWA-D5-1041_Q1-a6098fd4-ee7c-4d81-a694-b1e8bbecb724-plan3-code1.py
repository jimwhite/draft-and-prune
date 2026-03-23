# Facts about entities
is_cold("Bob", True)
is_quiet("Bob", True)
is_red("Bob", True)
is_smart("Bob", True)

is_kind("Charlie", True)
is_quiet("Charlie", True)
is_red("Charlie", True)
is_rough("Charlie", True)

is_cold("Dave", True)
is_kind("Dave", True)
is_smart("Dave", True)

is_quiet("Fiona", True)

# Rules for inference
quiet_and_cold_is_smart:
    foreach
        is_quiet($thing, True)
        is_cold($thing, True)
    assert
        is_smart($thing, True)

red_and_cold_are_round:
    foreach
        is_red($thing, True)
        is_cold($thing, True)
    assert
        is_round($thing, True)

kind_and_rough_is_red:
    foreach
        is_kind($thing, True)
        is_rough($thing, True)
    assert
        is_red($thing, True)

quiet_are_rough:
    foreach
        is_quiet($thing, True)
    assert
        is_rough($thing, True)

cold_and_smart_is_red:
    foreach
        is_cold($thing, True)
        is_smart($thing, True)
    assert
        is_red($thing, True)

rough_is_cold:
    foreach
        is_rough($thing, True)
    assert
        is_cold($thing, True)

red_are_rough:
    foreach
        is_red($thing, True)
    assert
        is_rough($thing, True)

dave_smart_and_kind_is_quiet:
    foreach
        is_smart("Dave", True)
        is_kind("Dave", True)
    assert
        is_quiet("Dave", True)

# Query to evaluate: Is Charlie kind?
is_kind("Charlie", True)