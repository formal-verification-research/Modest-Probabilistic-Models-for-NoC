import batch_detail.args as arg

def batch():
    # parse args
    args = arg.parse()
    if args is None:
        return
    
    # generate simulation specification 
    # run simulations

if __name__ == "__main__":
    batch()