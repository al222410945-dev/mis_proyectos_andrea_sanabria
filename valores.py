valores = [True, False]

cantidad = int(input("Cuantas proposiciones quieres evaluar "))

if cantidad == 2:
    print("P \t Q \t P and Q")

    for P in valores:
        for Q in valores:
            resultado = P and Q
            print(P, "\t", Q, "\t", resultado)

elif cantidad == 3:
    print("P \t Q \t R \t P and Q and R")

    for P in valores:
        for Q in valores:
            for R in valores:
                resultado = P and Q and R
                print(P, "\t", Q, "\t", R, "\t", resultado)

elif cantidad == 4:
    print("P \t Q \t R \t S \t P and Q and R and S")

    for P in valores:
        for Q in valores:
            for R in valores:
                for S in valores:
                    resultado = P and Q and R and S
                    print(P, "\t", Q, "\t", R, "\t", S, "\t", resultado)