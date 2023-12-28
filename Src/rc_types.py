# import: std
from typing import TypeVar
# import: non-std

# import: locals

# const/globals
T = TypeVar("T")

type Elements[T] = list[T] # generic type alias


# main
def main():
    input_l = [1,2,3,4,5,6]
    input_2 = ['1','2','3','4','5','6']
    element_list = process_elements(input_l)
    element_list = process_elements(input_2)
    print(element_list)

# code blocks

def process_numbers(numbers: list[int]) -> list[int]:
    return [number + 1 for number in numbers]

def process_elements(elements: list[T]) -> list[T]:
    return [element for index, element in enumerate(elements) if index % 2 == 1]


# main-line logic
if __name__ == '__main__':
    main()