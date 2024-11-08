import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar (misalnya, 540x540 piksel untuk grid 9x9)
screen_size = 540
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Sudoku Game")

# Warna dasar
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def generate_sudoku():
    # Buat papan kosong
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    
    # Angka yang akan digunakan diacak
    numbers = list(range(1, 10))
    random.shuffle(numbers)

    # Isi baris pertama dengan angka acak
    for col in range(9):
        puzzle[0][col] = numbers[col]
    
    # Isi papan secara rekursif
    fill_puzzle(puzzle)
    return puzzle

def is_valid(puzzle, row, col, num):
    # Cek baris
    for c in range(9):
        if puzzle[row][c] == num:
            return False
    
    # Cek kolom
    for r in range(9):
        if puzzle[r][col] == num:
            return False
    
    # Cek kotak 3x3
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for r in range(3):
        for c in range(3):
            if puzzle[box_row_start + r][box_col_start + c] == num:
                return False
    
    return True

def fill_puzzle(puzzle):
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:  # Temukan sel kosong
                # Coba angka dari 1 hingga 9
                for num in range(1, 10):
                    if is_valid(puzzle, row, col, num):
                        puzzle[row][col] = num  # Tempatkan angka
                        if fill_puzzle(puzzle):  # Rekursi
                            return True
                        puzzle[row][col] = 0  # Kembali jika tidak berhasil
                return False
    return True  # Jika semua sel terisi
    
def can_solve(puzzle):
    # Cek apakah ada solusi untuk puzzle yang diberikan
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(puzzle, row, col, num):
                        puzzle[row][col] = num
                        if can_solve(puzzle):
                            return True
                        puzzle[row][col] = 0  # Kembali jika tidak berhasil
                return False  # Jika tidak ada angka valid yang bisa digunakan
    return True  # Jika semua sel terisi

def remove_numbers(puzzle, num_to_remove=40):
    attempts = num_to_remove
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle[row][col] != 0:
            backup = puzzle[row][col]
            puzzle[row][col] = 0  # Hapus angka sementara
            
            # Salin puzzle untuk pengujian
            puzzle_copy = [r[:] for r in puzzle]
            
            # Pastikan puzzle masih bisa diselesaikan dan memiliki solusi tunggal
            if not has_unique_solution(puzzle_copy) or not can_solve(puzzle_copy):
                puzzle[row][col] = backup  # Kembalikan angka jika solusi tidak unik
            else:
                attempts -= 1
                
    return puzzle

def solve_and_count(puzzle, count=0):
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(puzzle, row, col, num):
                        puzzle[row][col] = num
                        count = solve_and_count(puzzle, count)
                        puzzle[row][col] = 0
                        if count > 1:  # Lebih dari satu solusi
                            return count
                return count  # Jika tidak ada solusi, kembalikan count sekarang
    return count + 1  # Menambah count ketika solusi ditemukan

def has_unique_solution(puzzle):
    return solve_and_count(puzzle) == 1

def shuffle_board(puzzle):
    # Fungsi untuk mengacak baris dan kolom dalam blok 3x3
    for i in range(0, 9, 3):
        rows = [i, i + 1, i + 2]
        cols = [i, i + 1, i + 2]
        random.shuffle(rows)
        random.shuffle(cols)

        # Tukar baris dan kolom secara acak dalam blok 3x3
        puzzle[rows[0]], puzzle[rows[1]], puzzle[rows[2]] = (
            puzzle[rows[1]], puzzle[rows[2]], puzzle[rows[0]]
        )
        for row in range(9):
            puzzle[row][cols[0]], puzzle[row][cols[1]], puzzle[row][cols[2]] = (
                puzzle[row][cols[1]], puzzle[row][cols[2]], puzzle[row][cols[0]]
            )
    return puzzle

# Puzzle contoh (0 berarti sel kosong)
initial_puzzle = generate_sudoku()
initial_puzzle = shuffle_board(initial_puzzle)
puzzle = remove_numbers(initial_puzzle, num_to_remove=40)

# Variabel untuk menyimpan posisi sel yang dipilih
selected_row = -1
selected_col = -1
game_won = False

