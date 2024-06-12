def print_pattern(value):
    print("Input = " + str(value) + ":")
    if value % 2 == 0:
        print("Please input an odd number for the pattern.")
    else:
        counter = int((value-1)/2)
        for i in range(value):
            print("   " * abs(counter - i), end="")
            for j in range((2*min(i, value-i-1))+1):
                print("*", end="  ")
            print("")
    print("")


rows = int(input("Enter number of rows in pattern : "))
print_pattern(rows)
