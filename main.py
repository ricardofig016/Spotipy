import os, subprocess, random, pygame, pytube, pydub, requests, shutil, bs4

WIDTH = 750
HEIGHT = 262

WHITE = (254, 255, 254)
GRAY = (18, 18, 18)
BLACK = (0, 0, 0)

shuffled_pl = False
stamp_sec = 0


def convert_mp4_to_wav(input_file, output_wav_file):
    # Run FFmpeg command to convert audio to WAV
    command = f"ffmpeg -i '{input_file}' -q:a 0 -map a '{output_wav_file}'"
    subprocess.run(command, shell=True)
    return


def normalize_audio(song_path):
    audio = pydub.AudioSegment.from_wav(song_path)
    normalized_audio = audio.normalize()
    normalized_audio.export(song_path, format="wav")
    return


def download_song_from_querry(query) -> None:
    search = pytube.Search(query)
    video = search.results[0]
    print("First result from querry:", video.watch_url)
    download_song_from_url(video.watch_url)
    return


def download_song_from_url(url) -> None:
    video = pytube.YouTube(url)

    audio_streams = video.streams.filter(only_audio=True)
    best_audio_stream = audio_streams.order_by("abr").desc().first()

    songs_path = "songs/"
    print(video.title)
    song_name = video.title.replace("/", "-")
    print(song_name)
    folder_path = os.path.join(songs_path, song_name)
    if not os.path.exists(folder_path):
        best_audio_stream.download(output_path=folder_path, filename="audio.mp4")
        convert_mp4_to_wav(
            os.path.join(folder_path, "audio.mp4"),
            os.path.join(folder_path, "audio.wav"),
        )
        normalize_audio(os.path.join(folder_path, "audio.wav"))
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
    print("Not yet implemented.")
    return


def load_thumbnail(song_path):
    img_path = os.path.join(song_path, "thumbnail.jpg")
    image = pygame.image.load(img_path)
    return pygame.transform.scale(image, (200, 112))


def load_icon(icon_path):
    icon_img = pygame.image.load(icon_path)
    return pygame.transform.scale(icon_img, (75, 75))


def blit_icons_song_window(screen, shuffle: bool, loop: bool, paused: bool):
    path = "icons/"
    icons = []
    if shuffle:
        icons.append("shuffle_activated_icon.jpg")
    else:
        icons.append("shuffle_deactivated_icon.jpg")
    if loop:
        icons.append("loop_song_activated_icon.jpg")
    else:
        icons.append("loop_song_deactivated_icon.jpg")
    icons.append("lyrics_window_icon.jpg")
    icons.append("previous_song_icon.jpg")
    if paused:
        icons.append("play_icon.jpg")
    else:
        icons.append("pause_icon.jpg")
    icons.append("next_song_icon.jpg")
    icons.append("rename_icon.jpg")
    icons.append("search_icon.jpg")
    icons.append("add_song_icon.jpg")
    icons.append("delete_song_icon.jpg")

    for i in range(len(icons)):
        icon_path = os.path.join(path, icons[i])
        icon_img = load_icon(icon_path)
        screen.blit(icon_img, (75 * i, 0))
    return


def blit_icon_keys_song_window(screen):
    keys = ["X", "L", "v", "<", "P", ">", "R", "S", "A", "D"]
    for i in range(len(keys)):
        blit_text(screen, keys[i], 32, 75 * i + 37, 112, WHITE, align="center")
    return


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


def blit_title_song_window(screen, title):
    font_size = 30
    font = pygame.font.Font(size=font_size)
    text_surface = font.render(title, True, WHITE, None)
    if text_surface.get_width() <= 515:
        blit_text(screen, title, font_size, 220, 206, WHITE, align="left")
    else:
        middle = len(title) // 2
        split_index = title.rfind(" ", 0, middle)
        title_first_half = title[:split_index].strip()
        title_second_half = title[split_index:].strip()

        blit_text(screen, title_first_half, font_size, 220, 187, WHITE, align="left")
        blit_text(screen, title_second_half, font_size, 220, 224, WHITE, align="left")
    return


def blit_time_song_window(screen, song_path):
    time = f"{get_elapsed_time()} / {get_total_time(song_path)}"
    blit_text(screen, time, 24, 190, 246, WHITE, GRAY, "right")


def draw_lines_song_window(screen, color):
    pygame.draw.line(screen, color, (0, 75), (WIDTH, 75), 2)
    pygame.draw.line(screen, color, (0, 150), (WIDTH, 150), 2)
    pygame.draw.line(screen, color, (225, 0), (225, 150), 2)
    pygame.draw.line(screen, color, (450, 0), (450, 150), 2)
    pygame.draw.line(screen, color, (200, 150), (200, HEIGHT), 2)


