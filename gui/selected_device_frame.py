from gui.creator import load_bot_config
from gui.creator import load_building_pos
from gui.creator import write_building_pos, write_bot_config
from gui.creator import button

from tkinter import Label, Frame, Text, Scrollbar, Canvas, LabelFrame, Toplevel, Entry, Button, StringVar
from tkinter import N, W, END, NSEW, INSERT, LEFT

from gui import bot_config_fns as atf
from bot_related.bot import Bot
from tasks.constants import BuildingNames
from filepath.file_relative_paths import ImagePathAndProps
from PIL import ImageTk, Image
from tasks.Task import Task
import time
from utils import log, device_log
import os, errno

class SelectedDeviceFrame(Frame):

    def __init__(self, windows, device, cnf={}, **kwargs):
        Frame.__init__(self, windows, kwargs)

        self.building_pos_window = None

        self.bot = Bot(device)
        self.device = device
        self.bot_config = load_bot_config(self.device.save_file_prefix)
        self.bot_building_pos = load_building_pos(self.device.save_file_prefix)
        self.windows_size = [kwargs['width'], kwargs['height']]

        display_frame, self.name, self.task_title, self.task_text, self.display_canvas = self.task_display_frame()
        config_frame = self.config_frame()
        bottom_frame = self.bottom_frame()

        display_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky=N+W)
        config_frame.grid(row=2, column=0, padx=10, sticky=N + W)
        bottom_frame.grid(row=3, column=0, padx=10, pady=(10, 10), sticky=(N+W))

        # def handle_focus(event):
        #     if event.widget == self.master.master.master and self.building_pos_window is not None:
        #         self.building_pos_window.attributes('-topmost', 1)
        #         self.building_pos_window.attributes('-topmost', 0)
        #         self.building_pos_window.focus_force()
        #
        # self.master.master.master.bind("<FocusIn>", handle_focus)
        if self.bot_building_pos is None:
            self.bot_config.hasBuildingPos = False
            self.bot_building_pos = {}

        self.bot.config = self.bot_config
        self.bot.building_pos = self.bot_building_pos

        self.bot.text_update_event = self.on_task_update
        self.bot.building_pos_update_event = lambda **kw: write_building_pos(kw['building_pos'], kw['prefix'])
        # self.bot.config_update_event = lambda **kw: write_bot_config(kw['config'], kw['prefix'])
        self.bot.config_update_event = self.on_config_update
        # self.bot.snashot_update_event = self.on_snashot_update
        
        self.refresh_snapshot()
        
    def refresh_snapshot(self):
        # device_log(self.device, '截图')
        img = self.bot.gui.get_curr_device_screen_img()
        try:
            os.mkdir('capture')
        except BaseException as e:
            if e.errno != errno.EEXIST:
                print(e)
        img2 = img.convert('RGB')    
        img2 = img2.resize((640, 360))    
        img2.save('capture/{}.jpg'.format(self.device.name))
        
        img = img.resize((205, 155))
        self.display_canvas.img = image = ImageTk.PhotoImage(img)
        self.display_canvas.create_image(5, 5, image=image, anchor='nw')
            
    def task_display_frame(self):
        width = self.windows_size[0] - 20
        height = 210
        frame = Frame(self, width=width, height=height)
        frame.grid_propagate(False)
        frame.columnconfigure(0, weight=width)
        frame.rowconfigure(0, weight=5)
        frame.rowconfigure(1, weight=5)
        frame.rowconfigure(2, weight=height - 10)

        nickname = '{}-{}-{}'.format(self.device.save_file_prefix, self.device.nickname, self.device.serial) if len(self.device.nickname)>0 is not None else '{}-{}'.format(self.device.save_file_prefix, self.device.serial)
        name = Label(frame, text=nickname, width=width, height=5, bg='white')
        title = Label(frame, text="Task: None", width=width, height=5, bg='white')
        # title.config(bg='white', anchor=W, justify=LEFT)
        text = Text(frame, width=width, height=height - 30)
        canvas = Canvas(frame, width=210)

        name.grid(row=0, column=0, columnspan=2, pady=5, sticky=N + W)
        title.grid(row=1, column=0, pady=5, sticky=N + W)
        text.grid(row=2, column=0, pady=5, sticky=N + W)
        canvas.grid(row=1, column=1, rowspan=2, pady=0, sticky=N + W)
        
        return frame, name, title, text, canvas

    def config_frame(self):
        frame_canvas = LabelFrame(self,
                                  text='Config',
                                  width=self.windows_size[0],
                                  height=self.windows_size[1] - 100
                                  )
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        canvas = Canvas(frame_canvas)
        canvas.grid(row=0, column=0, sticky=N + W)

        # Link a scrollbar to the canvas

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def bound_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", on_mousewheel)

        def unbound_to_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        y_scrollbar = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=y_scrollbar.set)

        inner_frame = Frame(canvas)
        inner_frame.bind('<Enter>', bound_to_mousewheel)
        inner_frame.bind('<Leave>', unbound_to_mousewheel)

        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        for i in range(len(atf.bot_config_title_fns)):
            title_fns, sub_fns = atf.bot_config_title_fns[i]
            check = section_frame(
                self,
                inner_frame,
                title_fns,
                sub_fns
            )
            check.grid(row=i, column=0, sticky=N + W)

        inner_frame.update_idletasks()

        frame_canvas.config(width=self.windows_size[0] - 20, height=self.windows_size[1] - 350)
        canvas.config(width=self.windows_size[0] - 20, height=self.windows_size[1] - 350,
                      scrollregion=canvas.bbox("all"))

        return frame_canvas

    def start(self):
        # if self.bot_building_pos is None:
        #     self.bot_config.hasBuildingPos = False
        #     self.bot_building_pos = {}
        #
        # self.bot.config = self.bot_config
        # self.bot.building_pos = self.bot_building_pos
        #
        # self.bot.text_update_event = self.on_task_update
        # self.bot.building_pos_update_event = lambda **kw: write_building_pos(kw['building_pos'], kw['prefix'])
        # self.bot.config_update_event = lambda **kw: write_bot_config(kw['config'], kw['prefix'])
        # self.bot.snashot_update_event = self.on_snashot_update
        self.task_title.config(text='Task: None')
        self.task_text.delete(1.0, END)
        self.bot.start(self.bot.do_task)

    def stop(self):
        self.bot.stop()
        # self.task_title.config(text='Task: None')
        # self.task_text.delete(1.0, END)

    def bottom_frame(self):
        frame = Frame(self)

        # start/stop
        def on_start_or_stop_click(btn):
            if btn.cget('text') == 'Start':
                self.start()
                btn.config(text='Stop')
            elif btn.cget('text') == 'Stop':
                self.stop()
                btn.config(text='Start')
            return

        start_button = button(frame, on_start_or_stop_click, text='Start')
        start_button.grid(row=0, column=0, padx=(0, 5), sticky=N + W)
        self.start_button = start_button
                
        def on_kill_click(btn):
            task = Task(self.bot)
            task.stopRok()
            
        kill_button = button(frame, on_kill_click, text='Kill')
        kill_button.grid(row=0, column=1, sticky=N + W)
        
        #building position setting
        def on_building_pos_click(btn):
            if self.building_pos_window is None:
                self.building_pos_window = building_pos_window(self)

        building_pos_button = button(frame, on_building_pos_click, text='Building Pos')
        building_pos_button.grid(row=0, column=2, sticky=N + W)

        # snapshot
        def on_snapshot_click(btn):
            # self.bot.gui.save_screen('{}.png'.format(self.bot.device.name))
            self.refresh_snapshot()
            
        snapshot_button = button(frame, on_snapshot_click, text='Snapshot')
        snapshot_button.grid(row=0, column=3, sticky=N + W)
        
        # change account
        def on_switch_account_click(btn):
            task = Task(self.bot)
            task.back_to_map_gui()
            # 打开设置
            task.tap((50, 50))
            task.tap((990, 570))
            # 账号管理
            task.tap((700, 380))
            # 切换账号
            task.tap((640, 680))
            _, _, login_other_pos = self.bot.gui.check_any(ImagePathAndProps.LOGIN_OTHER_BUTTON_PATH.value)
            if login_other_pos is not None:
                task.tap(login_other_pos)
                
            # 同意隐私
            task.tap((185, 220))
            # 输入手机
            task.text(185, 140, '13751872204')
            # 发送验证码
            task.tap((640, 300))
            
        switch_account_button = button(frame, on_switch_account_click, text='Switch By Phone')
        switch_account_button.grid(row=1, column=0, columnspan=2, sticky=N + W)
                
        return frame

    def on_task_update(self, text):
        name, title, text_list = text['name'], text['title'], text['text_list']
        if len(name) > 0:
            nickname = '{}-{}-{}'.format(self.device.save_file_prefix, name, self.device.serial)
            self.name.config(text=nickname)
        self.task_title.config(text="Task: " + title)
        self.task_text.delete(1.0, END)
        for t in text_list:
            self.task_text.insert(INSERT, t + '\n')
            
    def on_config_update(self, **kw):
        write_bot_config(kw['config'], kw['prefix'])
        config_frame = self.config_frame()
        config_frame.grid(row=2, column=0, padx=10, sticky=N + W)
        nickname = '{}-{}-{}'.format(self.device.save_file_prefix, self.device.nickname, self.device.serial) if len(self.device.nickname)>0 is not None else '{}-{}'.format(self.device.save_file_prefix, self.device.serial)
        self.name.config(text=nickname)
        return
           
    def on_snashot_update(self):
        self.refresh_snapshot()

