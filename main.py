import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Ukuran layar (misalnya, 540x540 piksel untuk grid 9x9)
screen_size = 540
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Sudoku Game")

# Warna dasar
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Puzzle contoh (0 berarti sel kosong)
initial_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
puzzle = [row[:] for row in initial_puzzle]  # Buat salinan untuk game

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

def is_valid(puzzle, row, col, num):
    # Cek baris
    for i in range(9):
        if puzzle[row][i] == num:
            return False

    # Cek kolom
    for i in range(9):
        if puzzle[i][col] == num:
            return False

    # Cek kotak 3x3
    box_start_row = (row // 3) * 3
    box_start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if puzzle[box_start_row + i][box_start_col + j] == num:
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
            if not game_won and selected_row != -1 and selected_col != -1:
                if event.unicode.isdigit() and event.unicode != '0':  # Cek input 1-9
                    num = int(event.unicode)
                    if is_valid(puzzle, selected_row, selected_col, num):
                        puzzle[selected_row][selected_col] = num

                        # Cek apakah sudah menang
                        if check_win(puzzle):
                            print("Selamat! Anda telah menyelesaikan Sudoku!")
                            game_won = True  # Update status game
                    else:
                        print("Angka tidak valid di posisi ini!")


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