# Fungsi untuk menggambar grid
def draw_grid():
    # Menggambar garis-garis grid
    for i in range(10):  # Menggambar 10 garis untuk membuat grid 9x9
        # Garis tebal untuk batas utama
        line_width = 4 if i % 3 == 0 else 1

        # Garis vertikal
        pygame.draw.line(screen, BLACK, (i * 60, 0), (i * 60, screen_size), line_width)
        # Garis horizontal
        pygame.draw.line(screen, BLACK, (0, i * 60), (screen_size, i * 60), line_width)

# Pengaturan font untuk angka
font = pygame.font.Font(None, 40)

# Fungsi untuk menggambar angka di grid
def draw_numbers():
    for row in range(9):
        for col in range(9):
            num = puzzle[row][col]
            if num != 0:  # Jika angka bukan 0, tampilkan
                text = font.render(str(num), True, BLACK)
                screen.blit(text, (col * 60 + 20, row * 60 + 15))

def draw_selected_cell():
    if selected_row != -1 and selected_col != -1:  # Jika ada sel yang dipilih
        pygame.draw.rect(
            screen, (0, 255, 0),  # Warna hijau
            (selected_col * 60, selected_row * 60, 60, 60), 3  # Posisi dan ukuran kotak
        )

def display_win_message():
    if game_won:
        font = pygame.font.Font(None, 60)
        text = font.render("Selamat, Anda menang!", True, (0, 128, 0))
        text_rect = text.get_rect(center=(300, 300))  # Posisikan di tengah layar
        screen.blit(text, text_rect)

def check_win(puzzle):
    for row in range(9):
        for col in range(9):
            num = puzzle[row][col]
            # Cek apakah ada sel kosong atau angka tidak valid
            if num == 0 or not is_valid(puzzle, row, col, num):
                return False
    return True

def reset_game():
    global puzzle, game_won, selected_row, selected_col
    puzzle = [row[:] for row in initial_puzzle]  # Salin ulang puzzle awal
    game_won = False  # Set game_won ke False
    selected_row = -1  # Hapus pilihan sel
    selected_col = -1
    print("Game di-reset. selected_row dan selected_col di-reset ke -1.")

def draw_reset_button():
    font = pygame.font.Font(None, 40)
    text = font.render("Reset", True, (255, 255, 255))
    text_rect = text.get_rect(center=(300, 580))  # Posisikan di bawah grid

    # Gambar kotak tombol
    pygame.draw.rect(screen, (0, 0, 255), (200, 550, 200, 60))  # Kotak biru
    screen.blit(text, text_rect)

    return pygame.Rect(200, 550, 200, 60)  # Kembalikan objek tombol

# Loop utama
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Cek apakah klik berada di tombol Reset
            if reset_button.collidepoint(pos):
                reset_game()
                print("Tombol Reset diklik.")
            
            # Jika game belum selesai dan klik bukan di tombol Reset, cek pilihan sel
            elif not game_won:
                selected_row = pos[1] // 60
                selected_col = pos[0] // 60

        elif event.type == pygame.KEYDOWN:
        # Logika input keyboard
            if not game_won and selected_row != -1 and selected_col != -1:
                if event.unicode.isdigit() and event.unicode != '0':  # Cek input 1-9
                    num = int(event.unicode)
                    # Cek validitas angka yang dimasukkan
                    if puzzle[selected_row][selected_col] == 0 or puzzle[selected_row][selected_col] != num:
                        if is_valid(puzzle, selected_row, selected_col, num):
                            puzzle[selected_row][selected_col] = num
                            if check_win(puzzle):
                                print("Selamat! Anda telah menyelesaikan Sudoku!")
                                game_won = True
                        else:
                            print("Angka tidak valid di posisi ini!")
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    # Hapus angka di sel yang dipilih
                    puzzle[selected_row][selected_col] = 0

        if event.type == pygame.QUIT:
            running = False

    # Bersihkan layar
    screen.fill(WHITE)

    # Gambar grid
    draw_grid()

    # Gambar angka
    draw_numbers()

    # Gambar sel yang dipilih
    draw_selected_cell()

    # Tampilkan pesan kemenangan jika sudah menang
    display_win_message()

    # Gambar tombol Reset
    reset_button = draw_reset_button()

    # Update layar
    pygame.display.flip()

# Tutup Pygame
pygame.quit()
sys.exit()
