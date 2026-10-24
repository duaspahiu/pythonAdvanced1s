
import streamlit as st

def kalkulo(num1, num2, operations):
    if operations == "Mbledhje":
        result = num1 + num2
    elif operations == "Zbritje":
        result = num1 - num2
    elif operations == "Shumëzim":
        result = num1 * num2
    else:
        result = num1 / num2

    return result


def main():

    st.title("Simple Calculator")

    num1 = st.number_input("Shëno vlerën e parë")
    num2 = st.number_input("Shëno vlerën e dytë")

    operations = st.radio(
        "Zgjidh një veprim",
        ["Mbledhje", "Zbritje", "Shumëzim", "Pjesëtim"]
    )

    if st.button("Llogarit"):
        result = kalkulo(num1, num2, operations)
        st.write("Rezultati:", result)


if __name__ == "__main__":
    main()