def get_next_song_path(curr_song_path, shuffle, loop) -> str:
    global stamp_sec
    stamp_sec = 0
    if loop:
        return curr_song_path
    curr_song = os.path.basename(curr_song_path)
    dir = os.path.dirname(curr_song_path)
    if shuffle:
        global shuffled_pl
        if not shuffled_pl:
            shuffled_pl = os.listdir(dir)
            random.shuffle(shuffled_pl)
        songs = shuffled_pl
    else:
        songs = os.listdir(dir)
        songs.sort()
    curr_song_index = songs.index(curr_song)
    if curr_song_index == len(songs) - 1:
        return os.path.join(dir, songs[0])
    return os.path.join(dir, songs[curr_song_index + 1])


def get_previous_song_path(curr_song_path, shuffle) -> str:
    global stamp_sec
    stamp_sec = 0
    curr_song = os.path.basename(curr_song_path)
    dir = os.path.dirname(curr_song_path)
    if shuffle:
        global shuffled_pl
        if not shuffled_pl:
            shuffled_pl = os.listdir(dir)
            random.shuffle(shuffled_pl)
        songs = shuffled_pl
    else:
        songs = os.listdir(dir)
        songs.sort()
    curr_song_index = songs.index(curr_song)
    if curr_song_index == 0:
        return os.path.join(dir, songs[len(songs) - 1])
    return os.path.join(dir, songs[curr_song_index - 1])


def rename_song(song_path):
    curr_song_name = os.path.basename(song_path)
    songs_path = os.path.dirname(song_path)
    display_song_name = ""
    if len(curr_song_name) > 20:
        display_song_name = curr_song_name[:17] + "..."
    else:
        display_song_name = curr_song_name
    text_for_input = curr_song_name
    while True:
        new_song_name = text_input_window(
            f'Rename "{display_song_name}"', text_for_input
        )
        if new_song_name not in os.listdir(songs_path):
            os.rename(song_path, os.path.join(songs_path, new_song_name))
            print("Song successfully renamed.")
            break
        elif new_song_name == curr_song_name:
            print("Renaming cancelled.")
            break
        else:
            text_for_input = new_song_name
            print("There is already a song with this name.")
    return os.path.join(songs_path, new_song_name)


def search_song():
    print("Not yet implemented")
    return


def add_song():
    print("Not yet implemented")
    return


def delete_song():
    print("Not yet implemented")
    return


def play_song(song_path, paused, start_time=0):
    pygame.mixer.music.stop()
    audio_wav_path = os.path.join(song_path, "audio.wav")
    pygame.mixer.music.load(audio_wav_path)
    pygame.mixer.music.play(start=start_time)
    if paused:
        pygame.mixer.music.pause()
    return


def set_elapsed_time(song_path, stamp, paused):
    if not stamp in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        print("Invalid timestamp:", stamp)
        return

    global stamp_sec
    audio = pygame.mixer.Sound(os.path.join(song_path, "audio.wav"))
    total_sec = audio.get_length()
    jump = total_sec / 10
    stamp_sec = jump * stamp

    play_song(song_path, paused, stamp_sec)
    return


def convert_sec_to_min(t_sec: float) -> str:
    min = int(t_sec / 60)
    sec = int(t_sec % 60)
    if sec < 10:
        sec = f"0{sec}"
    return f"{min}:{sec}"


def get_elapsed_time() -> str:
    global stamp_sec
    elapsed_sec = pygame.mixer.music.get_pos() / 1000.0 + stamp_sec
    return convert_sec_to_min(elapsed_sec)


def get_total_time(song_path):
    audio = pygame.mixer.Sound(os.path.join(song_path, "audio.wav"))
    total_sec = audio.get_length()
    return convert_sec_to_min(total_sec)


