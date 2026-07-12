"""
Subtitle mask.

Controls:
- Left drag: move
- Edge drag: resize
- Hold left mouse button: temporary transparent
- Hold Z key: same as hold left mouse button (temporary transparent)
- Double right-click: close
"""

import ctypes
import sys
import tkinter as tk

MASK_COLOR = '#000000'
MASK_ALPHA = 1.0
DRAG_ALPHA = 0.35
DEFAULT_HEIGHT = 110
BOTTOM_GAP = 0


def enable_dpi_awareness():
    if sys.platform != 'win32':
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def get_screen_size(root):
    return root.winfo_screenwidth(), root.winfo_screenheight()


class SubtitleBlocker:
    canvas = None
    drag_data = None
    height = None
    original_alpha = None
    resize_data = None
    resize_threshold = None
    right_click_timer = None
    root = None
    width = None
    x = None
    y = None

    def __init__(self):
        enable_dpi_awareness()

        self.root = tk.Tk()
        self.root.title('Subtitle Mask')
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', MASK_ALPHA)
        self.root.overrideredirect(True)
        self.root.configure(bg=MASK_COLOR)

        self.original_alpha = MASK_ALPHA

        screen_width, screen_height = get_screen_size(self.root)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = screen_width
        self.height = DEFAULT_HEIGHT
        self.x = 0
        self.y = max(0, screen_height - self.height - BOTTOM_GAP)

        self.canvas = tk.Canvas(
            self.root,
            bg=MASK_COLOR,
            highlightthickness=0,
            bd=0,
            relief='flat',
        )
        self.canvas.pack(fill='both', expand=True)

        self.set_geometry()

        self.drag_data = {'x': 0, 'y': 0, 'dragging': False}
        self.resize_data = {'resizing': False, 'edge': None}
        self.resize_threshold = 12
        self.right_click_timer = None
        self.z_pressed = False  # 追踪 Z 键是否按下

        self.canvas.bind('<Button-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.canvas.bind('<Button-3>', self.on_right_click)
        self.canvas.bind('<Motion>', self.on_motion)

        # === 全局 Z 键轮询（无需窗口焦点） ===
        self.poll_z_key()

    def set_geometry(self):
        self.root.geometry(
            f"{int(self.width)}x{int(self.height)}+{int(self.x)}+{int(self.y)}"
        )
        self.root.update_idletasks()

    def keep_above_taskbar_hotspot(self):
        _, screen_height = get_screen_size(self.root)
        max_y = max(0, screen_height - self.height - BOTTOM_GAP)
        if self.y > max_y:
            self.y = max_y

    def constrain_horizontal(self):
        """限制遮挡条的左右边界不能移出屏幕"""
        screen_width, _ = get_screen_size(self.root)

        # 左边界不能小于 0
        if self.x < 0:
            self.x = 0

        # 右边界不能超出屏幕宽度
        right_edge = self.x + self.width
        if right_edge > screen_width:
            self.x = screen_width - self.width

    def on_press(self, event):
        self.root.attributes('-alpha', DRAG_ALPHA)
        edge = self.get_edge(event.x, event.y)

        if edge:
            self.resize_data = {
                'resizing': True,
                'edge': edge,
                'start_x': event.x_root,
                'start_y': event.y_root,
                'start_width': self.width,
                'start_height': self.height,
                'start_window_x': self.x,
                'start_window_y': self.y,
            }
        else:
            self.drag_data['dragging'] = True
            self.drag_data['x'] = event.x
            self.drag_data['y'] = event.y

    def on_drag(self, event):
        if self.resize_data['resizing']:
            self.resize_window(event)
            return
        if self.drag_data['dragging']:
            self.x = self.root.winfo_x() + event.x - self.drag_data['x']
            self.y = self.root.winfo_y() + event.y - self.drag_data['y']
            self.constrain_horizontal()  # === 新增：限制水平移动 ===
            self.keep_above_taskbar_hotspot()
            self.root.geometry(f"+{int(self.x)}+{int(self.y)}")

    def on_release(self, event):
        self.root.attributes('-alpha', self.original_alpha)
        self.constrain_horizontal()  # === 新增：确保最终位置在屏幕内 ===
        self.keep_above_taskbar_hotspot()
        self.set_geometry()
        self.drag_data['dragging'] = False
        self.resize_data['resizing'] = False
        self.resize_data['edge'] = None

    def on_motion(self, event):
        if self.resize_data['resizing'] or self.drag_data['dragging']:
            return
        edge = self.get_edge(event.x, event.y)
        if edge in ('e', 'w'):
            self.canvas.config(cursor='sb_h_double_arrow')
        elif edge in ('n', 's'):
            self.canvas.config(cursor='sb_v_double_arrow')
        elif edge in ('ne', 'sw'):
            self.canvas.config(cursor='size_ne_sw')
        elif edge in ('nw', 'se'):
            self.canvas.config(cursor='size_nw_se')
        else:
            self.canvas.config(cursor='')

    def get_edge(self, x, y):
        t = self.resize_threshold
        edge = ''

        if y < t:
            edge += 'n'
        elif y > self.height - t:
            edge += 's'

        if x < t:
            edge += 'w'
        elif x > self.width - t:
            edge += 'e'

        return edge if edge else None

    def resize_window(self, event):
        edge = self.resize_data['edge']
        dx = event.x_root - self.resize_data['start_x']
        dy = event.y_root - self.resize_data['start_y']

        new_width = self.resize_data['start_width']
        new_height = self.resize_data['start_height']
        new_x = self.resize_data['start_window_x']
        new_y = self.resize_data['start_window_y']

        if 'e' in edge:
            new_width += dx
        if 'w' in edge:
            new_width -= dx
            new_x += dx
        if 's' in edge:
            new_height += dy
        if 'n' in edge:
            new_height -= dy
            new_y += dy

        screen_width, _ = get_screen_size(self.root)

        # === 新增：限制缩放时左右边界不超出屏幕 ===
        self.width = max(100, new_width)
        self.height = max(30, new_height)

        # 限制左边界
        if new_x < 0:
            self.width += new_x  # 如果左边超出，收缩宽度补偿
            new_x = 0

        # 限制右边界
        if new_x + self.width > screen_width:
            self.width = screen_width - new_x

        self.width = max(100, self.width)  # 确保最小宽度
        self.x = new_x
        self.y = new_y

        self.keep_above_taskbar_hotspot()
        self.set_geometry()

    def on_right_click(self, event):
        if self.right_click_timer:
            self.root.destroy()
        else:
            self.right_click_timer = self.root.after(300, self.reset_right_click)

    def reset_right_click(self):
        self.right_click_timer = None

    # === 全局 Z 键轮询（GetAsyncKeyState，无论焦点在哪个窗口都生效） ===
    def poll_z_key(self):
        """每 50ms 检查 Z 键物理状态，按下变半透明，松开恢复"""
        z_down = ctypes.windll.user32.GetAsyncKeyState(0x5A) & 0x8000
        if z_down and not self.z_pressed:
            self.z_pressed = True
            self.root.attributes('-alpha', DRAG_ALPHA)
        elif not z_down and self.z_pressed:
            self.z_pressed = False
            self.root.attributes('-alpha', self.original_alpha)
        self.root.after(50, self.poll_z_key)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = SubtitleBlocker()
    app.run()
