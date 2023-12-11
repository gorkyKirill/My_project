package main

import (
	"fmt"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) < 4 {
		fmt.Println("Использование: калькулятор <число1> <операция> <число2>")
		os.Exit(1)
	}

	num1, err1 := strconv.ParseFloat(os.Args[1], 64)
	num2, err2 := strconv.ParseFloat(os.Args[3], 64)

	if err1 != nil || err2 != nil {
		fmt.Println("Ошибка ввода чисел")
		os.Exit(1)
	}

	operation := os.Args[2]
	result := 0.0

	switch operation {
	case "+":
		result = num1 + num2
	case "-":
		result = num1 - num2
	case "*":
		result = num1 * num2
	case "/":
		if num2 != 0 {
			result = num1 / num2
		} else {
			fmt.Println("Деление на ноль невозможно")
			os.Exit(1)
		}
	default:
		fmt.Println("Неподдерживаемая операция:", operation)
		os.Exit(1)
	}

	fmt.Printf("Результат: %.2f\n", result)
}
