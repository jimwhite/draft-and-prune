# --- Facts ---
def facts():
    yield "is_furry", "Anne", True
    yield "is_furry", "Bob", True
    yield "is_blue", "Gary", True
    yield "is_cold", "Gary", True
    yield "is_furry", "Gary", True
    yield "is_quiet", "Gary", True
    yield "is_round", "Gary", True
    yield "is_blue", "Harry", True
    yield "is_cold", "Harry", True
    yield "is_quiet", "Harry", True
    yield "is_round", "Harry", True
    yield "is_young", "Harry", True

# --- Rules ---
def rules():
    # Cold, blue things are quiet.
    yield ["is_cold", "$x", True], ["is_blue", "$x", True], ["is_quiet", "$x", True]
    
    # All round, furry things are quiet.
    yield ["is_round", "$x", True], ["is_furry", "$x", True], ["is_quiet", "$x", True]
    
    # If Bob is blue and Bob is round then Bob is young.
    yield ["is_blue", "Bob", True], ["is_round", "Bob", True], ["is_young", "Bob", True]
    
    # If something is round then it is blue.
    yield ["is_round", "$x", True], ["is_blue", "$x", True]
    
    # If something is young and round then it is blue.
    yield ["is_young", "$x", True], ["is_round", "$x", True], ["is_blue", "$x", True]
    
    # If Harry is quiet and Harry is furry then Harry is blue.
    yield ["is_quiet", "Harry", True], ["is_furry", "Harry", True], ["is_blue", "Harry", True]
    
    # Furry things are cold.
    yield ["is_furry", "$x", True], ["is_cold", "$x", True]
    
    # Cold things are round.
    yield ["is_cold", "$x", True], ["is_round", "$x", True]
    
    # If something is young and furry then it is rough.
    yield ["is_young", "$x", True], ["is_furry", "$x", True], ["is_rough", "$x", True]

# --- Query ---
def query():
    yield "is_furry", "Harry", True