def section_frame(app, parent, title_component_fn, sub_component_fns=[], start_row=0, start_column=0):
    outer_frame = Frame(parent)
    inner_frame = Frame(outer_frame)

    def disable_when_false(checked):
        if checked:
            enableChildren(inner_frame)
        else:
            disableChildren(inner_frame)

    title, variable = title_component_fn(app, outer_frame, disable_when_false)
    title.grid(row=start_row, column=start_column, sticky=N + W)

    inner_frame.grid(row=start_row + 1, column=0, padx=30, pady=0, sticky=N + W)

    for row in range(len(sub_component_fns)):
        component, _ = sub_component_fns[row](app, inner_frame)
        component.grid(row=row, column=0, sticky=N + W)

    if not variable.get():
        disableChildren(inner_frame)
    else:
        enableChildren(inner_frame)

    return outer_frame


def disableChildren(parent):
    children = parent.winfo_children()
    for child in children:
        wtype = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe'):
            child.configure(state='disable')
            if wtype == 'Menubutton':
                child.config(width=8, bg='#F0F0F0')
        else:
            disableChildren(child)


def enableChildren(parent):
    for child in parent.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe'):
            child.configure(state='normal')
            if wtype == 'Menubutton':
                child.config(width=8, bg='white')
        else:
            enableChildren(child)


