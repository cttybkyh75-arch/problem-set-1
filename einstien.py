def main():
    m=float(input("m: "))
    C=300000000
    print(f"E: {E(m):.2e}")


def E(m):
    C=300000000
    return (m*(C**2))

main()