def song_window(song_path, shuffle: bool, loop: bool, paused: bool):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    caption = "SpotiPy"
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    thumbnail = load_thumbnail(song_path)
    title = os.path.basename(song_path)
    play_song(song_path, paused)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # quit
                if event.key == pygame.K_ESCAPE:
                    running = False
                # toggle shuffle
                if event.key == pygame.K_x:
                    shuffle = not shuffle
                # toggle loop
                if event.key == pygame.K_l:
                    loop = not loop
                # go to lyrics window
                if event.key == pygame.K_DOWN:
                    lyrics_window(song_path)
                # previous song
                if event.key == pygame.K_LEFT:
                    song_path = get_previous_song_path(song_path, shuffle)
                    thumbnail = load_thumbnail(song_path)
                    title = os.path.basename(song_path)
                    play_song(song_path, paused)
                # pause / unpause
                if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                # next song
                if event.key == pygame.K_RIGHT:
                    song_path = get_next_song_path(song_path, shuffle, loop)
                    thumbnail = load_thumbnail(song_path)
                    title = os.path.basename(song_path)
                    play_song(song_path, paused)
                # rename song
                if event.key == pygame.K_r:
                    song_path = rename_song(song_path)
                    title = os.path.basename(song_path)
                    pygame.display.set_caption(caption)
                # search song
                if event.key == pygame.K_s:
                    search_song()
                # add song
                if event.key == pygame.K_a or event.key == pygame.K_PLUS:
                    add_song()
                # delete song
                if event.key == pygame.K_d or event.key == pygame.K_MINUS:
                    delete_song()
                # go to timestamp
                if event.key in [
                    pygame.K_0,
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4,
                    pygame.K_5,
                    pygame.K_6,
                    pygame.K_7,
                    pygame.K_8,
                    pygame.K_9,
                ]:
                    set_elapsed_time(song_path, event.key - 48, paused)
            if event.type == pygame.QUIT:
                running = False

        screen.fill(GRAY)
        screen.blit(thumbnail, (0, 150))
        blit_icons_song_window(screen, shuffle, loop, paused)
        blit_icon_keys_song_window(screen)
        blit_title_song_window(screen, title)
        blit_time_song_window(screen, song_path)
        draw_lines_song_window(screen, WHITE)

        if not pygame.mixer.music.get_busy() and not paused:
            print("Song finished playing.")
            song_path = get_next_song_path(song_path, shuffle, loop)
            thumbnail = load_thumbnail(song_path)
            title = os.path.basename(song_path)
            play_song(song_path, paused)

        pygame.display.update()
        clock.tick(60)
    return


def lyrics_window(song_path):
    print("Not yet implemented.")
    return


def draw_lines_text_input_window(screen, color):
    pygame.draw.line(
        screen, color, (20, HEIGHT // 2 - 40), (WIDTH - 20, HEIGHT // 2 - 40), 2
    )
    pygame.draw.line(
        screen, color, (20, HEIGHT // 2 + 40), (WIDTH - 20, HEIGHT // 2 + 40), 2
    )
    pygame.draw.line(screen, color, (20, HEIGHT // 2 - 40), (20, HEIGHT // 2 + 40), 2)
    pygame.draw.line(
        screen, color, (WIDTH - 20, HEIGHT // 2 - 40), (WIDTH - 20, HEIGHT // 2 + 40), 2
    )


def blit_text_text_input_window(screen, text):
    font_size = 28
    font = pygame.font.Font(size=font_size)
    text_surface = font.render(text, True, WHITE, None)
    if text_surface.get_width() <= 600:
        blit_text(
            screen, text, font_size, WIDTH // 2, HEIGHT // 2, WHITE, align="center"
        )
    else:
        middle = len(text) // 2
        split_index = text.rfind(" ", 0, middle)
        text_first_half = text[:split_index].strip()
        text_second_half = text[split_index:].strip()

        blit_text(
            screen,
            text_first_half,
            font_size,
            WIDTH // 2,
            HEIGHT // 2 - 13,
            WHITE,
            align="center",
        )
        blit_text(
            screen,
            text_second_half,
            font_size,
            WIDTH // 2,
            HEIGHT // 2 + 13,
            WHITE,
            align="center",
        )
    return


def text_input_window(caption: str, text: str = "") -> str:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    init_text = text
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if text:
                        text = ""
                    else:
                        running = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_RETURN:
                    return text
                elif event.unicode:
                    if len(text) <= 120:
                        text += event.unicode
            if event.type == pygame.QUIT:
                running = False
        screen.fill(GRAY)
        blit_text_text_input_window(screen, text)
        draw_lines_text_input_window(screen, WHITE)

        pygame.display.update()
        clock.tick(60)
    return init_text


if __name__ == "__main__":
    pygame.init()

    # text_input_window(
    #    "trr",
    #    "LAKSHD FLAKSJDHF ALKDSJF HALKJD HFLKAJDS FLKADSJ HFLKAJDS HFLKASDJ HFLKASHDF ALKDS FHLKSADJHF",
    # )

    files = os.listdir("songs/")
    files.sort()
    some_song_path = os.path.join("songs/", files[0])
    song_window(some_song_path, False, False, True)

    # download_song_from_querry("Dawid Podsiadło - Let You Down (Lyrics) cyberpunk")
    # download_song_from_url("https://www.youtube.com/watch?v=o94gVQeP6PQ")
    # download_song_from_url("https://www.youtube.com/watch?v=6jrllECbLfA")
    # download_song_from_url("https://www.youtube.com/watch?v=ll7Su_BCNCA")
    # download_song_from_url("https://www.youtube.com/watch?v=0YT3NTiZKDw")

    pygame.quit()
