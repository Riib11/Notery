def log( tag , msg ):

    def check(s): return s == tag

    if   check( "msg" ):   print( "[#]" , msg )
    elif check( "error" ): print( "[!]" , msg )
    elif check( "log" ):   print( "[>]" , msg )
    else:                  print( "[%]" , msg )