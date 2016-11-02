#!/usr/bin/python3
#

#  Copyright (C)  2011-2012  the pyAlienFX team
#                 2014-2016  Rafael Senties Martinelli <rafael@senties-martinelli.com>
#
#  This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License 3 as published by
#   the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA.


import sys
import os
import time
import usb
from copy import copy

# local imports
from Computers import AllComputers, CommonConf


class Driver(AllComputers):
    def __init__(self):
        #Define I/O Reqquest types
        self.SEND_REQUEST_TYPE = 0x21
        self.SEND_REQUEST = 0x09
        self.SEND_VALUE = 0x202
        self.SEND_INDEX = 0x00
        self.READ_REQUEST_TYPE = 0xa1
        self.READ_REQUEST = 0x01
        self.READ_VALUE = 0x101
        self.READ_INDEX = 0x0
         
        #Initializing !
        # find our device 
        if not self.FindDevice():
            self.not_found=True
            return 
        else:
            self.not_found=False
            
        self.Take_over()
    
    def FindDevice(self, id_vendor=False, id_product=False):
        """
            Look for all the devices listed in the Computer file, if found return True, else return False.
            If a computer is found, the device is loaded, as well as all the parameters for the computer 
            (which are in the Computer)
        """
        
        #
        #   Block Testing
        #
        if id_vendor or id_product:
            """
                Normally if the id_vendor or id_product are supplied it is because the block
                testing, and the block testing needs both so:
            """
            if not id_vendor or not id_product:
                return False
            
            try:
                dev = usb.core.find(idVendor=id_vendor, idProduct=id_product)
                
                if dev != None:
                    
                    self.computer_name='Block Testing'
                    self.vendorId = id_vendor
                    self.productId = id_product
                    self.dev=dev
                    self.computer = CommonConf()
                    
                    self.Take_over()
                    return True
            except Exception as e:
                print(e)
                
            return False
        
        #        
        #   Normal initialization
        #
        for computer in sorted(self.computerList.keys()):
            dev = usb.core.find(idVendor=self.computerList[computer].vendorId, idProduct=self.computerList[computer].productId)

            if dev != None:
            
                # This hack was made to differenciate the M14XR1 from the R2
                if computer == 'M14XR1' and 'Gaming' in str(dev):
                    computer='M14XR2'
                
                self.computer_name = computer
                self.computer = self.computerList[computer].computer
                self.vendorId = self.computerList[computer].vendorId
                self.productId = self.computerList[computer].productId
                self.dev = dev
                
                return True
                
        return False
    
    def WriteDevice(self,MSG):
        if len(MSG[0].packet) == self.computer.DATA_LENGTH:
            for msg in MSG:
                time.sleep(0.02)
                self.dev.ctrl_transfer(self.SEND_REQUEST_TYPE, self.SEND_REQUEST, self.SEND_VALUE, self.SEND_INDEX, msg.packet)
        else:
            self.dev.ctrl_transfer(self.SEND_REQUEST_TYPE, self.SEND_REQUEST, self.SEND_VALUE, self.SEND_INDEX, MSG)
            
    def ReadDevice(self,msg):
        msg = self.dev.ctrl_transfer(self.READ_REQUEST_TYPE, self.READ_REQUEST, self.READ_VALUE, self.READ_INDEX, len(msg[0].packet))

        return msg
        
        
    def Take_over(self):
        try:
            self.dev.set_configuration()
        except:
            self.dev.detach_kernel_driver(0)
            try:
                self.dev.set_configuration()
            except Exception as e:
                raise DeviceNotFound("Can't set the configuration. Error: {}".format(e))
                sys.exit(1)


