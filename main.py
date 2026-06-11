import tkinter as tk


WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
TRANSITION_MS = 1000
HOLD_MS = 2000
CONTENT_DELAY_MS = 1000
CHOICE_FADE_MS = 500
BUBBLE_FADE_MS = 500
DIALOG_DELAY_MS = 1000
CHOICE_DELAY_MS = 700
SETTINGS_PANEL_MS = 450
CONFIRM_MESSAGE_MS = 1000
FPS_MS = 16

APP_TITLE = "\ubbf8\ub140 \uc5f0\uc560 \uc2dc\ubbac\ub808\uc774\ud130"
TITLE_TEXT = "\ubbf8 \uc5f0 \uc2dc"
TITLE_HEART_TEXT = "\u2764\ufe0f"
START_TEXT = "\uc2dc\uc791\ud558\uae30"
SETTINGS_TEXT = "\uc124\uc815"
HOW_TO_PLAY_TEXT = "\ud50c\ub808\uc774 \ubc29\ubc95"
SETTINGS_TITLE_TEXT = "- \uc124\uc815 -"
HOW_TO_PLAY_TITLE_TEXT = "- \ud50c\ub808\uc774 \ubc29\ubc95 -"
HOW_TO_PLAY_BODY_TEXT = (
    '\ub2f9\uc2e0\uc740 \ud604\uc7ac "\ucf00\uc774" \ub77c \ubd88\ub9ac\ub294 '
    "\uc544\ub984\ub2e4\uc6b4 \uc778\ubb3c\uacfc \uc0ac\ub791\uc5d0 \ube60\uc84c\uc2b5\ub2c8\ub2e4.\n"
    "\uadf8\ub140 \ub610\ud55c \uc544\ubb34\ub798\ub3c4 \ub2f9\uc2e0\uc5d0\uac8c "
    "\uc57d\uac04\uc758 \ud638\uac10\uc774 \uc788\ub098 \ubcf4\uad70\uc694?\n"
    "\uadf8\ub140\uc758 \ub2f4\ud654\ub97c \uc798 \uc77d\uace0, "
    "\uc62c\ubc14\ub978 \uc120\ud0dd\uc9c0\ub97c \uc120\ud0dd\ud558\uc5ec\n"
    "\uadf8\ub140\uc758 \ud638\uac10\ub3c4\ub97c \uc62c\ub824\ubcf4\uc138\uc694!\n"
    "[ \ubaa8\ub4e0 \uc120\ud0dd\uc740 \ucde8\uc18c\uac00 \ubd88\uac00\ub2a5\ud558\ubbc0\ub85c, "
    "\uc2e0\uc911\ud558\uac8c \uacb0\uc815\ud574 \uc8fc\uc2dc\uae38 \ubc14\ub78d\ub2c8\ub2e4. "
    "\uc778\uc0dd\uc740 \ub3cc\uc774\ud0ac \uc218 \uc5c6\uc73c\ub2c8\uae4c\uc694! ]"
)
TEXT_SPEED_TEXT = "\ud14d\uc2a4\ud2b8 \ucd9c\ub825 \uc18d\ub3c4"
SLOW_TEXT = "\ub290\ub9ac\uac8c"
NORMAL_TEXT = "\ubcf4\ud1b5"
FAST_TEXT = "\ube60\ub974\uac8c"
KEI_TEXT = "dummy"
BUBBLE_READY_TEXT = "dummy :"
BUBBLE_DIALOG_GAP = "   "
DIALOG_TEXT = "\uc544, \uc548\ub155\ud558\uc138\uc694. \ub77c\uc6b0\ub2d8."
TEXT_SPEEDS = {
    "slow": ("\ub290\ub9ac\uac8c", 600),
    "normal": ("\ubcf4\ud1b5", 1000),
    "fast": ("\ube60\ub974\uac8c", 1700),
}


class MiyeonsiApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(800, 600)
        self.root.configure(bg="white")

        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.redraw)

        self.transition_rect = None
        self.is_transitioning = False
        self.screen = "title"
        self.choices_visible = False
        self.choice_label_visible = False
        self.waiting_for_choice_click = False
        self.choice_items = []
        self.choice_label = None
        self.bubble_text = BUBBLE_READY_TEXT
        self.bubble_color = "#000000"
        self.settings_open = False
        self.settings_animating = False
        self.settings_panel_x = None
        self.text_speed_key = "normal"
        self.settings_message = ""
        self.settings_message_after = None
        self.how_to_play_open = False
        self.how_to_play_animating = False
        self.how_to_play_panel_x = None

    def run(self):
        self.root.mainloop()

    def size(self):
        return self.canvas.winfo_width(), self.canvas.winfo_height()

    def redraw(self, event=None):
        if self.is_transitioning:
            return

        if self.screen == "dummy":
            self.draw_dummy_screen()
        else:
            self.draw_title_screen()

    def draw_title_screen(self):
        self.screen = "title"
        self.choices_visible = False
        self.choice_label_visible = False
        self.waiting_for_choice_click = False
        self.canvas.unbind("<Button-1>")
        self.bubble_text = BUBBLE_READY_TEXT
        self.bubble_color = "#000000"
        self.settings_open = False
        self.settings_animating = False
        self.settings_panel_x = None
        self.how_to_play_open = False
        self.how_to_play_animating = False
        self.how_to_play_panel_x = None
        self.root.configure(cursor="")

        width, height = self.size()
        self.canvas.delete("all")
        self.canvas.configure(bg="white")

        title_y = height * 0.34
        title_item = self.canvas.create_text(
            width / 2,
            title_y,
            text=TITLE_TEXT,
            fill="black",
            font=("Malgun Gothic", 72, "bold"),
            tags=("title_screen",),
        )
        title_bbox = self.canvas.bbox(title_item)
        heart_gap = 64
        right_heart_extra_gap = 34
        left_heart_x = title_bbox[0] - heart_gap
        right_heart_x = title_bbox[2] + heart_gap + right_heart_extra_gap
        self.canvas.create_text(
            left_heart_x,
            title_y,
            text=TITLE_HEART_TEXT,
            fill="black",
            font=("Malgun Gothic", 58, "bold"),
            tags=("title_screen",),
        )
        self.canvas.create_text(
            right_heart_x,
            title_y,
            text=TITLE_HEART_TEXT,
            fill="black",
            font=("Malgun Gothic", 58, "bold"),
            tags=("title_screen",),
        )

        button_width = 260
        button_height = 70
        side_button_width = 220
        button_gap = 34
        center_x1 = (width - button_width) / 2
        y1 = height * 0.68

        self.draw_title_button(
            center_x1,
            y1,
            button_width,
            button_height,
            START_TEXT,
            "start_button",
            font_size=28,
        )
        self.draw_title_button(
            center_x1 - button_gap - side_button_width,
            y1,
            side_button_width,
            button_height,
            HOW_TO_PLAY_TEXT,
            "how_to_play_button",
            font_size=24,
        )
        self.draw_title_button(
            center_x1 + button_width + button_gap,
            y1,
            side_button_width,
            button_height,
            SETTINGS_TEXT,
            "settings_button",
            font_size=24,
        )
        self.canvas.tag_bind("start_button", "<Button-1>", self.start_transition)
        self.canvas.tag_bind("settings_button", "<Button-1>", self.open_settings)
        self.canvas.tag_bind("how_to_play_button", "<Button-1>", self.open_how_to_play)
        self.canvas.tag_bind("start_button", "<Enter>", lambda _: self.root.configure(cursor="hand2"))
        self.canvas.tag_bind("start_button", "<Leave>", lambda _: self.root.configure(cursor=""))
        self.canvas.tag_bind("settings_button", "<Enter>", lambda _: self.root.configure(cursor="hand2"))
        self.canvas.tag_bind("settings_button", "<Leave>", lambda _: self.root.configure(cursor=""))
        self.canvas.tag_bind("how_to_play_button", "<Enter>", lambda _: self.root.configure(cursor="hand2"))
        self.canvas.tag_bind("how_to_play_button", "<Leave>", lambda _: self.root.configure(cursor=""))

        if self.settings_open and not self.settings_animating:
            self.draw_settings_panel(self.settings_target_x(width))
        if self.how_to_play_open and not self.how_to_play_animating:
            self.draw_how_to_play_panel(self.settings_target_x(width))

    def draw_title_button(self, x, y, width, height, text, tag, font_size):
        self.canvas.create_rectangle(
            x,
            y,
            x + width,
            y + height,
            fill="#f7f7f7",
            outline="#d8d8d8",
            width=2,
            tags=("title_screen", tag),
        )
        self.canvas.create_text(
            x + width / 2,
            y + height / 2,
            text=text,
            fill="black",
            font=("Malgun Gothic", font_size, "bold"),
            tags=("title_screen", tag),
        )

    def settings_size(self, width, height):
        return width * 0.68, height * 0.7

    def settings_target_x(self, width):
        panel_width, _ = self.settings_size(width, self.canvas.winfo_height())
        return (width - panel_width) / 2

    def open_settings(self, event=None):
        if (
            self.settings_open
            or self.settings_animating
            or self.how_to_play_open
            or self.how_to_play_animating
            or self.screen != "title"
        ):
            return

        self.root.configure(cursor="")
        self.settings_open = True
        self.settings_animating = True
        self.animate_settings(opening=True, start_time=None)

    def close_settings(self, event=None):
        if not self.settings_open or self.settings_animating:
            return

        self.root.configure(cursor="")
        self.settings_animating = True
        self.animate_settings(opening=False, start_time=None)

    def open_how_to_play(self, event=None):
        if (
            self.how_to_play_open
            or self.how_to_play_animating
            or self.settings_open
            or self.settings_animating
            or self.screen != "title"
        ):
            return

        self.root.configure(cursor="")
        self.how_to_play_open = True
        self.how_to_play_animating = True
        self.animate_how_to_play(opening=True, start_time=None)

    def close_how_to_play(self, event=None):
        if not self.how_to_play_open or self.how_to_play_animating:
            return

        self.root.configure(cursor="")
        self.how_to_play_animating = True
        self.animate_how_to_play(opening=False, start_time=None)

    def animate_settings(self, opening, start_time):
        now = self.root.tk.call("clock", "milliseconds")
        if start_time is None:
            start_time = now

        elapsed = now - start_time
        progress = min(elapsed / SETTINGS_PANEL_MS, 1)
        eased = self.ease_out_cubic(progress)

        width, height = self.size()
        panel_width, _ = self.settings_size(width, height)
        start_x = width + 8
        end_x = (width - panel_width) / 2

        if opening:
            x = start_x + (end_x - start_x) * eased
        else:
            x = end_x + (start_x - end_x) * eased

        self.settings_panel_x = x
        self.draw_settings_panel(x)

        if progress < 1:
            self.root.after(FPS_MS, lambda: self.animate_settings(opening, start_time))
        else:
            self.settings_animating = False
            if opening:
                self.settings_panel_x = end_x
                self.draw_settings_panel(end_x)
            else:
                self.settings_open = False
                self.settings_panel_x = None
                self.canvas.delete("settings_panel")

    def animate_how_to_play(self, opening, start_time):
        now = self.root.tk.call("clock", "milliseconds")
        if start_time is None:
            start_time = now

        elapsed = now - start_time
        progress = min(elapsed / SETTINGS_PANEL_MS, 1)
        eased = self.ease_out_cubic(progress)

        width, height = self.size()
        panel_width, _ = self.settings_size(width, height)
        start_x = -panel_width - 8
        end_x = (width - panel_width) / 2

        if opening:
            x = start_x + (end_x - start_x) * eased
        else:
            x = end_x + (start_x - end_x) * eased

        self.how_to_play_panel_x = x
        self.draw_how_to_play_panel(x)

        if progress < 1:
            self.root.after(FPS_MS, lambda: self.animate_how_to_play(opening, start_time))
        else:
            self.how_to_play_animating = False
            if opening:
                self.how_to_play_panel_x = end_x
                self.draw_how_to_play_panel(end_x)
            else:
                self.how_to_play_open = False
                self.how_to_play_panel_x = None
                self.canvas.delete("how_to_play_panel")

    def draw_settings_panel(self, x):
        width, height = self.size()
        panel_width, panel_height = self.settings_size(width, height)
        y = (height - panel_height) / 2
        title_y = y + 54
        center_x = x + panel_width / 2

        self.canvas.delete("settings_panel")
        self.canvas.create_rectangle(
            x,
            y,
            x + panel_width,
            y + panel_height,
            fill="white",
            outline="black",
            width=4,
            tags=("settings_panel",),
        )
        self.canvas.create_text(
            center_x,
            title_y,
            text=SETTINGS_TITLE_TEXT,
            fill="black",
            font=("Malgun Gothic", 26, "bold"),
            tags=("settings_panel",),
        )
        divider_y = title_y + 54
        self.canvas.create_line(
            x + 28,
            divider_y,
            x + panel_width - 28,
            divider_y,
            fill="black",
            width=3,
            tags=("settings_panel",),
        )

        close_size = 42
        close_x1 = center_x + 110
        close_y1 = title_y - close_size / 2
        self.canvas.create_rectangle(
            close_x1,
            close_y1,
            close_x1 + close_size,
            close_y1 + close_size,
            fill="white",
            outline="black",
            width=2,
            tags=("settings_panel", "settings_close"),
        )
        self.canvas.create_text(
            close_x1 + close_size / 2,
            close_y1 + close_size / 2,
            text="X",
            fill="black",
            font=("Malgun Gothic", 20, "bold"),
            tags=("settings_panel", "settings_close"),
        )

        label_y = divider_y + 86
        option_y = label_y + 78
        self.canvas.create_text(
            center_x,
            label_y,
            text=TEXT_SPEED_TEXT,
            fill="black",
            font=("Malgun Gothic", 24, "bold"),
            tags=("settings_panel",),
        )
        slow_weight = "bold" if self.text_speed_key == "slow" else "normal"
        normal_weight = "bold" if self.text_speed_key == "normal" else "normal"
        fast_weight = "bold" if self.text_speed_key == "fast" else "normal"

        self.canvas.create_text(
            center_x - 120,
            option_y,
            text=SLOW_TEXT,
            fill="black",
            font=("Malgun Gothic", 20, slow_weight),
            tags=("settings_panel", "speed_slow"),
        )
        self.canvas.create_text(
            center_x,
            option_y,
            text=NORMAL_TEXT,
            fill="black",
            font=("Malgun Gothic", 20, normal_weight),
            tags=("settings_panel", "speed_normal"),
        )
        self.canvas.create_text(
            center_x + 120,
            option_y,
            text=FAST_TEXT,
            fill="black",
            font=("Malgun Gothic", 20, fast_weight),
            tags=("settings_panel", "speed_fast"),
        )

        if self.settings_message:
            self.canvas.create_text(
                center_x,
                option_y + 56,
                text=self.settings_message,
                fill="black",
                font=("Malgun Gothic", 18),
                tags=("settings_panel",),
            )

        self.canvas.tag_raise("settings_panel")
        self.canvas.tag_bind("settings_close", "<Button-1>", self.close_settings)
        self.canvas.tag_bind("settings_close", "<Enter>", lambda _: self.root.configure(cursor="hand2"))
        self.canvas.tag_bind("settings_close", "<Leave>", lambda _: self.root.configure(cursor=""))
        self.canvas.tag_bind("speed_slow", "<Button-1>", lambda _: self.select_text_speed("slow"))
        self.canvas.tag_bind("speed_normal", "<Button-1>", lambda _: self.select_text_speed("normal"))
        self.canvas.tag_bind("speed_fast", "<Button-1>", lambda _: self.select_text_speed("fast"))
        for tag in ("speed_slow", "speed_normal", "speed_fast"):
            self.canvas.tag_bind(tag, "<Enter>", lambda _: self.root.configure(cursor="hand2"))
            self.canvas.tag_bind(tag, "<Leave>", lambda _: self.root.configure(cursor=""))

    def draw_how_to_play_panel(self, x):
        width, height = self.size()
        panel_width, panel_height = self.settings_size(width, height)
        y = (height - panel_height) / 2
        title_y = y + 54
        center_x = x + panel_width / 2

        self.canvas.delete("how_to_play_panel")
        self.canvas.create_rectangle(
            x,
            y,
            x + panel_width,
            y + panel_height,
            fill="white",
            outline="black",
            width=4,
            tags=("how_to_play_panel",),
        )
        self.canvas.create_text(
            center_x,
            title_y,
            text=HOW_TO_PLAY_TITLE_TEXT,
            fill="black",
            font=("Malgun Gothic", 26, "bold"),
            tags=("how_to_play_panel",),
        )
        divider_y = title_y + 54
        self.canvas.create_line(
            x + 28,
            divider_y,
            x + panel_width - 28,
            divider_y,
            fill="black",
            width=3,
            tags=("how_to_play_panel",),
        )

        close_size = 42
        close_x1 = center_x + 170
        close_y1 = title_y - close_size / 2
        self.canvas.create_rectangle(
            close_x1,
            close_y1,
            close_x1 + close_size,
            close_y1 + close_size,
            fill="white",
            outline="black",
            width=2,
            tags=("how_to_play_panel", "how_to_play_close"),
        )
        self.canvas.create_text(
            close_x1 + close_size / 2,
            close_y1 + close_size / 2,
            text="X",
            fill="black",
            font=("Malgun Gothic", 20, "bold"),
            tags=("how_to_play_panel", "how_to_play_close"),
        )
        body_margin = 48
        self.canvas.create_text(
            x + body_margin,
            divider_y + 42,
            text=HOW_TO_PLAY_BODY_TEXT,
            anchor="nw",
            fill="black",
            font=("Malgun Gothic", 18),
            width=panel_width - body_margin * 2,
            tags=("how_to_play_panel",),
        )

        self.canvas.tag_raise("how_to_play_panel")
        self.canvas.tag_bind("how_to_play_close", "<Button-1>", self.close_how_to_play)
        self.canvas.tag_bind("how_to_play_close", "<Enter>", lambda _: self.root.configure(cursor="hand2"))
        self.canvas.tag_bind("how_to_play_close", "<Leave>", lambda _: self.root.configure(cursor=""))

    def select_text_speed(self, speed_key):
        self.text_speed_key = speed_key
        label, _ = TEXT_SPEEDS[speed_key]
        self.settings_message = f"{label} \uc18d\ub3c4\uac00 \uc124\uc815\ub428!"

        if self.settings_message_after is not None:
            self.root.after_cancel(self.settings_message_after)

        if self.settings_panel_x is not None:
            self.draw_settings_panel(self.settings_panel_x)

        self.settings_message_after = self.root.after(CONFIRM_MESSAGE_MS, self.clear_settings_message)

    def clear_settings_message(self):
        self.settings_message = ""
        self.settings_message_after = None
        if self.settings_open and self.settings_panel_x is not None:
            self.draw_settings_panel(self.settings_panel_x)

    def draw_dummy_screen(self):
        self.canvas.delete("all")
        self.canvas.configure(bg="white")
        self.draw_dummy_text()
        if self.choice_label_visible:
            self.draw_choice_label(self.bubble_text, self.bubble_color)
        if self.choices_visible:
            self.draw_choices(outline="#000000")
        self.draw_game_close_button()

    def draw_dummy_text(self):
        width, height = self.size()
        separator_y = self.choice_area_top(height)
        label_divider_y = self.choice_label_divider_y(height)

        self.canvas.delete("game_frame")
        self.canvas.delete("dummy_text")

        self.canvas.create_rectangle(
            2,
            2,
            width - 2,
            height - 2,
            outline="black",
            width=4,
            tags=("game_frame",),
        )
        self.canvas.create_line(
            2,
            separator_y,
            width - 2,
            separator_y,
            fill="black",
            width=4,
            tags=("game_frame",),
        )
        self.canvas.create_line(
            2,
            label_divider_y,
            width - 2,
            label_divider_y,
            fill="black",
            width=4,
            tags=("game_frame",),
        )

        self.canvas.create_text(
            width / 2,
            separator_y / 2,
            text=KEI_TEXT,
            fill="black",
            font=("Malgun Gothic", 64, "bold"),
            tags=("dummy_text",),
        )
        self.draw_game_close_button()

    def draw_game_close_button(self):
        width, _ = self.size()
        button_size = 44
        margin = 18
        x1 = width - margin - button_size
        y1 = margin

        self.canvas.delete("game_close")
        self.canvas.create_rectangle(
            x1,
            y1,
            x1 + button_size,
            y1 + button_size,
            fill="white",
            outline="black",
            width=2,
            tags=("game_close",),
        )
        self.canvas.create_text(
            x1 + button_size / 2,
            y1 + button_size / 2,
            text="X",
            fill="black",
            font=("Malgun Gothic", 20, "bold"),
            tags=("game_close",),
        )
        self.canvas.tag_raise("game_close")
        self.canvas.tag_bind("game_close", "<Button-1>", self.return_to_title)
        self.canvas.tag_bind("game_close", "<Enter>", lambda _: self.root.configure(cursor="hand2"))
        self.canvas.tag_bind("game_close", "<Leave>", lambda _: self.root.configure(cursor=""))

    def return_to_title(self, event=None):
        self.is_transitioning = False
        self.choices_visible = False
        self.choice_label_visible = False
        self.waiting_for_choice_click = False
        self.transition_rect = None
        self.draw_title_screen()

    def choice_area_top(self, height):
        return height - min(190, height * 0.28)

    def choice_label_divider_y(self, height):
        return self.choice_area_top(height) + min(58, height * 0.075)

    def draw_choice_label(self, text, fill):
        width, height = self.size()
        separator_y = self.choice_area_top(height)
        side_margin = max(28, width * 0.035)

        self.canvas.delete("choice_label")

        self.choice_label = self.canvas.create_text(
            side_margin + 4,
            separator_y + 28,
            text=text,
            anchor="w",
            fill=fill,
            font=("Malgun Gothic", 20),
            tags=("choice_label",),
        )

    def draw_choices(self, outline="#000000"):
        width, height = self.size()
        self.canvas.delete("choices")
        self.choice_items = []

        label_divider_y = self.choice_label_divider_y(height)
        side_margin = max(28, width * 0.035)
        column_gap = max(36, width * 0.055)
        row_gap = max(16, height * 0.022)
        choice_width = (width - side_margin * 2 - column_gap) / 2
        choice_height = min(32, height * 0.043)
        start_x = side_margin
        start_y = label_divider_y + 22

        for index in range(4):
            row = index // 2
            column = index % 2
            x1 = start_x + column * (choice_width + column_gap)
            y1 = start_y + row * (choice_height + row_gap)
            x2 = x1 + choice_width
            y2 = y1 + choice_height
            item = self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill="#ffffff",
                outline=outline,
                width=2,
                tags=("choices",),
            )
            self.choice_items.append(item)

    def start_transition(self, event=None):
        if (
            self.is_transitioning
            or self.settings_open
            or self.settings_animating
            or self.how_to_play_open
            or self.how_to_play_animating
        ):
            return

        self.is_transitioning = True
        self.root.configure(cursor="")
        self.canvas.tag_unbind("start_button", "<Button-1>")
        self.animate_cover(start_time=None)

    def ease_out_cubic(self, value):
        return 1 - pow(1 - value, 3)

    def animate_cover(self, start_time):
        now = self.root.tk.call("clock", "milliseconds")
        if start_time is None:
            start_time = now

        elapsed = now - start_time
        progress = min(elapsed / TRANSITION_MS, 1)
        eased = self.ease_out_cubic(progress)

        width, height = self.size()
        rect_width = width * 1.1
        x1 = width - rect_width * eased
        x2 = x1 + rect_width

        if self.transition_rect is None:
            self.transition_rect = self.canvas.create_rectangle(
                x1,
                0,
                x2,
                height,
                fill="black",
                outline="black",
                tags=("transition",),
            )
        else:
            self.canvas.coords(self.transition_rect, x1, 0, x2, height)

        self.canvas.tag_raise("transition")

        if progress < 1:
            self.root.after(FPS_MS, lambda: self.animate_cover(start_time))
        else:
            self.screen = "dummy"
            self.choices_visible = False
            self.choice_label_visible = False
            self.waiting_for_choice_click = False
            self.bubble_text = BUBBLE_READY_TEXT
            self.bubble_color = "#000000"
            self.canvas.delete("title_screen")
            self.draw_dummy_text()
            self.canvas.tag_raise("transition")
            self.root.after(HOLD_MS, lambda: self.animate_uncover(start_time=None))

    def animate_uncover(self, start_time):
        now = self.root.tk.call("clock", "milliseconds")
        if start_time is None:
            start_time = now

        elapsed = now - start_time
        progress = min(elapsed / TRANSITION_MS, 1)
        reversed_eased = 1 - self.ease_out_cubic(progress)

        width, height = self.size()
        rect_width = width * 1.1
        x1 = width - rect_width * reversed_eased
        x2 = x1 + rect_width

        self.canvas.coords(self.transition_rect, x1, 0, x2, height)
        self.canvas.tag_raise("transition")

        if progress < 1:
            self.root.after(FPS_MS, lambda: self.animate_uncover(start_time))
        else:
            self.canvas.delete("transition")
            self.transition_rect = None
            self.is_transitioning = False
            self.root.after(CONTENT_DELAY_MS, self.show_choice_label)

    def show_choice_label(self):
        if self.screen != "dummy":
            return

        self.choice_label_visible = True
        self.bubble_text = BUBBLE_READY_TEXT
        self.bubble_color = "#ffffff"
        self.draw_choice_label(self.bubble_text, self.bubble_color)
        self.fade_bubble(start_time=None)

    def fade_bubble(self, start_time):
        if self.screen != "dummy":
            return

        now = self.root.tk.call("clock", "milliseconds")
        if start_time is None:
            start_time = now

        elapsed = now - start_time
        progress = min(elapsed / BUBBLE_FADE_MS, 1)
        channel = round(255 + (0 - 255) * progress)
        self.bubble_color = f"#{channel:02x}{channel:02x}{channel:02x}"

        if self.choice_label is not None:
            self.canvas.itemconfigure(self.choice_label, fill=self.bubble_color)

        if progress < 1:
            self.root.after(FPS_MS, lambda: self.fade_bubble(start_time))
        else:
            self.bubble_color = "#000000"
            self.root.after(DIALOG_DELAY_MS, lambda: self.type_dialog(index=0))

    def type_dialog(self, index):
        if self.screen != "dummy":
            return

        self.bubble_text = BUBBLE_READY_TEXT + BUBBLE_DIALOG_GAP + DIALOG_TEXT[:index]
        if self.choice_label is not None:
            self.canvas.itemconfigure(self.choice_label, text=self.bubble_text, fill="#000000")

        if index < len(DIALOG_TEXT):
            self.root.after(self.type_interval_ms(), lambda: self.type_dialog(index + 1))
        else:
            self.root.after(CHOICE_DELAY_MS, self.start_choice_fade)

    def type_interval_ms(self):
        _, speed = TEXT_SPEEDS[self.text_speed_key]
        return max(1, round(60000 / speed))

    def start_choice_fade(self, event=None):
        if self.screen != "dummy" or self.choices_visible:
            return

        self.waiting_for_choice_click = False
        self.choices_visible = True
        self.canvas.unbind("<Button-1>")
        self.draw_choices(outline="#ffffff")
        self.fade_choices(start_time=None)

    def fade_choices(self, start_time):
        if self.screen != "dummy":
            return

        now = self.root.tk.call("clock", "milliseconds")
        if start_time is None:
            start_time = now

        elapsed = now - start_time
        progress = min(elapsed / CHOICE_FADE_MS, 1)
        channel = round(255 + (0 - 255) * progress)
        outline = f"#{channel:02x}{channel:02x}{channel:02x}"

        for item in self.choice_items:
            self.canvas.itemconfigure(item, outline=outline)

        if progress < 1:
            self.root.after(FPS_MS, lambda: self.fade_choices(start_time))


if __name__ == "__main__":
    app = MiyeonsiApp()
    app.run()
