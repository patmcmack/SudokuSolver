# SudokuSolver

This is a minimal effort boredom project

This script is intented to be used to read, solve and then input a sudoku puzzle from [sudoku.com](https://sudoku.com). The basic overview is as follows:

## Read puzzle
  - The hardest part is reading the problem from [sudoku.com](https://sudoku.com)
  - Reads puzzle from a screen shot, could not scrape from url
  - Currently was lazy and simply hardcoded the on-screen location of the puzzle. In an ideal work you could use ```cv2``` to do some pattern recognition to find it
  - The image is split into the 81 parts and OCR (opitcal character recognition) was used to identify the numbers in each block
    - ```easyOCR``` ended up working the best for this case, but more refining certainly could be done
      - ```easyOCR``` had issues resolving the number 7 for some reason
    - ```pytesseract``` was also tried, but it wasn't as sucessful 
  - The puzzle is formatted to a 9x9 ```numpy``` array
## Solve 
- Simple backtracking method 
  - No need for anything more complicated, solves in <1sec 
- See [here](https://medium.com/@techwithjulles/python-sudoku-solver-d034eedb2e8d) for source of my code for this part 
## Input solution
- Uses ```pyautogui``` to control the mouse and keyboard to input the solution 