class Controller:
    def __init__(self, driver):
        self.driver = driver

    def Bye(self):
        sys.exit(0)
        
    def Set_Loop(self,action):
        self.WaitForOk()
        self.driver.WriteDevice(action)
    
    def Set_Loop_Conf(self, Save=False, block=0x01):
        self.request = Constructor(self.driver, Save, block)
    
    def Add_Loop_Conf(self, area, mode, color1, color2=None):
    
        if type(area) != list:
            area = self.request.Area(area)
            
        if type(color1) != list:
            color1 = self.request.Color(color1)
            
        if type(color2) != list and color2:
            color2 = self.request.Color2(color2)
            
        if mode == 'fixed':
            self.request.Set_Color(area,color1)
        elif mode == 'blink':
            self.request.Set_Blink_Color(area,color1)
        elif mode == 'morph' and color2:
            self.request.Set_Morph_Color(area,color1,color2)
        
    def Add_Speed_Conf(self, speed = 0xc800):
        self.request.Set_Speed(speed)
        
    def End_Loop_Conf(self):
        self.request.End_Loop()
        
    def End_Transfert_Conf(self):
        self.request.End_Transfert()
        
    def Write_Conf(self):
        self.WaitForOk()
        self.driver.WriteDevice(self.request)
    
    def Set_Color(self, Area, Color, Save = False, Apply = False, block = 0x01):
        """Set the Color of an Area """
    
        request = Constructor(self.driver,Save,block)
        if type(Area) != list:
            Area = request.Area(Area)
        if type(Color) != list:
            Color = request.Color(Color)
            
        self.WaitForOk()
        request.Set_Color(Area, Color)
        request.End_Loop()
        request.End_Transfert()
        self.driver.WriteDevice(request)
        
    
        if Apply:
            self.WaitForOk()
            request = Constructor(self.driver,False,block)
            request.Set_Color(Area,Color)
            request.End_Loop()
            request.End_Transfert()
            self.driver.WriteDevice(request)
    
    def Set_Color_Blink(self,Area,Color, Save = False, Apply = False, block = 0x01):
        self.WaitForOk()
        request = Constructor(self.driver,Save,block)
        if type(Area) != list:
            Area = request.Area(Area)
        if type(Color) != list:
            Color = request.Color(Color)
        request.Set_Speed()
        request.Set_Blink_Color(Area,Color)
        request.End_Loop()
        request.End_Transfert()
        self.driver.WriteDevice(request)
            
        if Apply:
            self.WaitForOk()
            request = Constructor(self.driver)
            request.Set_Speed()
            request.Set_Blink_Color(Area,Color)
            request.End_Loop()
            request.End_Transfert()
            self.driver.WriteDevice(request)

        
    def Set_Color_Morph(self,Area,Color1,Color2, Save = False, Apply = False, block = 0x01):
        self.WaitForOk()
        request = Constructor(self.driver,Save,block)
        if type(Area) != list:
            Area = request.Area(Area)
        if type(Color1) != list:
            Color1 = request.Color(Color1)
        if type(Color2) != list:
            Color2 = request.Color(Color2)
        request.Set_Speed()
        request.Set_Morph_Color(Area,Color1,Color2)
        request.End_Loop()
        request.End_Transfert()
        self.driver.WriteDevice(request)
                        
        if Apply:
            self.WaitForOk()
            request = Constructor(self.driver,Save,block)
            request.Set_Speed()
            request.Set_Morph_Color(Area,Color1,Color2)
            request.End_Loop()
            request.End_Transfert()
            self.driver.WriteDevice(request)

    def WaitForOk(self):
        self.driver.Take_over()
        self.Get_State()
        request = Constructor(self.driver)
        request.Reset_all()
        self.driver.WriteDevice(request)
        while not self.Get_State():
            request.raz()
            request.Get_Status()
            request.Reset_all()
            self.driver.WriteDevice(request)
        return True
        
    def Get_State(self):
        self.driver.Take_over()
        request = Constructor(self.driver)
        request.Get_Status()
        self.driver.WriteDevice(request)
        msg = self.driver.ReadDevice(request)
        return msg[0] == self.driver.computer.STATE_READY
    
    def Reset(self,res_cmd):
        self.driver.Take_over()
        request = Constructor(self.driver)
        while True:
            request.Get_Status()
            self.driver.WriteDevice(request)
            msg = self.driver.ReadDevice(request)
            if msg[0] == 0x10:
                break
            request.raz()
            request.Get_Status()
            request.Reset(res_cmd)
            self.driver.WriteDevice(request)
            msg =  self.driver.ReadDevice(request)
            if msg[0] == 0x10:
                break
        return True
    
