from tkinter import font as tkfont


TRANSITION_MS = 1000
HOLD_MS = 2000
CONTENT_DELAY_MS = 1000
CHOICE_FADE_MS = 500
BUBBLE_FADE_MS = 500
DIALOG_DELAY_MS = 1000
CHOICE_DELAY_MS = 700
FPS_MS = 16

KEI_TEXT = "dummy"
SCENE_LABEL_TEXT = "\uc7a5\uba74 1"
BUBBLE_FONT = ("Malgun Gothic", 20)
KEI_SPEECH_LABEL_TEXT = "dummy :"
BUBBLE_READY_TEXT = KEI_SPEECH_LABEL_TEXT
BUBBLE_DIALOG_GAP = "   "
BUBBLE_DIALOG_GAP_PX = 12
DIALOG_TEXT = (
    "...\ub2a6\uc5c8\uc796\uc544\uc694. \uadf8\uac83\ub3c4 2\ubd84! "
    "\ub2f9\uc2e0\uc740... \uc5b4\uc9f8\uc11c \ud56d\uc0c1 "
    "\ub2a6\ub294 \uac81\ub2c8\uae4c?"
)
TEXT_SPEEDS = {
    "slow": ("\ub290\ub9ac\uac8c", 600),
    "normal": ("\ubcf4\ud1b5", 1000),
    "fast": ("\ube60\ub974\uac8c", 1700),
}


class GameSceneMixin:
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
        self.draw_scene_label()
        self.draw_game_close_button()

    def draw_scene_label(self):
        x1 = 18
        y1 = 18
        label_width = 112
        label_height = 38

        self.canvas.delete("scene_label")
        self.canvas.create_rectangle(
            x1,
            y1,
            x1 + label_width,
            y1 + label_height,
            fill="white",
            outline="black",
            width=2,
            tags=("scene_label",),
        )
        self.canvas.create_text(
            x1 + label_width / 2,
            y1 + label_height / 2,
            text=SCENE_LABEL_TEXT,
            fill="black",
            font=("Malgun Gothic", 16, "bold"),
            tags=("scene_label",),
        )

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
        self.choice_label = None
        self.choice_dialog_label = None
        self.transition_rect = None
        self.draw_title_screen()

    def choice_area_top(self, height):
        return height - min(250, height * 0.36)

    def choice_label_divider_y(self, height):
        dialog_height = min(112, max(90, height * 0.15))
        return self.choice_area_top(height) + dialog_height

    def choice_label_geometry(self):
        width, height = self.size()
        separator_y = self.choice_area_top(height)
        label_divider_y = self.choice_label_divider_y(height)
        side_margin = max(28, width * 0.035)
        font = tkfont.Font(font=BUBBLE_FONT)
        line_height = font.metrics("linespace")
        text_left = side_margin + 4
        text_right = width - side_margin - 4
        name_x = text_left
        center_y = (separator_y + label_divider_y) / 2
        dialog_x = name_x + font.measure(BUBBLE_READY_TEXT) + BUBBLE_DIALOG_GAP_PX
        dialog_width = max(120, text_right - dialog_x)
        return name_x, center_y, dialog_x, dialog_width, line_height

    def split_bubble_text(self, text):
        if text.startswith(BUBBLE_READY_TEXT):
            return BUBBLE_READY_TEXT, text[len(BUBBLE_READY_TEXT) :].lstrip()

        return BUBBLE_READY_TEXT, text.lstrip()

    def draw_choice_label(self, text, fill):
        name_x, center_y, dialog_x, dialog_width, line_height = self.choice_label_geometry()
        name_text, dialog_text = self.split_bubble_text(text)

        self.canvas.delete("choice_label")

        self.choice_label = self.canvas.create_text(
            name_x,
            center_y,
            text=name_text,
            anchor="w",
            fill=fill,
            font=BUBBLE_FONT,
            tags=("choice_label",),
        )
        self.choice_dialog_label = None

        if dialog_text:
            formatted_dialog_text = self.format_bubble_text(dialog_text, dialog_width)
            dialog_y = self.centered_dialog_y(formatted_dialog_text, center_y, line_height)
            self.choice_dialog_label = self.canvas.create_text(
                dialog_x,
                dialog_y,
                text=formatted_dialog_text,
                anchor="nw",
                fill=fill,
                font=BUBBLE_FONT,
                width=dialog_width,
                tags=("choice_label",),
            )

    def centered_dialog_y(self, text, center_y, line_height):
        line_count = max(1, text.count("\n") + 1)
        return center_y - (line_count * line_height) / 2

    def format_bubble_text(self, text, max_width):
        font = tkfont.Font(font=BUBBLE_FONT)
        lines = []
        current_line = ""

        for character in text:
            if character == "\n":
                lines.append(current_line.rstrip())
                current_line = ""
                continue

            current_line += character
            if current_line and font.measure(current_line) > max_width:
                break_index = current_line.rfind(" ")
                if break_index > 0:
                    lines.append(current_line[:break_index].rstrip())
                    current_line = current_line[break_index + 1 :].lstrip()
                else:
                    lines.append(current_line[:-1].rstrip())
                    current_line = character.lstrip()

        if current_line or not lines:
            lines.append(current_line.rstrip())

        return "\n".join(lines)

    def draw_choices(self, outline="#000000"):
        width, height = self.size()
        self.canvas.delete("choices")
        self.choice_items = []

        label_divider_y = self.choice_label_divider_y(height)
        side_margin = 3
        column_gap = 0
        row_gap = 0
        top_margin = 3
        bottom_margin = 6
        choice_width = (width - side_margin * 2 - column_gap) / 2
        start_y = label_divider_y + top_margin
        available_height = max(64, height - bottom_margin - start_y)
        choice_height = (available_height - row_gap) / 2
        start_x = side_margin

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
        self.draw_choice_label(self.bubble_text, "#000000")

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
