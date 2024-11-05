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
puzzle = [
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

# Variabel untuk menyimpan posisi sel yang dipilih
selected_row = -1
selected_col = -1


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


# Loop utama
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            selected_row = y // 60
            selected_col = x // 60
        elif event.type == pygame.KEYDOWN:
            if selected_row != -1 and selected_col != -1:
                if event.unicode.isdigit() and event.unicode != '0':  # Cek input 1-9
                    puzzle[selected_row][selected_col] = int(event.unicode)


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


    # Update layar
    pygame.display.flip()


# Tutup Pygame
pygame.quit()
sys.exit()
