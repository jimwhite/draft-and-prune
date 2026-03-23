# PyKe program for animal relationships reasoning

facts:
    sees(cow, mouse, True)
    is_kind(cow, True)
    
    eats(mouse, cow, True)
    is_kind(mouse, True)
    needs(mouse, squirrel, True)
    
    eats(rabbit, mouse, True)
    is_not_blue(rabbit, True)
    
    is_not_blue(squirrel, True)
    is_green(squirrel, True)
    is_rough(squirrel, True)
    needs(squirrel, mouse, True)
    sees(squirrel, rabbit, True)
    
    # Explicit negation: rabbit does not see mouse
    sees(rabbit, mouse, False)

rules:
    # If something sees the cow then it sees the squirrel
    foreach sees($x, cow, True)
        assert sees($x, squirrel, True)
    
    # If something sees the rabbit then it eats the cow
    foreach sees($x, rabbit, True)
        assert eats($x, cow, True)
    
    # If something needs the cow then the cow eats the mouse
    foreach needs($x, cow, True)
        assert eats(cow, mouse, True)
    
    # If something needs the squirrel and the squirrel needs the cow then the cow does not need the rabbit
    foreach needs($x, squirrel, True)
        and needs(squirrel, cow, True)
        assert not needs(cow, rabbit, True)
    
    # If the mouse eats the rabbit and the rabbit does not see the mouse then the rabbit is green
    foreach eats(mouse, rabbit, True)
        and sees(rabbit, mouse, False)
        assert is_green(rabbit, True)
    
    # If the cow needs the rabbit then the rabbit does not eat the mouse
    foreach needs(cow, rabbit, True)
        assert not eats(rabbit, mouse, True)
    
    # If something eats the squirrel and the squirrel eats the cow then it needs the cow
    foreach eats($x, squirrel, True)
        and eats(squirrel, cow, True)
        assert needs($x, cow, True)
    
    # If something eats the mouse then it eats the squirrel
    foreach eats($x, mouse, True)
        assert eats($x, squirrel, True)

query:
    needs(rabbit, cow, True)