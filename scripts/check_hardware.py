#!/usr/bin/env python3
"""Regression guards for specific defects found in the original hardware.
Independent expectations are taken from linked manufacturer pin/reference tables.
"""
import json
from pathlib import Path
from kicad_data import parse,children,one
R=Path(__file__).resolve().parents[1];d=json.loads((R/'design/rev-b-netmap.json').read_text())
def check(ref,m):
 for p,n in m.items():assert d[ref]['nets'].get(str(p))==n,f'{ref} pin {p}: expected {n}'
check('U2',{3:'PWRKEY_1V8',4:'RESET_1V8',15:'VDD_EXT',17:'USIM_DATA',18:'USIM_RST',19:'USIM_CLK',20:'USIM_VDD',49:'MODEM_STATUS_1V8',59:'RF_AUX',66:'MODEM_RTS_1V8',67:'MODEM_CTS_1V8',68:'MODEM_RXD_1V8',71:'MODEM_TXD_1V8',79:'RF_GNSS',82:'RF_MAIN'})
for pin in [38,39,62,63]:check('U2',{pin:'VBAT_MODEM'})
for pin in [88,89,90,91,92,99,100,101,102,103,104,105,107,111]:check('U2',{pin:''})
check('U3',{1:'VDD_EXT',8:'UART_OE',14:'+3.3V'})
check('R11',{1:'VDD_EXT',2:'UART_OE'});check('R24',{1:'UART_OE',2:'GND'})
check('U7',{1:'VDD_EXT',2:'GND',3:'MODEM_STATUS_1V8',4:'MODEM_STATUS',5:'VDD_EXT',6:'+3.3V'})
check('D2',{1:'USB_D+',6:'USB_D+',3:'USB_D-',4:'USB_D-',2:'GND',5:'VBUS'})
for ref,net in [('D6','USIM_CLK_SIM'),('D7','USIM_DAT_SIM'),('D9','USIM_RST_SIM')]:check(ref,{1:net,2:'GND'})
check('J3',{6:''});check('LED1',{1:'GND',2:'USER_LED_R'})
check('J6',{1:'',4:'',8:'GND',15:'VCC_EPD',16:'VCC_EPD',17:'GND',18:'EPD_VDD',19:'',21:'EPD_PREVGH',23:'EPD_PREVGL'})
check('C42',{1:'EPD_VDD',2:'GND'});check('D3',{1:'EPD_PREVGH',2:'EPD_SW'});check('D4',{1:'GND',2:'EPD_FLY'});check('D5',{1:'EPD_FLY',2:'EPD_PREVGL'});check('C40',{1:'EPD_SW',2:'EPD_FLY'})
assert d['R10']['value']=='2.2R';assert d['L2']['value']=='47uH SRN4018-470M';assert d['Q9']['footprint']=='Package_TO_SOT_SMD:SOT-323_SC-70'
check('U1',{15:'',24:'BAT_SENSE_EN',13:'MCU_USB_D-',14:'MCU_USB_D+'})
assert d['U1']['value']=='ESP32-S3-WROOM-1-N8';assert d['U5']['value']=='AP2112K-3.3TRG1'
assert 'U4' not in d,'no onboard charging path in revision B'
fp=parse((R/'Cellular.pretty/SIM7600G_H_135.kicad_mod').read_text());pads=children(fp,'pad')
assert len(pads)==135 and {p[1]for p in pads}=={str(i)for i in range(1,136)}
for pin,at in {'1':(9.5,-14.7),'20':(-9.5,-14.7),'38':(-14.7,7.5),'62':(14.7,8.5),'79':(14.7,-8.5),'82':(-10.5,14.7),'120':(6,-6),'135':(-6,6)}.items():
 p=next(p for p in pads if p[1]==pin);assert tuple(map(float,one(p,'at')[1:3]))==at,(pin,one(p,'at'))
assert len(children(fp,'zone'))==2
print('PASS: manufacturer-based modem pin map / footprint, voltage domains, SIM protection, display topology, LED polarity and USB guards.')
print('These checks cannot establish RF performance, footprint fit or physical operation.')
