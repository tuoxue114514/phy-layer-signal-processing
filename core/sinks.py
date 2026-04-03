from PyQt5 import Qt
from gnuradio import qtgui
import sip

class Sinks:
    def __init__(self, parent, samp_rate):
        self.parent = parent
        self.samp_rate = samp_rate
        self.create_sinks()
        self.configure_sinks()
        self.add_to_layout()
    
    def create_sinks(self):
        # 创建时间波形sink
        self.received_time_sink = qtgui.time_sink_c(
            4096, #size
            self.samp_rate, #samp_rate
            "Received Waveform", #name
            1, #number of inputs
            None # parent
        )
        
        self.transmitted_time_sink = qtgui.time_sink_c(
            4096, #size
            self.samp_rate, #samp_rate
            "Transmitted Waveform", #name
            1, #number of inputs
            None # parent
        )
        
        # 创建星座图sink
        self.received_const_sink = qtgui.const_sink_c(
            1024, #size
            "Received Constellation", #name
            1, #number of inputs
            None # parent
        )
        
        self.transmitted_const_sink = qtgui.const_sink_c(
            1024, #size
            "Transmitted Constellation", #name
            1, #number of inputs
            None # parent
        )
    
    def configure_sinks(self):
        # 配置接收时间波形sink
        self.received_time_sink.set_update_time(0.10)
        self.received_time_sink.set_y_axis(-1, 1)
        self.received_time_sink.set_y_label('Amplitude', "")
        self.received_time_sink.enable_tags(True)
        self.received_time_sink.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.received_time_sink.enable_autoscale(True)
        self.received_time_sink.enable_grid(False)
        self.received_time_sink.enable_axis_labels(True)
        self.received_time_sink.enable_control_panel(False)
        self.received_time_sink.enable_stem_plot(False)
        
        # 配置发送时间波形sink
        self.transmitted_time_sink.set_update_time(0.10)
        self.transmitted_time_sink.set_y_axis(-1, 1)
        self.transmitted_time_sink.set_y_label('Amplitude', "")
        self.transmitted_time_sink.enable_tags(True)
        self.transmitted_time_sink.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.transmitted_time_sink.enable_autoscale(True)
        self.transmitted_time_sink.enable_grid(False)
        self.transmitted_time_sink.enable_axis_labels(True)
        self.transmitted_time_sink.enable_control_panel(False)
        self.transmitted_time_sink.enable_stem_plot(False)
        
        # 配置接收星座图sink
        self.received_const_sink.set_update_time(0.10)
        self.received_const_sink.set_y_axis((-2.5), 2.5)
        self.received_const_sink.set_x_axis((-2.5), 2.5)
        self.received_const_sink.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.received_const_sink.enable_autoscale(False)
        self.received_const_sink.enable_grid(False)
        self.received_const_sink.enable_axis_labels(True)
        
        # 配置发送星座图sink
        self.transmitted_const_sink.set_update_time(0.10)
        self.transmitted_const_sink.set_y_axis((-2.5), 2.5)
        self.transmitted_const_sink.set_x_axis((-2.5), 2.5)
        self.transmitted_const_sink.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.transmitted_const_sink.enable_autoscale(False)
        self.transmitted_const_sink.enable_grid(False)
        self.transmitted_const_sink.enable_axis_labels(True)
        
        # 配置时间波形sink的线条
        time_labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        time_widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        time_colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        time_alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        time_styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        time_markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]
        
        for i in range(2):
            if len(time_labels[i]) == 0:
                if (i % 2 == 0):
                    self.received_time_sink.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                    self.transmitted_time_sink.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.received_time_sink.set_line_label(i, "Im{{Data {0}}}".format(i/2))
                    self.transmitted_time_sink.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.received_time_sink.set_line_label(i, time_labels[i])
                self.transmitted_time_sink.set_line_label(i, time_labels[i])
            self.received_time_sink.set_line_width(i, time_widths[i])
            self.transmitted_time_sink.set_line_width(i, time_widths[i])
            self.received_time_sink.set_line_color(i, time_colors[i])
            self.transmitted_time_sink.set_line_color(i, time_colors[i])
            self.received_time_sink.set_line_style(i, time_styles[i])
            self.transmitted_time_sink.set_line_style(i, time_styles[i])
            self.received_time_sink.set_line_marker(i, time_markers[i])
            self.transmitted_time_sink.set_line_marker(i, time_markers[i])
            self.received_time_sink.set_line_alpha(i, time_alphas[i])
            self.transmitted_time_sink.set_line_alpha(i, time_alphas[i])
        
        # 配置星座图sink的线条
        const_labels = ['', '', '', '', '',
            '', '', '', '', '']
        const_widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        const_colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        const_styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        const_markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        const_alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in range(1):
            if len(const_labels[i]) == 0:
                self.received_const_sink.set_line_label(i, "Data {0}".format(i))
                self.transmitted_const_sink.set_line_label(i, "Data {0}".format(i))
            else:
                self.received_const_sink.set_line_label(i, const_labels[i])
                self.transmitted_const_sink.set_line_label(i, const_labels[i])
            self.received_const_sink.set_line_width(i, const_widths[i])
            self.transmitted_const_sink.set_line_width(i, const_widths[i])
            self.received_const_sink.set_line_color(i, const_colors[i])
            self.transmitted_const_sink.set_line_color(i, const_colors[i])
            self.received_const_sink.set_line_style(i, const_styles[i])
            self.transmitted_const_sink.set_line_style(i, const_styles[i])
            self.received_const_sink.set_line_marker(i, const_markers[i])
            self.transmitted_const_sink.set_line_marker(i, const_markers[i])
            self.received_const_sink.set_line_alpha(i, const_alphas[i])
            self.transmitted_const_sink.set_line_alpha(i, const_alphas[i])
    
    def add_to_layout(self):
        # 将sink添加到布局中
        self.received_time_sink_win = sip.wrapinstance(self.received_time_sink.qwidget(), Qt.QWidget)
        self.parent.top_layout.addWidget(self.received_time_sink_win)
        
        self.transmitted_time_sink_win = sip.wrapinstance(self.transmitted_time_sink.qwidget(), Qt.QWidget)
        self.parent.top_layout.addWidget(self.transmitted_time_sink_win)
        
        self.received_const_sink_win = sip.wrapinstance(self.received_const_sink.qwidget(), Qt.QWidget)
        self.parent.top_layout.addWidget(self.received_const_sink_win)
        
        self.transmitted_const_sink_win = sip.wrapinstance(self.transmitted_const_sink.qwidget(), Qt.QWidget)
        self.parent.top_layout.addWidget(self.transmitted_const_sink_win)
    
    def get_received_time_sink(self):
        return self.received_time_sink
    
    def get_transmitted_time_sink(self):
        return self.transmitted_time_sink
    
    def get_received_const_sink(self):
        return self.received_const_sink
    
    def get_transmitted_const_sink(self):
        return self.transmitted_const_sink
