import numpy as np
import os

path = "stats/task_matrix/"
output_path = "stats/task_matrix/eigenvalues/"
jordan_check_output_path = "stats/task_matrix/jordan_check/"

os.makedirs(output_path, exist_ok=True)
os.makedirs(jordan_check_output_path, exist_ok=True)

def extract_block(matrix, start_row, end_row, start_col, end_col):
    return matrix[start_row:end_row, start_col:end_col]

def is_jordan_block(block):
    n = block.shape[0]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            elif i == j - 1:
                if block[i, j] != 1:
                    return False
            else:
                if block[i, j] != 0:
                    return False
    return True

def is_jordan_matrix(matrix):
    if matrix.shape[0] != matrix.shape[1]:
        return False

    n = matrix.shape[0]
    block_start = 0

    while block_start < n:
        block_size = 1
        while block_start + block_size < n and matrix[block_start + block_size - 1, block_start + block_size] == 1:
            block_size += 1

        block = extract_block(matrix, block_start, block_start + block_size, block_start, block_start + block_size)
        
        if not is_jordan_block(block):
            return False
        
        block_start += block_size
    
    return True

jordan_check_results = {}

for file in os.listdir(path):
    if file.endswith(".npy"):
        full_path = os.path.join(path, file)
        print(f"Processing file: {full_path}")
        matrix = np.load(full_path)
        
        is_jordan = is_jordan_matrix(matrix)
        jordan_check_results[file] = is_jordan
        
        eigenvalues = np.linalg.eigvals(matrix)
        output_file = os.path.join(output_path, f"eigenvalues_{file}")
        np.save(output_file, eigenvalues)

jordan_check_output_file = os.path.join(jordan_check_output_path, "jordan_check_results.txt")
with open(jordan_check_output_file, 'w') as f:
    for file, is_jordan in jordan_check_results.items():
        f.write(f"{file}: {'Jordan matrix' if is_jordan else 'Not a Jordan matrix'}\n")

print(f"Jordan matrix check results saved to: {jordan_check_output_file}")