def building_pos_window(parent):
    width = 1024
    height = 360

    selected_building = {
        'name': None,
        'label': None,
        'prev_pos': [-1, -1],
    }

    def building_name_xy_config_frame(master, row, name, pos):
        name_label = Label(master, text=name.replace('_', ' ').title())
        pos_label = Label(master, text='[{}, {}]'.format(pos[0], pos[1]), width=18)

        def on_set_click(btn):
            if selected_building['name'] is not None:
                selected_building['label'].config(
                    text='[{}, {}]'.format(
                        selected_building['prev_pos'][0], selected_building['prev_pos'][1]
                    )
                )

            selected_building['name'] = name
            selected_building['label'] = pos_label
            selected_building['label'].config(text='click on building')
            selected_building['prev_pos'] = pos


        set_button = button(master, on_set_click, text='Edit', )

        name_label.grid(row=row, column=0, pady=2, sticky=W)
        pos_label.grid(row=row, column=1, pady=2, sticky=W)
        set_button.grid(row=row, column=2, pady=2, sticky=NSEW)

    def close_window():
        parent.building_pos_window.grab_release()
        parent.building_pos_window.destroy()
        parent.building_pos_window = None

    def image_frame(parent):
        frame = Frame(parent.building_pos_window, width=640, height=360)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_propagate(False)
        frame.grid(row=0, column=0, sticky=N + W)

        label = Label(frame, text='Loading city image, Please wait!', background='white')
        label.grid(row=0, column=0, sticky=NSEW)

        canvas = Canvas(frame, width=640, height=360)

        def setBuildingCoords(event):
            if selected_building['name'] is None:
                return
            pos = [event.x * 2, event.y * 2]
            if parent.bot_building_pos is None:
                parent.bot_building_pos = {}

            parent.bot_config.hasBuildingPos = True
            parent.bot_building_pos[selected_building['name']] = [pos[0], pos[1]]
            write_building_pos(
                parent.bot_building_pos,
                parent.device.save_file_prefix
            )
            selected_building['label'].config(text='[{}, {}]'.format(pos[0], pos[1]))
            selected_building['name'] = None
            selected_building['label'] = None

        canvas.bind("<Button 1>", setBuildingCoords)

        def after_image_load():
            # image = parent.bot.get_city_image().resize((640, 360), Image.ANTIALIAS)
            image = parent.bot.get_city_image().resize((640, 360), Image.LANCZOS)
            frame.image = image = ImageTk.PhotoImage(image)
            canvas.create_image((0, 0), image=image, anchor='nw')
            parent.bot.curr_thread = None
            label.grid_forget()
            canvas.grid(row=0, column=0, sticky=N + W)

        parent.bot.start(after_image_load)

        return frame

    def right_frame(parent):
        rf_width = 360
        rf_height = 360
        # right side frame
        frame_right = LabelFrame(parent.building_pos_window,
                                 text="Building Position",
                                 width=rf_width - 10,
                                 height=rf_height - 10,
                                 )

        frame_right.grid_rowconfigure(0, weight=1)
        frame_right.grid_columnconfigure(0, weight=1)
        frame_right.grid_propagate(False)

        canvas_right = Canvas(frame_right)
        canvas_right.grid(row=0, column=0, sticky=N + W)

        # Link a scrollbar to the canvas
        def on_mousewheel(event):
            canvas_right.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def bound_to_mousewheel(event):
            canvas_right.bind_all("<MouseWheel>", on_mousewheel)

        def unbound_to_mousewheel(event):
            canvas_right.unbind_all("<MouseWheel>")

        y_scrollbar = Scrollbar(frame_right, orient="vertical", command=canvas_right.yview)
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        canvas_right.configure(yscrollcommand=y_scrollbar.set)

        inner_frame_right = Frame(canvas_right)
        inner_frame_right.bind('<Enter>', bound_to_mousewheel)
        inner_frame_right.bind('<Leave>', unbound_to_mousewheel)

        canvas_right.create_window((0, 0), window=inner_frame_right, anchor='nw')

        idx = 0
        for e_name in BuildingNames:
            building_name_xy_config_frame(
                inner_frame_right,
                idx,
                e_name.value,
                parent.bot_building_pos.get(e_name.value, [-1, -1]) if parent.bot_building_pos is not None else [-1, -1]
            )
            idx = idx + 1

        inner_frame_right.update_idletasks()

        frame_right.config(width=rf_width - 10, height=360 - 10)
        canvas_right.config(width=rf_width - 10, height=360 - 10, scrollregion=canvas_right.bbox("all"))

        frame_right.grid(row=0, column=1, padx=5, pady=5, sticky=N + W)

        return inner_frame_right

    def set_focus(event):
        parent.building_pos_window.attributes('-topmost', 1)
        parent.building_pos_window.attributes('-topmost', 0)
        parent.building_pos_window.focus_force()

    parent.building_pos_window = Toplevel(parent.master.master.master)
    parent.building_pos_window.resizable(0, 0)
    parent.building_pos_window.grab_set()

    parent.building_pos_window.title("{} Building Position".format(parent.device.serial.replace(':', "_")))
    parent.building_pos_window.geometry("{}x{}".format(width, height))
    parent.building_pos_window.protocol("WM_DELETE_WINDOW", close_window)

    image_frame(parent)
    rf = right_frame(parent)

    set_focus(None)

    return parent.building_pos_window
