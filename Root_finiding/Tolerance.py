def error(a,b):
    delta = abs(b-a)
    return (delta/a)*100

if __name__ == "__main__":
    print(f"Error: {error(5,2.5)}%")