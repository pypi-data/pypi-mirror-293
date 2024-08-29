# ******************************************************************************
# Copyright (c) 2019 Analog Devices, Inc.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
# - Modified versions of the software must be conspicuously marked as such.
# - This software is licensed solely and exclusively for use with
#  processors/products manufactured by or for Analog Devices, Inc.
# - This software may not be combined or merged with other code in any manner
#  that would cause the software to become subject to terms and conditions
#  which differ from those listed here.
# - Neither the name of Analog Devices, Inc. nor the names of its contributors
#  may be used to endorse or promote products derived from this software
#  without specific prior written permission.
# - The use of this software may or may not infringe the patent rights of one
#  or more patent holders.  This license does not release you from the
#  requirement that you obtain separate licenses from these patent holders to
#  use this software.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES, INC. AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# NONINFRINGEMENT, TITLE, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ANALOG DEVICES, INC. OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, DAMAGES ARISING OUT OF
# CLAIMS OF INTELLECTUAL PROPERTY RIGHTS INFRINGEMENT; PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ******************************************************************************

from .. import utils
from ..data_types.array import Array
from ..data_types.enums import Enums
from ..data_types.integer import Int
from ..data_types.decimal import Decimal
from .command_packet import CommandPacket
from ..enums.bia_enums import BIASweepFrequency, BIAAppInfo


class ADPDDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.ADPD6: ['0xC2', '0x16']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x2C',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'data_type': 4,
                'channel_num': 2,
                'timestamp': 1751731879,
                'sample_num': 2,
                'signal_data': [ 351762, 351755 ],
                'dark_data': [ 0, 0 ],
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["data_type"] = Int(2)
        self._config["payload"]["channel_num"] = Int(1)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["sample_num"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=1, data_types=[Int(1)])

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["dark_data"] = []
        packet["payload"]["signal_data"] = []
        if packet["payload"]["data_type"] & 0x100 == 0:
            signal_size = (packet["payload"]["data_type"] & 0xF)
            dark_size = (packet["payload"]["data_type"] & 0xF0) >> 4
            data_size = signal_size + dark_size
            sample_num = packet["payload"]["sample_num"]
            for i in range(0, sample_num * data_size, data_size):
                data = packet["payload"]["data"][i: i + dark_size]
                dark_data = utils.join_multi_length_packets(data)
                data = packet["payload"]["data"][i + dark_size: i + dark_size + signal_size]
                signal_data = utils.join_multi_length_packets(data)
                packet["payload"]["dark_data"].append(dark_data)
                packet["payload"]["signal_data"].append(signal_data)
        else:
            signal_size = (packet["payload"]["data_type"] & 0xFF)
            for i in range(0, signal_size, 2):
                packet["payload"]["dark_data"].append(0)
                data = packet["payload"]["data"][i: i + 1]
                signal_data = utils.join_multi_length_packets(data)
                packet["payload"]["signal_data"].append(signal_data)
        del packet["payload"]["data"]
        utils.update_timestamp(packet, last_timestamp)
        return packet


class ADXLDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.ADXL: ['0xC2', '0x02']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x37',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 395,
                'data_type': 0,
                'stream_data': [
                    {
                        'timestamp': 1767361372,
                        'x': -85,
                        'y': 90,
                        'z': 55
                    },
                    {
                        'timestamp': 1767362027,
                        'x': -80,
                        'y': 88,
                        'z': 55
                    },
                    {
                        'timestamp': 1767362682,
                        'x': 40,
                        'y': 274,
                        'z': 79
                    },
                    {
                        'timestamp': 1767363337,
                        'x': 70,
                        'y': 273,
                        'z': 54
                    },
                    {
                        'timestamp': 1767363931,
                        'x': 57,
                        'y': 257,
                        'z': 48
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["data_type"] = Int(1)
        self._config["payload"]["timestamp1"] = Int(4)
        self._config["payload"]["x1"] = Int(2, sign=True)
        self._config["payload"]["y1"] = Int(2, sign=True)
        self._config["payload"]["z1"] = Int(2, sign=True)
        self._config["payload"]["timestamp2"] = Int(2)
        self._config["payload"]["x2"] = Int(2, sign=True)
        self._config["payload"]["y2"] = Int(2, sign=True)
        self._config["payload"]["z2"] = Int(2, sign=True)
        self._config["payload"]["timestamp3"] = Int(2)
        self._config["payload"]["x3"] = Int(2, sign=True)
        self._config["payload"]["y3"] = Int(2, sign=True)
        self._config["payload"]["z3"] = Int(2, sign=True)
        self._config["payload"]["timestamp4"] = Int(2)
        self._config["payload"]["x4"] = Int(2, sign=True)
        self._config["payload"]["y4"] = Int(2, sign=True)
        self._config["payload"]["z4"] = Int(2, sign=True)
        self._config["payload"]["timestamp5"] = Int(2)
        self._config["payload"]["x5"] = Int(2, sign=True)
        self._config["payload"]["y5"] = Int(2, sign=True)
        self._config["payload"]["z5"] = Int(2, sign=True)

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        timestamp = 0
        for i in range(1, 6):
            timestamp += packet["payload"][f"timestamp{i}"]
            data = {
                "timestamp": timestamp,
                "x": packet["payload"][f"x{i}"],
                "y": packet["payload"][f"y{i}"],
                "z": packet["payload"][f"z{i}"]
            }
            [packet["payload"].pop(key) for key in [f"timestamp{i}", f"x{i}", f"y{i}", f"z{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet


class ECGDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.ECG: ['0xC4', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x3D',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'data_type': 1,
                'ecg_info': 0,
                'hr': 0,
                'stream_data': [
                    {
                        'timestamp': 1771095376,
                        'ecg_data': 12351
                    },
                    {
                        'timestamp': 1771095703,
                        'ecg_data': 12353
                    },
                    {
                        'timestamp': 1771096030,
                        'ecg_data': 52470
                    },
                    {
                        'timestamp': 1771096357,
                        'ecg_data': 41129
                    },
                    {
                        'timestamp': 1771096676,
                        'ecg_data': 63838
                    },
                    {
                        'timestamp': 1771096995,
                        'ecg_data': 63848
                    },
                    {
                        'timestamp': 1771097314,
                        'ecg_data': 63848
                    },
                    {
                        'timestamp': 1771097633,
                        'ecg_data': 63848
                    },
                    {
                        'timestamp': 1771097954,
                        'ecg_data': 63833
                    },
                    {
                        'timestamp': 1771098273,
                        'ecg_data': 63846
                    },
                    {
                        'timestamp': 1771098592,
                        'ecg_data': 63846
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["data_type"] = Int(1)
        self._config["payload"]["timestamp1"] = Int(4)
        self._config["payload"]["ecg_info"] = Int(1)
        self._config["payload"]["hr"] = Int(1)
        self._config["payload"]["ecg_data1"] = Int(2)
        self._config["payload"]["timestamp2"] = Int(2)
        self._config["payload"]["ecg_data2"] = Int(2)
        self._config["payload"]["timestamp3"] = Int(2)
        self._config["payload"]["ecg_data3"] = Int(2)
        self._config["payload"]["timestamp4"] = Int(2)
        self._config["payload"]["ecg_data4"] = Int(2)
        self._config["payload"]["timestamp5"] = Int(2)
        self._config["payload"]["ecg_data5"] = Int(2)
        self._config["payload"]["timestamp6"] = Int(2)
        self._config["payload"]["ecg_data6"] = Int(2)
        self._config["payload"]["timestamp7"] = Int(2)
        self._config["payload"]["ecg_data7"] = Int(2)
        self._config["payload"]["timestamp8"] = Int(2)
        self._config["payload"]["ecg_data8"] = Int(2)
        self._config["payload"]["timestamp9"] = Int(2)
        self._config["payload"]["ecg_data9"] = Int(2)
        self._config["payload"]["timestamp10"] = Int(2)
        self._config["payload"]["ecg_data10"] = Int(2)
        self._config["payload"]["timestamp11"] = Int(2)
        self._config["payload"]["ecg_data11"] = Int(2)

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        timestamp = 0
        for i in range(1, 12):
            timestamp += packet["payload"][f"timestamp{i}"]
            data = {"timestamp": timestamp,
                    "ecg_data": packet["payload"][f"ecg_data{i}"]}
            [packet["payload"].pop(key) for key in [f"timestamp{i}", f"ecg_data{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet


class EDADataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.EDA: ['0xC4', '0x02']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x3D',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'data_type': 0,
                'stream_data': [
                    {
                        'timestamp': 1774366622,
                        'real': 0,
                        'imaginary': 0
                    },
                    {
                        'timestamp': 1774374407,
                        'real': 0,
                        'imaginary': 16708
                    },
                    {
                        'timestamp': 1774382157,
                        'real': 16728,
                        'imaginary': 3257
                    },
                    {
                        'timestamp': 1774389924,
                        'real': 3277,
                        'imaginary': -20751
                    },
                    {
                        'timestamp': 1774397691,
                        'real': -20731,
                        'imaginary': -15161
                    },
                    {
                        'timestamp': 1774405458,
                        'real': -15141,
                        'imaginary': -30319
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["data_type"] = Int(1)
        self._config["payload"]["timestamp1"] = Int(4)
        self._config["payload"]["real1"] = Int(2, sign=True)
        self._config["payload"]["imaginary1"] = Int(2, sign=True)
        self._config["payload"]["timestamp2"] = Int(4)
        self._config["payload"]["real2"] = Int(2, sign=True)
        self._config["payload"]["imaginary2"] = Int(2, sign=True)
        self._config["payload"]["timestamp3"] = Int(4)
        self._config["payload"]["real3"] = Int(2, sign=True)
        self._config["payload"]["imaginary3"] = Int(2, sign=True)
        self._config["payload"]["timestamp4"] = Int(4)
        self._config["payload"]["real4"] = Int(2, sign=True)
        self._config["payload"]["imaginary4"] = Int(2, sign=True)
        self._config["payload"]["timestamp5"] = Int(4)
        self._config["payload"]["real5"] = Int(2, sign=True)
        self._config["payload"]["imaginary5"] = Int(2, sign=True)
        self._config["payload"]["timestamp6"] = Int(4)
        self._config["payload"]["real6"] = Int(2, sign=True)
        self._config["payload"]["imaginary6"] = Int(2, sign=True)

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        for i in range(1, 7):
            timestamp = packet["payload"][f"timestamp{i}"]
            data = {"timestamp": timestamp,
                    "real": packet["payload"][f"real{i}"],
                    "imaginary": packet["payload"][f"imaginary{i}"]}
            [packet["payload"].pop(key) for key in [f"timestamp{i}", f"real{i}", f"imaginary{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet


class PedometerDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.PEDOMETER: ['0xC4', '0x04']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x17',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 1,
                'steps': 0,
                'algo_status': 8193,
                'timestamp': 1776836792,
                'reserved': 0
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["steps"] = Int(4, sign=True)
        self._config["payload"]["algo_status"] = Int(2)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["reserved"] = Int(1)

    def get_dict(self, last_timestamp=None):
        """
        Postprocessing.
        """
        packet = super().get_dict()
        utils.update_timestamp(packet, last_timestamp)
        return packet


class TemperatureDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.TEMPERATURE: ['0xC4', '0x06']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x14',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 2,
                'timestamp': 1779692742,
                'skin_temperature': 30.1, # celsius
                'impedance': 79000 # ohm
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["skin_temperature"] = Int(2)
        self._config["payload"]["impedance"] = Int(2)

    def get_dict(self, last_timestamp=None):
        """
        Postprocessing.
        """
        packet = super().get_dict()
        packet["payload"]["skin_temperature"] = packet["payload"]["skin_temperature"] / 1000.0
        packet["payload"]["impedance"] = packet["payload"]["impedance"] * 100
        utils.update_timestamp(packet, last_timestamp)
        return packet


class PPGDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.PPG: ['0xC4', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x2E',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.NEW_STREAM_STATUS: ['0x43']>,
                'sequence_number': 9,
                'timestamp': 1782357951,
                'adpd_lib_state': 7,
                'hr': 0,
                'confidence': 0,
                'hr_type': 0,
                'rr_interval': 0,
                'debug_info': [ 0, 320, 50, 0, 5, 0, 320, 50, 978 ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["adpd_lib_state"] = Int(2)
        self._config["payload"]["hr"] = Int(2)
        self._config["payload"]["confidence"] = Int(2)
        self._config["payload"]["hr_type"] = Int(2)
        self._config["payload"]["rr_interval"] = Int(2)
        self._config["payload"]["debug_info"] = Array(-1, dimension=1, data_types=[Int(2)])

    def get_dict(self, last_timestamp=None):
        """
        Postprocessing.
        """
        packet = super().get_dict()
        utils.update_timestamp(packet, last_timestamp)
        return packet


class SYNCPPGDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.SYNC_PPG: ['0xC4', '0x05']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x48',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 119,
                'stream_data': [
                    {
                        'ppg_timestamp': 1782379042,
                        'ppg_data': 186278,
                        'adxl_timestamp': 1782378429,
                        'adxl_x': 48,
                        'adxl_y': 268,
                        'adxl_z': 62
                    },
                    {
                        'ppg_timestamp': 1782379682,
                        'ppg_data': 186278,
                        'adxl_timestamp': 1782379070,
                        'adxl_x': 55,
                        'adxl_y': 264,
                        'adxl_z': 60
                    },
                    {
                        'ppg_timestamp': 1782380323,
                        'ppg_data': 186289,
                        'adxl_timestamp': 1782379709,
                        'adxl_x': 68,
                        'adxl_y': 268,
                        'adxl_z': 57
                    },
                    {
                        'ppg_timestamp': 1782380962,
                        'ppg_data': 186305,
                        'adxl_timestamp': 1782380349,
                        'adxl_x': 60,
                        'adxl_y': 263,
                        'adxl_z': 62
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["ppg_timestamp1"] = Int(4)
        self._config["payload"]["adxl_timestamp1"] = Int(4)
        self._config["payload"]["ppg_timestamp2"] = Int(2)
        self._config["payload"]["ppg_timestamp3"] = Int(2)
        self._config["payload"]["ppg_timestamp4"] = Int(2)
        self._config["payload"]["adxl_timestamp2"] = Int(2)
        self._config["payload"]["adxl_timestamp3"] = Int(2)
        self._config["payload"]["adxl_timestamp4"] = Int(2)
        self._config["payload"]["ppg_data1"] = Int(4)
        self._config["payload"]["ppg_data2"] = Int(4)
        self._config["payload"]["ppg_data3"] = Int(4)
        self._config["payload"]["ppg_data4"] = Int(4)
        self._config["payload"]["adxl_x1"] = Int(2, sign=True)
        self._config["payload"]["adxl_x2"] = Int(2, sign=True)
        self._config["payload"]["adxl_x3"] = Int(2, sign=True)
        self._config["payload"]["adxl_x4"] = Int(2, sign=True)
        self._config["payload"]["adxl_y1"] = Int(2, sign=True)
        self._config["payload"]["adxl_y2"] = Int(2, sign=True)
        self._config["payload"]["adxl_y3"] = Int(2, sign=True)
        self._config["payload"]["adxl_y4"] = Int(2, sign=True)
        self._config["payload"]["adxl_z1"] = Int(2, sign=True)
        self._config["payload"]["adxl_z2"] = Int(2, sign=True)
        self._config["payload"]["adxl_z3"] = Int(2, sign=True)
        self._config["payload"]["adxl_z4"] = Int(2, sign=True)

    def get_dict(self, last_timestamp=None):
        """
        Postprocessing.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        ppg_timestamp = 0
        adxl_timestamp = 0
        for i in range(1, 5):
            ppg_timestamp += packet["payload"][f"ppg_timestamp{i}"]
            adxl_timestamp += packet["payload"][f"adxl_timestamp{i}"]
            data = {"ppg_timestamp": ppg_timestamp,
                    "ppg_data": packet["payload"][f"ppg_data{i}"],
                    "adxl_timestamp": adxl_timestamp,
                    "adxl_x": packet["payload"][f"adxl_x{i}"],
                    "adxl_y": packet["payload"][f"adxl_y{i}"],
                    "adxl_z": packet["payload"][f"adxl_z{i}"]}
            [packet["payload"].pop(key) for key in
             [f"ppg_timestamp{i}", f"ppg_data{i}", f"adxl_timestamp{i}", f"adxl_x{i}", f"adxl_y{i}", f"adxl_z{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp, is_syncppg=True)
        return packet


class SQIDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.SQI: ['0xC8', '0x0D']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x19',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'sqi': 2.537532566293521e-07,
                'sqi_slot': 42405,
                'algo_status': 0,
                'timestamp': 1786433199,
                'reserved': 0
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["sqi"] = Decimal(4)
        self._config["payload"]["sqi_slot"] = Int(2)
        self._config["payload"]["algo_status"] = Int(2)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["reserved"] = Int(1)

    def get_dict(self, last_timestamp=None):
        """
        Postprocessing.
        """
        packet = super().get_dict()
        utils.update_timestamp(packet, last_timestamp)
        return packet


class BIADataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.BIA: ['0xC4', '0x07']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x41',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 1,
                'data_type': 0,
                'stream_data': [
                    {
                        'timestamp': 1788107093,
                        'real': 0,
                        'imaginary': 0,
                        'frequency_index': 82
                    },
                    {
                        'timestamp': 1788114863,
                        'real': 0,
                        'imaginary': 0,
                        'frequency_index': 5
                    },
                    {
                        'timestamp': 1788122630,
                        'real': 0,
                        'imaginary': 0,
                        'frequency_index': 8
                    },
                    {
                        'timestamp': 1788130399,
                        'real': 0,
                        'imaginary': 0,
                        'frequency_index': 54
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["data_type"] = Int(1)
        self._config["payload"]["bia_info"] = Enums(1, enum_class=BIAAppInfo)
        self._config["payload"]["timestamp1"] = Int(4)
        self._config["payload"]["real1"] = Int(4, sign=True)
        self._config["payload"]["imaginary1"] = Int(4, sign=True)
        self._config["payload"]["frequency_index1"] = Int(4)
        self._config["payload"]["timestamp2"] = Int(4)
        self._config["payload"]["real2"] = Int(4, sign=True)
        self._config["payload"]["imaginary2"] = Int(4, sign=True)
        self._config["payload"]["frequency_index2"] = Int(4)
        self._config["payload"]["timestamp3"] = Int(4)
        self._config["payload"]["real3"] = Int(4, sign=True)
        self._config["payload"]["imaginary3"] = Int(4, sign=True)
        self._config["payload"]["frequency_index3"] = Int(4)
        self._config["payload"]["timestamp4"] = Int(4)
        self._config["payload"]["real4"] = Int(4, sign=True)
        self._config["payload"]["imaginary4"] = Int(4, sign=True)
        self._config["payload"]["frequency_index4"] = Int(4)

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        for i in range(1, 5):
            timestamp = packet["payload"][f"timestamp{i}"]
            data = {"timestamp": timestamp,
                    "real": packet["payload"][f"real{i}"],
                    "imaginary": packet["payload"][f"imaginary{i}"],
                    "frequency_index": packet["payload"][f"frequency_index{i}"]}
            [packet["payload"].pop(key) for key in
             [f"timestamp{i}", f"real{i}", f"imaginary{i}", f"frequency_index{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet


class AGCDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.AGC: ['0xC6', '0xB0']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 48,
                'checksum': 0
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.NEW_STREAM_STATUS: ['0x43']>,
                'sequence_number': 0,
                'timestamp': 1633077776386.271,
                'mts': [ 65535, 0, 0, 0, 0, 0 ],
                'setting': [ 7, 83, 0, 320, 58331, 50, 0, 0, 0, 0 ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["mts"] = Array(12, dimension=1, data_types=[Int(2)])
        self._config["payload"]["setting"] = Array(20, dimension=1, data_types=[Int(2)])

    def get_dict(self, last_timestamp=None):
        """
        Postprocessing.
        """
        packet = super().get_dict()
        utils.update_timestamp(packet, last_timestamp)
        return packet


class HRVDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.HRV: ['0xC6', '0xC0']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 46,
                'checksum': 0
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.NEW_STREAM_STATUS: ['0x43']>,
                'sequence_number': 0,
                'stream_data': [
                    {
                        'timestamp': 1633077488525.1702,
                        'rr_interval': 0,
                        'is_gap': 0,
                        'rmssd': 0
                    },
                    {
                        'timestamp': 1633077488527.2014,
                        'rr_interval': 0,
                        'is_gap': 0,
                        'rmssd': 0
                    },
                    {
                        'timestamp': 1633077488529.1702,
                        'rr_interval': 0,
                        'is_gap': 0,
                        'rmssd': 0
                    },
                    {
                        'timestamp': 1633077488531.2017,
                        'rr_interval': 0,
                        'is_gap': 0,
                        'rmssd': 0
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["timestamp1"] = Int(4)
        self._config["payload"]["rr_interval1"] = Int(2, sign=True)
        self._config["payload"]["is_gap1"] = Int(2)
        self._config["payload"]["rmssd1"] = Int(2)
        self._config["payload"]["timestamp2"] = Int(2)
        self._config["payload"]["rr_interval2"] = Int(2, sign=True)
        self._config["payload"]["is_gap2"] = Int(2)
        self._config["payload"]["rmssd2"] = Int(2)
        self._config["payload"]["timestamp3"] = Int(2)
        self._config["payload"]["rr_interval3"] = Int(2, sign=True)
        self._config["payload"]["is_gap3"] = Int(2)
        self._config["payload"]["rmssd3"] = Int(2)
        self._config["payload"]["timestamp4"] = Int(2)
        self._config["payload"]["rr_interval4"] = Int(2, sign=True)
        self._config["payload"]["is_gap4"] = Int(2)
        self._config["payload"]["rmssd4"] = Int(2)

    def get_dict(self, last_timestamp=None):
        """
        Postprocessing.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        timestamp = 0
        for i in range(1, 5):
            timestamp += packet["payload"][f"timestamp{i}"]
            data = {
                "timestamp": timestamp,
                "rr_interval": packet["payload"][f"rr_interval{i}"],
                "is_gap": packet["payload"][f"is_gap{i}"],
                "rmssd": packet["payload"][f"rmssd{i}"],
            }
            [packet["payload"].pop(key) for key in
             [f"timestamp{i}", f"rr_interval{i}", f"is_gap{i}", f"rmssd{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet


class KeyStreamDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.DISPLAY: ['0xC5', '0x03']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xB',
                'checksum': '0x0'
            },
            'payload': {
                'command': <DisplayCommand.KEY_STREAM_DATA: ['0x48']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'key_code': 18
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["key_code"] = Int(1)


class CapSenseStreamDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.CAP_SENSE_STREAM_DATA: ['0x82']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'position': 1,
                'value': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["position"] = Int(1)
        self._config["payload"]["value"] = Int(1)


class AD7156DataPacket(CommandPacket):
    """
    AD7156DataPacket
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["timestamp1"] = Int(4)
        self._config["payload"]["ch1_cap1"] = Int(2)
        self._config["payload"]["ch2_cap1"] = Int(2)
        self._config["payload"]["ch1_ADCCode1"] = Int(2)
        self._config["payload"]["ch2_ADCCode1"] = Int(2)
        self._config["payload"]["OUT1_val1"] = Int(1)
        self._config["payload"]["OUT2_val1"] = Int(1)
        self._config["payload"]["timestamp2"] = Int(2)
        self._config["payload"]["ch1_cap2"] = Int(2)
        self._config["payload"]["ch2_cap2"] = Int(2)
        self._config["payload"]["ch1_ADCCode2"] = Int(2)
        self._config["payload"]["ch2_ADCCode2"] = Int(2)
        self._config["payload"]["OUT1_val2"] = Int(1)
        self._config["payload"]["OUT2_val2"] = Int(1)
        self._config["payload"]["timestamp3"] = Int(2)
        self._config["payload"]["ch1_cap3"] = Int(2)
        self._config["payload"]["ch2_cap3"] = Int(2)
        self._config["payload"]["ch1_ADCCode3"] = Int(2)
        self._config["payload"]["ch2_ADCCode3"] = Int(2)
        self._config["payload"]["OUT1_val3"] = Int(1)
        self._config["payload"]["OUT2_val3"] = Int(1)
        self._config["payload"]["timestamp4"] = Int(2)
        self._config["payload"]["ch1_cap4"] = Int(2)
        self._config["payload"]["ch2_cap4"] = Int(2)
        self._config["payload"]["ch1_ADCCode4"] = Int(2)
        self._config["payload"]["ch2_ADCCode4"] = Int(2)
        self._config["payload"]["OUT1_val4"] = Int(1)
        self._config["payload"]["OUT2_val4"] = Int(1)

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        timestamp = 0
        for i in range(1, 5):
            timestamp += packet["payload"][f"timestamp{i}"]
            data = {
                "timestamp": timestamp,
                "ch1_cap": packet["payload"][f"ch1_cap{i}"],
                "ch2_cap": packet["payload"][f"ch2_cap{i}"],
                "ch1_ADCCode": packet["payload"][f"ch1_ADCCode{i}"],
                "ch2_ADCCode": packet["payload"][f"ch2_ADCCode{i}"],
                "OUT1_val": packet["payload"][f"OUT1_val{i}"],
                "OUT2_val": packet["payload"][f"OUT2_val{i}"]
            }
            [packet["payload"].pop(key) for key in [f"timestamp{i}", f"ch1_cap{i}", f"ch2_cap{i}",
                                                    f"ch1_ADCCode{i}", f"ch2_ADCCode{i}",
                                                    f"OUT1_val{i}", f"OUT2_val{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet


class BCMDataPacket(CommandPacket):
    """
    BCMDataPacket
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_num"] = Int(2)
        self._config["payload"]["ffm_estimated"] = Decimal(4)
        self._config["payload"]["bmi"] = Decimal(4)
        self._config["payload"]["fat_percent"] = Decimal(4)
        self._config["payload"]["timestamp"] = Int(4)

    def get_dict(self, last_timestamp=None):
        """
        Postprocessing.
        """
        packet = super().get_dict()
        utils.update_timestamp(packet, last_timestamp)
        return packet


class SHMAX86178DataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.ADPD6: ['0xC8', '0x27']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x2C',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'op_mode': 1,
                'channel_num': 2,
                'timestamp': 1751731879,
                'sample_num': 2,
                'sh_data': [ 351762, 351755 ],
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["op_mode"] = Int(1)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["channel_num"] = Int(1)
        self._config["payload"]["sample_num"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=1, data_types=[Int(1)])

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["sh_data"] = []
        data_size = 3
        sample_num = packet["payload"]["sample_num"]
        for i in range(0, sample_num * data_size, data_size):
            data = packet["payload"]["data"][i: i + data_size]
            sh_data = utils.join_multi_length_packets(data)
            packet["payload"]["sh_data"].append(sh_data)
        del packet["payload"]["data"]
        utils.update_timestamp(packet, last_timestamp)
        return packet

class SHMAX86178ECGDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.SENSORHUB_MAX86178_ECG_STREAM: ['0xC8', '0x32']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x2C',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'op_mode': 1,
                'timestamp': 1751731879,
                'ecg_data': [ 351762, 351755, ... ],
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["op_mode"] = Int(1)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["lead_status"] = Int(1)
        self._config["payload"]["ecg_data"] = Array(-1, dimension=1, data_types=[Int(4)])

    def get_dict(self, last_timestamp=None):
        """
        Convert ECG data into signed values
        """
        packet = super().get_dict()
        for i in range(12):
            val = packet["payload"]["ecg_data"][i]
            packet["payload"]["ecg_data"][i] = (val & ((1<<17) - 1)) - (val & (1<<17))
        utils.update_timestamp(packet, last_timestamp)
        return packet
        
class SHMAX86178BIOZDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.SENSORHUB_MAX86178_BIOZ_STREAM: ['0xC8', '0x36']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x2C',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'op_mode': 1,
                'timestamp': 1751731879,
                'ecg_data': [ 351762, 351755, ... ],
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["op_mode"] = Int(1)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["bioz_data"] = Int(4)

    def get_dict(self, last_timestamp=None):
        """
        Postprocess BIOZ data
        """
        packet = super().get_dict()
        utils.update_timestamp(packet, last_timestamp)
        return packet
    
class SHRegConfPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.SENSORHUB_REG_CONF: ['0xC8', '0x2D']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x2C',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'op_mode': 1,
                'timestamp': 1751731879,
                'led_curr': [ 3A, 1B, 1A, 1A ],
                'tint': ['3A']
                'avg_smpl': ['2A']
                'reg_sample_average' : ['1A']
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["op_mode_id"] = Int(1)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["led_curr1"] = Decimal(4)
        self._config["payload"]["tint1"] = Int(1)
        self._config["payload"]["avg_smpl1"] = Int(1)
        self._config["payload"]["led_curr2"] = Decimal(4)
        self._config["payload"]["tint2"] = Int(1)
        self._config["payload"]["avg_smpl2"] = Int(1)
        self._config["payload"]["led_curr3"] = Decimal(4)
        self._config["payload"]["tint3"] = Int(1)
        self._config["payload"]["avg_smpl3"] = Int(1)
        self._config["payload"]["reg_sample_average"] = Int(1)

    def get_dict(self, last_timestamp=None):
        """
        Postprocessing.
        """
        packet = super().get_dict()
        packet["payload"]["reg_conf"] = []
        for i in range(1, 4):
            data = {
                "led_curr": packet["payload"][f"led_curr{i}"],
                "tint": packet["payload"][f"tint{i}"],
                "avg_smpl": packet["payload"][f"avg_smpl{i}"]
            }
            [packet["payload"].pop(key) for key in [f"led_curr{i}", f"tint{i}", f"avg_smpl{i}"]]
            packet["payload"]["reg_conf"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet

class SHADXLDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.ADXL: ['0xC8', '0x2C']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x37',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 395,
                'op_mode_id': 0,
                'stream_data': [
                    {
                        'timestamp': 1767361372,
                        'x': -85,
                        'y': 90,
                        'z': 55
                    },
                    {
                        'timestamp': 1767362027,
                        'x': -80,
                        'y': 88,
                        'z': 55
                    },
                    {
                        'timestamp': 1767362682,
                        'x': 40,
                        'y': 274,
                        'z': 79
                    },
                    {
                        'timestamp': 1767363337,
                        'x': 70,
                        'y': 273,
                        'z': 54
                    },
                    {
                        'timestamp': 1767363931,
                        'x': 57,
                        'y': 257,
                        'z': 48
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["op_mode_id"] = Int(1)
        self._config["payload"]["timestamp1"] = Int(4)
        self._config["payload"]["x1"] = Int(2, sign=True)
        self._config["payload"]["y1"] = Int(2, sign=True)
        self._config["payload"]["z1"] = Int(2, sign=True)
        self._config["payload"]["timestamp2"] = Int(2)
        self._config["payload"]["x2"] = Int(2, sign=True)
        self._config["payload"]["y2"] = Int(2, sign=True)
        self._config["payload"]["z2"] = Int(2, sign=True)
        self._config["payload"]["timestamp3"] = Int(2)
        self._config["payload"]["x3"] = Int(2, sign=True)
        self._config["payload"]["y3"] = Int(2, sign=True)
        self._config["payload"]["z3"] = Int(2, sign=True)
        self._config["payload"]["timestamp4"] = Int(2)
        self._config["payload"]["x4"] = Int(2, sign=True)
        self._config["payload"]["y4"] = Int(2, sign=True)
        self._config["payload"]["z4"] = Int(2, sign=True)
        self._config["payload"]["timestamp5"] = Int(2)
        self._config["payload"]["x5"] = Int(2, sign=True)
        self._config["payload"]["y5"] = Int(2, sign=True)
        self._config["payload"]["z5"] = Int(2, sign=True)

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        timestamp = 0
        for i in range(1, 6):
            timestamp += packet["payload"][f"timestamp{i}"]
            data = {
                "timestamp": timestamp,
                "x": packet["payload"][f"x{i}"],
                "y": packet["payload"][f"y{i}"],
                "z": packet["payload"][f"z{i}"]
            }
            [packet["payload"].pop(key) for key in [f"timestamp{i}", f"x{i}", f"y{i}", f"z{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet

class SHHRMDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.SENSORHUB_HRM_STREAM: ['0xC8', '0x2B']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 33,
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 395,
                'op_mode_id': 1,
                'stream_data': [
                    {
                        'timestamp': 1767361372,
                        'hr': 0,
                        'hr_conf': 0,
                        'rr': 11,
                        'rr_conf': 0,
                        'activity_class': 0,
                    },
                    {
                        'timestamp': 1767361372,
                        'hr': 0,
                        'hr_conf': 0,
                        'rr': 11,
                        'rr_conf': 0,
                        'activity_class': 0,
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["op_mode_id"] = Int(1)
        self._config["payload"]["timestamp1"] = Int(4)
        self._config["payload"]["hr1"] = Int(2, sign=True)
        self._config["payload"]["hr_conf1"] = Int(1, sign=False)
        self._config["payload"]["rr1"] = Int(2, sign=False)
        self._config["payload"]["rr_conf1"] = Int(1, sign=False)
        self._config["payload"]["activity_class1"] = Int(1, sign=False)
        self._config["payload"]["timestamp2"] = Int(2)
        self._config["payload"]["hr2"] = Int(2, sign=True)
        self._config["payload"]["hr_conf2"] = Int(1, sign=False)
        self._config["payload"]["rr2"] = Int(2, sign=False)
        self._config["payload"]["rr_conf2"] = Int(1, sign=False)
        self._config["payload"]["activity_class2"] = Int(1, sign=False)

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        timestamp = 0
        for i in range(1, 3):
            timestamp += packet["payload"][f"timestamp{i}"]
            data = {
                "timestamp": timestamp,
                "hr": packet["payload"][f"hr{i}"],
                "hr_conf": packet["payload"][f"hr_conf{i}"],
                "rr": packet["payload"][f"rr{i}"],
                "rr_conf": packet["payload"][f"rr_conf{i}"],
                "activity_class": packet["payload"][f"activity_class{i}"]
            }
            [packet["payload"].pop(key) for key in [f"timestamp{i}", f"hr{i}", f"hr_conf{i}", f"rr{i}", f"rr_conf{i}", f"activity_class{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet


class SHSPO2DataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.SENSORHUB_HRM_STREAM: ['0xC8', '0x2A']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 43,
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 395,
                'op_mode_id': 1,
                'stream_data': [
                    {
                        'r': 0,
                        'spo2_conf': 0,
                        'spo2': 0,
                        'percentComplete': 0,
                        'lowQualitySignalFlag': 1,
                        'motionFlag': 1,
                        'lowPiFlag': 1,
                        'unreliableRFlag': 0,
                        'spo2_state': 0,
                        'scd_contact_state': 0
                    },
                    {
                       'r': 0,
                        'spo2_conf': 0,
                        'spo2': 0,
                        'percentComplete': 0,
                        'lowQualitySignalFlag': 1,
                        'motionFlag': 1,
                        'lowPiFlag': 1,
                        'unreliableRFlag': 0,
                        'spo2_state': 0,
                        'scd_contact_state': 0
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["op_mode_id"] = Int(1)
        self._config["payload"]["timestamp1"] = Int(4)
        self._config["payload"]["r1"] = Int(2, sign=True)
        self._config["payload"]["spo2_conf1"] = Int(1, sign=False)
        self._config["payload"]["spo21"] = Int(2, sign=False)
        self._config["payload"]["percentComplete1"] = Int(1, sign=False)
        self._config["payload"]["lowQualitySignalFlag1"] = Int(1, sign=False)
        self._config["payload"]["motionFlag1"] = Int(1, sign=False)
        self._config["payload"]["lowPiFlag1"] = Int(1, sign=False)
        self._config["payload"]["unreliableRFlag1"] = Int(1, sign=False)
        self._config["payload"]["spo2_state1"] = Int(1, sign=False)
        self._config["payload"]["scd_contact_state1"] = Int(1, sign=False)
        self._config["payload"]["timestamp2"] = Int(2)
        self._config["payload"]["r2"] = Int(2, sign=True)
        self._config["payload"]["spo2_conf2"] = Int(1, sign=False)
        self._config["payload"]["spo22"] = Int(2, sign=False)
        self._config["payload"]["percentComplete2"] = Int(1, sign=False)
        self._config["payload"]["lowQualitySignalFlag2"] = Int(1, sign=False)
        self._config["payload"]["motionFlag2"] = Int(1, sign=False)
        self._config["payload"]["lowPiFlag2"] = Int(1, sign=False)
        self._config["payload"]["unreliableRFlag2"] = Int(1, sign=False)
        self._config["payload"]["spo2_state2"] = Int(1, sign=False)
        self._config["payload"]["scd_contact_state2"] = Int(1, sign=False)

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        timestamp = 0
        for i in range(1, 3):
            timestamp += packet["payload"][f"timestamp{i}"]
            data = {
                "timestamp": timestamp,
                "r": packet["payload"][f"r{i}"],
                "spo2_conf": packet["payload"][f"spo2_conf{i}"],
                "spo2": packet["payload"][f"spo2{i}"],
                "percentComplete": packet["payload"][f"percentComplete{i}"],
                "lowQualitySignalFlag": packet["payload"][f"lowQualitySignalFlag{i}"],
                "motionFlag": packet["payload"][f"motionFlag{i}"],
                "lowPiFlag": packet["payload"][f"lowPiFlag{i}"],
                "unreliableRFlag": packet["payload"][f"unreliableRFlag{i}"],
                "spo2_state": packet["payload"][f"spo2_state{i}"],
                "scd_contact_state": packet["payload"][f"scd_contact_state{i}"]
            }
            [packet["payload"].pop(key) for key in [f"timestamp{i}", f"r{i}", f"spo2_conf{i}", f"spo2{i}", f"percentComplete{i}", f"lowQualitySignalFlag{i}",
                                                    f"motionFlag{i}", f"lowPiFlag{i}", f"unreliableRFlag{i}", f"spo2_state{i}", f"scd_contact_state{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet

class SHRRDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.SENSORHUB_RR_STREAM: ['0xC8', '0x2E']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 43,
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 395,
                'op_mode_id': 1,
                'stream_data': [
                    {
                        'timestamp': 15656161576
                        'irCardiacRespRmsRatio': 0,
                        'irRangeRmsRatio': 0,
                        'irGreenCorrCoefficient': 0,
                        'greenRrFromIbi': 0,
                        'irBaselineRr': 1,
                        'stdIbiMSec': 1,
                        'avgHrBpm': 1,
                        'greenRrFromIbiQuality': 0,
                        'rr_mlp_output': 0,
                        'rr_median_output': 0,
                        'rr_confidence': 0
                    },
                    {
                        'timestamp': 15656161616
                        'irCardiacRespRmsRatio': 0,
                        'irRangeRmsRatio': 0,
                        'irGreenCorrCoefficient': 0,
                        'greenRrFromIbi': 0,
                        'irBaselineRr': 1,
                        'stdIbiMSec': 1,
                        'avgHrBpm': 1,
                        'greenRrFromIbiQuality': 0,
                        'rr_mlp_output': 0,
                        'rr_median_output': 0,
                        'rr_confidence': 0
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["op_mode_id"] = Int(1)
        self._config["payload"]["timestamp1"] = Int(4)
        self._config["payload"]["irCardiacRespRmsRatio1"] = Int(2, sign=True)
        self._config["payload"]["irRangeRmsRatio1"] = Int(2, sign=True)
        self._config["payload"]["irGreenCorrCoefficient1"] = Int(2, sign=True)
        self._config["payload"]["greenRrFromIbi1"] = Int(2, sign=True)
        self._config["payload"]["irBaselineRr1"] = Int(2, sign=True)
        self._config["payload"]["stdIbiMSec1"] = Int(2, sign=True)
        self._config["payload"]["avgHrBpm1"] = Int(2, sign=True)
        self._config["payload"]["greenRrFromIbiQuality1"] = Int(2, sign=True)
        self._config["payload"]["rr_mlp_output1"] = Int(2, sign=True)
        self._config["payload"]["rr_median_output1"] = Int(2, sign=True)
        self._config["payload"]["rr_confidence1"] = Int(2, sign=True)
        self._config["payload"]["timestamp2"] = Int(2)
        self._config["payload"]["irCardiacRespRmsRatio2"] = Int(2, sign=True)
        self._config["payload"]["irRangeRmsRatio2"] = Int(2, sign=True)
        self._config["payload"]["irGreenCorrCoefficient2"] = Int(2, sign=True)
        self._config["payload"]["greenRrFromIbi2"] = Int(2, sign=True)
        self._config["payload"]["irBaselineRr2"] = Int(2, sign=True)
        self._config["payload"]["stdIbiMSec2"] = Int(2, sign=True)
        self._config["payload"]["avgHrBpm2"] = Int(2, sign=True)
        self._config["payload"]["greenRrFromIbiQuality2"] = Int(2, sign=True)
        self._config["payload"]["rr_mlp_output2"] = Int(2, sign=True)
        self._config["payload"]["rr_median_output2"] = Int(2, sign=True)
        self._config["payload"]["rr_confidence2"] = Int(2, sign=True)

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        timestamp = 0
        for i in range(1, 3):
            timestamp += packet["payload"][f"timestamp{i}"]
            data = {
                "timestamp": timestamp,
                "irCardiacRespRmsRatio": packet["payload"][f"irCardiacRespRmsRatio{i}"]/100.0,
                "irRangeRmsRatio": packet["payload"][f"irRangeRmsRatio{i}"]/100.0,
                "irGreenCorrCoefficient": packet["payload"][f"irGreenCorrCoefficient{i}"]/100.0,
                "greenRrFromIbi": packet["payload"][f"greenRrFromIbi{i}"]/100.0,
                "irBaselineRr": packet["payload"][f"irBaselineRr{i}"]/100.0,
                "stdIbiMSec": packet["payload"][f"stdIbiMSec{i}"]/100.0,
                "avgHrBpm": packet["payload"][f"avgHrBpm{i}"]/100.0,
                "greenRrFromIbiQuality": packet["payload"][f"greenRrFromIbiQuality{i}"]/100.0,
                "rr_mlp_output": packet["payload"][f"rr_mlp_output{i}"]/100.0,
                "rr_median_output": packet["payload"][f"rr_median_output{i}"]/100.0,
                "rr_confidence": packet["payload"][f"rr_confidence{i}"]/100.0
            }
            [packet["payload"].pop(key) for key in [f"timestamp{i}", f"irCardiacRespRmsRatio{i}", f"irRangeRmsRatio{i}", f"irGreenCorrCoefficient{i}", f"greenRrFromIbi{i}", f"irBaselineRr{i}",
                                                    f"stdIbiMSec{i}", f"avgHrBpm{i}", f"greenRrFromIbiQuality{i}", f"rr_mlp_output{i}", f"rr_median_output{i}", f"rr_confidence{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet

class SHAMADataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.SENSORHUB_AMA_STREAM: ['0xC8', '0x37']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 43,
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 395,
                'op_mode_id': 1,
                'stream_data': [
                    {
                        'timestamp': 15656161576
                        'activity_class': 0,
                        'total_activity_time': 0,
                        'total_walk_steps': 0,
                        'total_distance': 0
                    },
                    {
                        'timestamp': 15656161576
                        'activity_class': 0,
                        'total_activity_time': 0,
                        'total_walk_steps': 0,
                        'total_distance': 0
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["op_mode_id"] = Int(1)
        self._config["payload"]["timestamp1"] = Int(4)
        self._config["payload"]["activity_class1"] = Int(1, sign=False)
        self._config["payload"]["total_activity_time1"] = Int(4, sign=False)
        self._config["payload"]["total_walk_steps1"] = Int(4, sign=False)
        self._config["payload"]["total_distance1"] = Int(4, sign=False)
        self._config["payload"]["timestamp2"] = Int(2)
        self._config["payload"]["activity_class2"] = Int(1, sign=False)
        self._config["payload"]["total_activity_time2"] = Int(4, sign=False)
        self._config["payload"]["total_walk_steps2"] = Int(4, sign=False)
        self._config["payload"]["total_distance2"] = Int(4, sign=False)

    def get_dict(self, last_timestamp=None):
        """
        Reorganising of stream data in stream_data key.
        """
        packet = super().get_dict()
        packet["payload"]["stream_data"] = []
        timestamp = 0
        for i in range(1, 3):
            timestamp += packet["payload"][f"timestamp{i}"]
            data = {
                "timestamp": timestamp,
                "activity_class": packet["payload"][f"activity_class{i}"],
                "total_activity_time": packet["payload"][f"total_activity_time{i}"],
                "total_walk_steps": packet["payload"][f"total_walk_steps{i}"],
                "total_distance": packet["payload"][f"total_distance{i}"]/10.0,
            }
            [packet["payload"].pop(key) for key in [f"timestamp{i}", f"activity_class{i}", f"total_activity_time{i}", f"total_walk_steps{i}", f"total_distance{i}"]]
            packet["payload"]["stream_data"].append(data)
        utils.update_timestamp(packet, last_timestamp)
        return packet
    
class MAX30208TemperatureDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.MAX30208_TEMPERATURE_STREAM: ['0xC4', '0x06']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x14',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 2,
                'timestamp': 1779692742,
                'skin_temperature': 30.1, # celsius
                'impedance': 79000 # ohm
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = Int(2)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["temperature"] = Int(2)

    def get_dict(self, last_timestamp=None):
        """
        Postprocessing.
        """
        packet = super().get_dict()
        packet["payload"]["temperature"] = packet["payload"]["temperature"] * 0.005
        utils.update_timestamp(packet, last_timestamp)
        return packet
