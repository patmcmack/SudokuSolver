'''
Solve puzzles from Sudoku.com
'''

from PIL import Image, ImageOps
# from pytesseract import pytesseract
import pyautogui
import cv2
import numpy as np
import time
import easyocr

reader = easyocr.Reader(['en'])

def readSudoku():

    pRegion = (370, 875, 500, 500)
    pLoc = np.full((9,9), np.nan, dtype='f,f') # screen location of each box

    img = pyautogui.screenshot(region=pRegion)
    img = ImageOps.grayscale(img)
    # img.show()

    data = np.array(img)
    puzzle = np.zeros((9,9))
    blockSize = round(data.shape[0]/9)
    gap = 8 # pixels gap to avoid grid lines

    for row in range(9):
        for col in range(9):

            # Crop region of interest 
            row0 = row*blockSize+gap
            row1 = row0+(blockSize-2*gap)
            col0 = col*blockSize+gap
            col1 = col0+(blockSize-2*gap)
            roi = data[row0:row1,col0:col1]
            # Image.fromarray(roi).show()

            # Record box screen location for later 
            x = pRegion[0]+row*blockSize+blockSize/2
            y = pRegion[1]+col*blockSize+blockSize/2
            pLoc[col][row] = (x,y)

            # Determine if there is a number in square 
            count = (roi<150).sum()
            if count >50:
                
                thresh, roi = cv2.threshold(roi, 150, 255, cv2.
                THRESH_BINARY)
                # Image.fromarray(roi).show()

                # Image recognition to read puzzle 
                img1 = Image.fromarray(roi)
                img1 = img1.resize((100,100), Image.LANCZOS)
                # ret = pytesseract.image_to_string(img1, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
                ret2 = reader.readtext(np.array(img1), allowlist='0123456789')

                # For some reason, number 9 isn't recognized
                # if ret == '\x0c':
                #     puzzle[row,col] = 9
                # else:
                #     puzzle[row,col] = int(ret[0])

                # EasyOCR can't recognize the number 7
                if len(ret2)>0:
                    puzzle[row,col] = int(ret2[0][1])
                else:
                    puzzle[row, col] = 7

    return puzzle, pLoc

def is_valid_move(board, row, col, num):
  # Check if the number is already in the row
  for i in range(9):
    if board[row][i] == num:
      return False

  # Check if the number is already in the column
  for i in range(9):
    if board[i][col] == num:
      return False

  # Check if the number is already in the 3x3 box
  box_row = (row // 3) * 3
  box_col = (col // 3) * 3
  for i in range(box_row, box_row + 3):
    for j in range(box_col, box_col + 3):
      if board[i][j] == num:
        return False

  return True

def find_empty_cell(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return -1, -1  # If there are no empty cells left, return -1

def solve_sudoku(board):
    # Find the next empty cell
    row, col = find_empty_cell(board)
    if row == -1:  # If there are no empty cells left, the puzzle is solved
        return True

    # Try each possible value for the empty cell
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            # Place the number in the empty cell
            board[row][col] = num

            # Recursively solve the puzzle
            if solve_sudoku(board):
                return True

            # If the puzzle cannot be solved with this number, remove it
            board[row][col] = 0

    # If none of the possible numbers work, backtrack
    return False

def inputSolution(unSolved, solution, pLoc):
    for row in range(9):
        for col in range(9):
            if unSolved[row][col]==0:
                
                # Click box of interest
                loc = pLoc[row][col]
                pyautogui.click(x=loc[0], y=loc[1])
                # time.sleep(.05)

                # Write number
                pyautogui.typewrite(str(int(solution[row][col])))
                # time.sleep(1)


if __name__ == "__main__":

    # Read Sudoku puzzle
    print('\n ------ Input -------\n')
    puzzle, pLoc = readSudoku()
    unSolved = puzzle.copy()
    print(puzzle)

    # Solve Sudoku
    print('\n ------ Solved puzzle -------\n')
    solution = solve_sudoku(puzzle)
    print(puzzle)
    print(solution)

    # Auto input solution to sudoku.com
    # print(pLoc)
    # pyautogui.displayMousePosition()
    if solution:
        inputSolution(unSolved, puzzle, pLoc)
    else:
        print("No solution found, issue with input")
