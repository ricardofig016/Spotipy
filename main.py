import os, pygame, requests
from pytube import Search
from bs4 import BeautifulSoup

WIDTH = 675
HEIGHT = 262
WHITE = (254, 255, 254)
BLACK = (18, 18, 18)


def download_song(query) -> None:
    songs_path = "songs/"
    search = Search(query)
    video = search.results[0]

    audio_streams = video.streams.filter(only_audio=True)
    best_audio_stream = audio_streams.order_by("abr").desc().first()

    song_name = video.title.replace("/", "-")
    folder_path = os.path.join(songs_path, song_name)
    if not os.path.exists(folder_path):
        best_audio_stream.download(output_path=folder_path, filename="audio.mp4")
        thumbnail_url = video.thumbnail_url
        print("Audio downloaded sucssessfully.")
        download_thumbnail(thumbnail_url, folder_path)
        download_lyrics()
    else:
        print("Song already exists.")
    return


def download_thumbnail(url, path):
    response = requests.get(url)

    if response.status_code == 200:
        img_path = os.path.join(path, "thumbnail.jpg")
        with open(img_path, "wb") as file:
            file.write(response.content)
            print("Thumbnail image downloaded successfully.")
    else:
        print("Failed to download thumbnail image.")
    return


def download_lyrics():
    return


def load_thumbnail(song_path):
    img_path = os.path.join(song_path, "thumbnail.jpg")
    image = pygame.image.load(img_path)
    return pygame.transform.scale(image, (200, 112))


def load_icon():
    return


def blit_icons(screen):
    path = "icons/"
    icons = os.listdir(path)
    for icon in icons:
        pass
    # screen.blit(icon, (0, 150))
    return


def draw_line_separations(screen, color):
    pygame.draw.line(screen, color, (0, 75), (WIDTH, 75), 2)
    pygame.draw.line(screen, color, (0, 150), (WIDTH, 150), 2)
    pygame.draw.line(screen, color, (200, 150), (200, HEIGHT), 2)


def blit_text(screen, text, font_size, x, y, color, bg_color=None, align=None) -> None:
    """
    Args:
        align (str, optional): Can be "left", "right", "top", "bottom", "center". Defaults to None.
    """
    font = pygame.font.Font(size=font_size)
    text_surface = font.render(text, True, color, bg_color)

    if align == "left":
        align_mult = (0, -0.5)
    elif align == "right":
        align_mult = (-1, -0.5)
    elif align == "top":
        align_mult = (-0.5, 0)
    elif align == "bottom":
        align_mult = (-0.5, -1)
    elif align == "center":
        align_mult = (-0.5, -0.5)
    else:
        align_mult = (0, 0)

    screen.blit(
        text_surface,
        (
            int(x + text_surface.get_width() * align_mult[0]),
            int(y + text_surface.get_height() * align_mult[1]),
        ),
    )
    return


def blit_title(screen, title):
    font = pygame.font.Font(size=30)
    text_surface = font.render(title, True, WHITE, None)
    if text_surface.get_width() <= 440:
        blit_text(screen, title, 30, 220, 206, WHITE, align="left")
    else:
        middle = len(title) // 2
        left_space = title.rfind(" ", 0, middle)
        right_space = title.find(" ", middle)
        if abs(middle - left_space) < abs(right_space - middle):
            split_index = left_space
        else:
            split_index = right_space
        title_first_half = title[:split_index].strip()
        title_second_half = title[split_index:].strip()

        blit_text(screen, title_first_half, 30, 220, 187, WHITE, align="left")
        blit_text(screen, title_second_half, 30, 220, 224, WHITE, align="left")
    return


def song_window(song_path):
    thumbnail = load_thumbnail(song_path)
    title = os.path.basename(song_path)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SpotiPy")
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        screen.blit(thumbnail, (0, 150))
        blit_icons(screen)
        blit_title(screen, title)
        draw_line_separations(screen, WHITE)

        pygame.display.update()
        clock.tick(30)
    pygame.quit()
    return


def lyric_window(song_path):
    return


if __name__ == "__main__":
    files = os.listdir("songs/")
    first_file_path = os.path.join("songs/", os.listdir("songs/")[1])

    song_window(first_file_path)
    download_song("i really want to stay at your house")
    # download_song("vinland saga season2 op1")
