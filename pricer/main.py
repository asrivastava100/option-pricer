from BSPricer import BSPricer

def main():
    c = BSPricer('call', 3/12, 100, 95, 0.5, 0.01)
    print(c.price_call())
if __name__=="__main__":
    main()