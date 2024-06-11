#!/bin/bash
#!Calculator.

echo "+(1), -(2), *(3), /(4)"
read selection

active=false

function_add () {
    echo "num 1 to add: "
    read input1

    echo "num 2 to add: "
    read input2

    echo "Result: $((input1 + input2))"
}

function_sub () {
    echo "num 1 to subtract: "
    read input1

    echo "num 2 to subtract: "
    read input2

    echo "Result: $((input1 - input2))"
}

function_mult () {
    echo "num 1 to multiply: "
    read input1

    echo "num 2 to multiply: "
    read input2

    echo "Result: $((input1 * input2))"
}

function_div () {
    echo "num 1 to divide: "
    read input1

    echo "num 2 to divide: "
    read input2

    echo "Result: $((input1 / input2))"
}

active=true

while [ "$active" == true ]; do

    if [ "$selection" == "1" ]; then
        function_add
    elif [ "$selection" == "2" ]; then
        function_sub
    elif [ "$selection" == "3" ]; then
        function_mult
    elif [ "$selection" == "4" ]; then
        function_div
    else
        echo "Invalid selection"
    fi

    echo "Run program again? (Y/N)"
    read answer

    if [ "$answer" == "Y" ]; then
        active=true
        echo "+(1), -(2), *(3), /(4)"
        read selection
    else
        active=false
    fi
done
