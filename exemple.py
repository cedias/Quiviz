import quiviz

# importing quiviz does x things:
#
#   1) Creates the shared state within the script ()
#   2) Auto starts text logger to save in X
#

def main():

    for i in range(15):
        #logged function
        do(i)
    
    return


@quiviz.log #we bind the logger to this function's returned dict
def do(i):
    return {"i":i}


if __name__ == '__main__':
    main()



