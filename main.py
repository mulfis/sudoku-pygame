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

# Loop utama
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Bersihkan layar
    screen.fill(WHITE)

    # Gambar grid
    draw_grid()

    # Update layar
    pygame.display.flip()


# Tutup Pygame
pygame.quit()
sys.exit()
