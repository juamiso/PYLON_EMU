from __future__ import print_function
import cantools
import time
from binascii import hexlify
import can

#TO debug with no CAN physical interface use
#sudo ip link add dev vcan0 type vcan
#sudo ip link set up vcan0

db = cantools.db.load_file('pylon_CAN_210124.dbc')

msg_data_Network_alive_msg = {
    'Alive_packet': 0}

msg_data_Battery_SoC_SoH = {
    'SoC': 80,
    'SoH': 100}

msg_data_Battery_Request = {
 'Full_charge_req' : 0,
 'Force_charge_req_II' : 0,
 'Force_charge_req_I' : 0,
 'Discharge_enable' : 1,
 'Charge_enable' : 1}

msg_data_Battery_actual_values_UIt = {
  'Battery_temperature' : 20,
  'Battery_current' : 0,
  'Battery_voltage' : 0}

msg_data_Battery_limits = {
 'Battery_discharge_current_limit' : -120,
 'Battery_charge_current_limit' : 120,
 'Battery_charge_voltage' : 56,
 'Battery_discharge_voltage' : 49 }

msg_data_Battery_Error_Warnings = {
 'Module_numbers' : 16,
 'Charge_current_high_WARN' : 0,
 'Internal_Error_WARN' : 0,
 'voltage_low_WARN' : 0,
 'voltage_high_WARN' : 0,
 'Temperature_high_WARN' : 0,
 'Temperature_low_WARN' : 0,
 'Discharge_current_high_WARN' : 0,
 'Charge_overcurrent_ERR' : 0,
 'System_Error' : 0,
 'Overvoltage_ERR' : 0,
 'Undervoltage_ERR' : 0,
 'Overtemperature_ERR' : 0,
 'Undertemperature_ERR' : 0,
 'Overcurrent_discharge_ERR' : 0 }

Network_alive_msg = db.get_message_by_name('Network_alive_msg')
Battery_SoC_SoH = db.get_message_by_name('Battery_SoC_SoH')
Battery_Manufacturer = db.get_message_by_name('Battery_Manufacturer')
Battery_Request = db.get_message_by_name('Battery_Request')
Battery_actual_values_UIt = db.get_message_by_name('Battery_actual_values_UIt')
Battery_limits = db.get_message_by_name('Battery_limits')
Battery_Error_Warnings = db.get_message_by_name('Battery_Error_Warnings')

msg_data_enc_Network_alive_msg = db.encode_message('Network_alive_msg', msg_data_Network_alive_msg)
msg_data_enc_Battery_SoC_SoH = db.encode_message('Battery_SoC_SoH', msg_data_Battery_SoC_SoH)
msg_data_enc_Battery_Manufacturer = b'\x50\x59\x4c\x4f\x4e\x00\x00\x00'
#hex(ord('P'))
#'0x50'
#hex(ord('Y'))
#'0x59'
#hex(ord('L'))
#'0x4c'
#hex(ord('O'))
#'0x4f'
#hex(ord('N'))
#'0x4e'

msg_data_enc_Battery_Request = db.encode_message('Battery_Request', msg_data_Battery_Request)
msg_data_enc_Battery_actual_values_UIt = db.encode_message('Battery_actual_values_UIt', msg_data_Battery_actual_values_UIt)
msg_data_enc_Battery_limits = db.encode_message('Battery_limits', msg_data_Battery_limits)
msg_data_enc_Battery_Error_Warnings = db.encode_message('Battery_Error_Warnings', msg_data_Battery_Error_Warnings)

msg_tx_Network_alive_msg = can.Message(arbitration_id=Network_alive_msg.frame_id, data=msg_data_enc_Network_alive_msg, is_extended_id=False)
msg_tx_Battery_SoC_SoH = can.Message(arbitration_id=Battery_SoC_SoH.frame_id, data=msg_data_enc_Battery_SoC_SoH, is_extended_id=False)
msg_tx_Battery_Manufacturer = can.Message(arbitration_id=Battery_Manufacturer.frame_id, data=msg_data_enc_Battery_Manufacturer, is_extended_id=False)
msg_tx_Battery_Request = can.Message(arbitration_id=Battery_Request.frame_id, data=msg_data_enc_Battery_Request, is_extended_id=False)
msg_tx_Battery_actual_values_UIt = can.Message(arbitration_id=Battery_actual_values_UIt.frame_id, data=msg_data_enc_Battery_actual_values_UIt, is_extended_id=False)
msg_tx_Battery_limits = can.Message(arbitration_id=Battery_limits.frame_id, data=msg_data_enc_Battery_limits, is_extended_id=False)
msg_tx_Battery_Error_Warnings = can.Message(arbitration_id=Battery_Error_Warnings.frame_id, data=msg_data_enc_Battery_Error_Warnings, is_extended_id=False)


def test_periodic_send_with_modifying_data(bus):
    Alive_packet = 0 #counter
    SoC = 50
    Bat_t = 25
    Bat_i = -10
    Bat_U = 52
    print("Starting to send a message every 1s")
    task_tx_Network_alive_msg = bus.send_periodic(msg_tx_Network_alive_msg, 1)
    task_tx_Battery_SoC_SoH = bus.send_periodic(msg_tx_Battery_SoC_SoH, 1)
    task_tx_Battery_Manufacturer = bus.send_periodic(msg_tx_Battery_Manufacturer, 1)
    task_tx_Battery_Request = bus.send_periodic(msg_tx_Battery_Request, 1)
    task_tx_Battery_actual_values_UIt = bus.send_periodic(msg_tx_Battery_actual_values_UIt, 1)
    task_tx_Battery_limits = bus.send_periodic(msg_tx_Battery_limits, 1)
    task_tx_Battery_Error_Warnings = bus.send_periodic(msg_tx_Battery_Error_Warnings, 1)
    time.sleep(0.5)
#    if not isinstance(task, can.ModifiableCyclicTaskABC):
#        print("This interface doesn't seem to support modification")
#        task.stop()
#        return
    while True:
      Alive_packet = Alive_packet+1
      print("updating data ", Alive_packet )
      msg_tx_Network_alive_msg.data = db.encode_message('Network_alive_msg',{'Alive_packet': Alive_packet})
      msg_tx_Battery_SoC_SoH.data = db.encode_message('Battery_SoC_SoH',{'SoC': SoC,
        'SoH': 100})
      msg_tx_Battery_actual_values_UIt.data = db.encode_message('Battery_actual_values_UIt',{
        'Battery_temperature' : Bat_t,
        'Battery_current' : Bat_i,
        'Battery_voltage' : Bat_U})

      task_tx_Network_alive_msg.modify_data(msg_tx_Network_alive_msg)
      task_tx_Battery_SoC_SoH.modify_data(msg_tx_Battery_SoC_SoH)
      task_tx_Battery_actual_values_UIt.modify_data(msg_tx_Battery_actual_values_UIt)

      if Alive_packet >= 4611686018427387904:
        Alive_packet = 2

      time.sleep(1)
    task.stop()
    print("done")


if __name__ == "__main__":

    reset_msg = can.Message(arbitration_id=0x00, data=[0, 0, 0, 0, 0, 0], is_extended_id=False)

    for interface, channel in [
        ('socketcan', 'vcan0'),
        #('ixxat', 0)
    ]:
        print("Carrying out cyclic tests with {} interface".format(interface))
        bus = can.Bus(interface=interface, channel=channel, bitrate=500000)
        test_periodic_send_with_modifying_data(bus)
        bus.shutdown()

    time.sleep(5)
