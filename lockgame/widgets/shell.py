from gi.repository import Gtk

class ShellWidget(Gtk.ScrolledWindow):
    """
        Custom widget which tries to mimic a simple shell
    """

    def __init__(self, shell_manager, *args, **kwargs):
        Gtk.VBox.__init__(self, *args, **kwargs)

        self.listener_ids = []
        self.set_shell_manager(shell_manager)

        self.viewport = Gtk.Viewport()
        self.add(self.viewport)

        # Create vbox
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.viewport.add(self.vbox)

        # Create textview
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.vbox.pack_start(self.textview, True, True, 0)

        # Create command entry widget
        # This contains a label containing the prompt, and the entry itself
        self.entry_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.prompt_label = Gtk.Label("Booting...")
        self.command_entry = Gtk.Entry()
        self.command_entry.connect('activate', self.run_command)

        self.entry_hbox.pack_start(self.prompt_label, False, True, 10)
        self.entry_hbox.pack_start(self.command_entry, True, True, 0)

        self.vbox.pack_start(self.entry_hbox, False, True, 0)

    def set_shell_manager(self, shell_manager):
        if self.listener_ids:
            for listener_id in self.listener_ids:
                self.shell_manager.disconnect(listener_id)

        self.shell_manager = shell_manager
        self.listener_ids.append(
            self.shell_manager.connect('command-done', self.on_command_done))
        self.listener_ids.append(
            self.shell_manager.connect('command-output', self.on_command_output))

    def run_command(self, entry):
        command = self.command_entry.get_text()
        self.add_text("test@localhost> {}".format(command))
        self.command_entry.set_editable(False)
        self.command_entry.set_text("")
        self.shell_manager.run_command(command)

    def on_command_done(self, sender):
        self.command_entry.set_editable(True)

    def add_text(self, text):
        self.textbuffer.insert(self.textbuffer.get_end_iter(), text)
        adj = self.viewport.get_vadjustment()

        adj.set_value(adj.get_upper())

    def on_command_output(self, sender, text):
        self.add_text(text)
