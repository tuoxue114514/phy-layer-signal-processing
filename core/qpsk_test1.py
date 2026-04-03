from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip
from sinks import Sinks
from gold_sequence_insertion import gold_sequence_insertion



class qpsk_test1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "qpsk_test1", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("qpsk_test1")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "qpsk_test1")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################

        # 创建sink实例
        self.sinks = Sinks(self, samp_rate)

        # 获取各个sink
        self.qtgui_time_sink_x_1_0 = self.sinks.get_received_time_sink()
        self.qtgui_time_sink_x_1 = self.sinks.get_transmitted_time_sink()
        self.qtgui_const_sink_x_0_0 = self.sinks.get_received_const_sink()
        self.qtgui_const_sink_x_0 = self.sinks.get_transmitted_const_sink()
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc([1+1j,-1+1j,-1-1j,1-1j], 1)
        self.gold_sequence_insertion_0 = gold_sequence_insertion()
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=0.01,
            frequency_offset=0.1,
            epsilon=1.0,
            taps=[1.0],
            noise_seed=0,
            block_tags=False)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, 2, "", False, gr.GR_MSB_FIRST)
        self.blocks_file_source_0_1 = blocks.file_source(gr.sizeof_char*1, 'core/test_input.txt', True, 0, 0)
        self.blocks_file_source_0_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/dell/Desktop/py_project/PMF-FFT/demo4_GUI/output/gold_encoded_data.dat', False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0_1, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.gold_sequence_insertion_0, 0))
        self.connect((self.gold_sequence_insertion_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_time_sink_x_1_0, 0))
        self.connect((self.gold_sequence_insertion_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.gold_sequence_insertion_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.gold_sequence_insertion_0, 0), (self.blocks_file_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "qpsk_test1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.samp_rate)




def main(top_block_cls=qpsk_test1, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