class Constructor(list):
    def __init__(self, driver, save=False, block=0x01):
        self.raz()
        self.computer = driver.computer
        self.void = [self.computer.FILL_BYTE]*self.computer.DATA_LENGTH
        self.Id = 0x01
        self.save = save
        self.block = block
    
    def Save(self,end = False):
        if self.save:
            if not end:
                self.Set_Save_Block(self.block)
            else:
                self.Set_Save()
    
    def Show_Request(self):
        for i in self:
            packet = ''
            for j in i.packet:
                packet += hex(int(j)) + ' '

    def Set_Speed(self,Speed = 0xc800):
        self.Save()
        cmd = copy(self.void)
        legend = "Set Speed: {}".format(Speed)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_SPEED
        cmd[3] = int(Speed/256)
        cmd[4] = int(Speed - (Speed/256)*256)
        self.append(Request(legend,cmd))
    
    def Set_Blink_Color(self,Area,Color):
        self.Save()
        cmd = copy(self.void)
        legend = "Set Blink Color"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_BLINK_COLOR
        cmd[2] = self.Id
        cmd[3] = Area[0]
        cmd[4] = Area[1]
        cmd[5] = Area[2]
        cmd[6] = Color[0]
        cmd[7] = Color[1]

        self.append(Request(legend,cmd))
    
    def Set_Morph_Color(self,Area,Color1,Color2):
        self.Save()
        cmd = copy(self.void)
        legend="Set Morph Color"
            
        Color12 = Color1[1] + Color2[0]
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_MORPH_COLOR
        cmd[2] = self.Id
        cmd[3] = Area[0]
        cmd[4] = Area[1]
        cmd[5] = Area[2]
        cmd[6] = Color1[0]
        cmd[7] = Color12
        cmd[8] = Color2[1]
        
        self.append(Request(legend,cmd))
        
    def Area(self, areas): # gotta check the power button to understand it ...
        """
            This method will parse an area to a list of tree values.
            
            area = 0x000000
        
            0x80    -> [0x0, 0x0, 0x80]
            0x100   -> [0x0, 0x1, 0x0]
            0x2     -> [0x0, 0x0, 0x2]
            0x1     -> [0x0, 0x0, 0x1]
            0x20    -> [0x0, 0x0, 0x20]
            0x1c00  -> [0x0, 0x1c, 0x0]
            0x4     -> [0x0, 0x0, 0x4]
            0x8     -> [0x0, 0x0, 0x8]
            0x40    -> [0x0, 0x0, 0x40]
            0x200   -> [0x0, 0x2, 0x0]
        """
    
        ret = [0x00,0x00,0x00]
        
        if type(areas) == dict:
            for key in areas:
                print(key)
                area += self.computer.regions[key].regionId
                
        elif type(areas) == int:
            area = areas
            
        elif type(areas) == str:
            area = int(areas,16)
        
        ret[0] = area//65536                           # Takes the two first digit
        ret[1] = area//256 - ret[0] * 256              # Takes the four first digit and remove the two first digit
        ret[2] = area - ret[0] * 65536 - ret[1] * 256  # Same but remove the first 4 digit

        return ret
    
    def Set_Color(self,Area,Color, Id = 0x01):

        self.Save()        
        cmd = copy(self.void)                                                                                    
        legend="Set Color"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_COLOR
        cmd[2] = self.Id
        cmd[3] = Area[0]
        cmd[4] = Area[1]
        cmd[5] = Area[2]
        cmd[6] = Color[0]
        cmd[7] = Color[1]
        
        self.append(Request(legend,cmd))
    
    def Set_Save_Block(self,block):
        cmd = copy(self.void)
        legend = "Save block: {}".format(block)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SAVE_NEXT
        cmd[2] = block
        
        self.append(Request(legend,cmd))
    
    def Set_Save(self):
        cmd = copy(self.void)
        legend = "Set Save"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SAVE
        
        self.append(Request(legend,cmd))
    
    def Color(self,color):
        color=color.replace('#','')
        r = int(color[0:2],16)//16
        g = int(color[2:4],16)//16
        b = int(color[4:6],16)//16
        c = [0x00,0x00]
        c[0] = r * 16 + g  # if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc 
        c[1] = b * 16
        return c

    def Color2(self,color):
        color=color.replace('#','')
        r = int(color[0:2],16)//16
        g = int(color[2:4],16)//16
        b = int(color[4:6],16)//16
        c = [0x00,0x00]
        c[0] = r  # if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
        c[1] = g * 16 + b
        return c
        
    def Get_Status(self):
        cmd = copy(self.void)
        legend = "Get Status"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_GET_STATUS

        self.append(Request(legend,cmd))
        
    def Reset_all(self):
        self.Save()
        cmd = copy(self.void)
        legend = "Reset All Lights On"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_RESET
        cmd[2] = self.computer.RESET_ALL_LIGHTS_ON

        self.append(Request(legend,cmd))
        
    def Reset(self,command):
        if command in [ self.computer.RESET_ALL_LIGHTS_ON,
                        self.computer.RESET_ALL_LIGHTS_OFF,
                        self.computer.RESET_TOUCH_CONTROLS,
                        self.computer.RESET_SLEEP_LIGHTS_ON
                        ]:
            self.Save()
            cmd = copy(self.void)
            legend = "Reset All Lights On"
            cmd[0] = self.computer.START_BYTE
            cmd[1] = self.computer.COMMAND_RESET
            cmd[2] = command

            self.append(Request(legend,cmd))
        else:
            print("Engine > Constructor error: WRONG RESET COMMAND")
    
    def End_Loop(self):
        self.Save()
        cmd = copy(self.void)
        legend = "End Loop"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_LOOP_BLOCK_END
        
        self.Id += 0x01
        self.append(Request(legend,cmd))
        
    def End_Transfert(self):
        self.Save(end = True)
        if not self.save:
            cmd = copy(self.void)
            legend = "End Transfert"
            cmd[0] = self.computer.START_BYTE
            cmd[1] = self.computer.COMMAND_TRANSMIT_EXECUTE
            
            self.append(Request(legend,cmd))
    
    def raz(self):
        while len(self) > 0:
            self.pop()
            

class Request:
    def __init__(self,legend,packet):
        self.legend = legend
        self.packet = packet
