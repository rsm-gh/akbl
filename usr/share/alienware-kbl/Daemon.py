#!/usr/bin/python3
#

#  Copyright (C) 2015-2017  Rafael Senties Martinelli <rafael@senties-martinelli.com>
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



import Pyro4
import os
import pwd
from traceback import format_exc
from time import time, sleep
from common import getuser
from CCParser import CCParser

# local imports
import Configuration
from Engine import *
from Paths import Paths
from Texts import *

class ConnectDaemon:
    def __init__(self):
        self.daemon=Pyro4.Daemon()
        self.paths=Paths()
        
        uri=self.daemon.register(Daemon(self))
        with open(self.paths.DAEMON_PYRO_PATH, encoding='utf-8', mode='wt') as f:
            f.write(str(uri))

        self.daemon.requestLoop()
    

class Daemon:
    
    def __init__(self, loop_self):
        
        self._driver = Driver()     
        if self._driver.not_found:
            print("Warning: The computer is not supported")
            exit(1)

        self.loop_self=loop_self


        # Get the user that the daemon should use
        #
        self._paths=Paths()
        _global_ccp=CCParser(self._paths.GLOBAL_CONFIG,'Global alienware-kbl Configuration')
        self._user=_global_ccp.get_str_defval('boot_user','root')
        
        
        # Check if the user of the configuration file exists
        #
        try:
            pwd.getpwnam(self._user)
        except:
            user=getuser()
            print('Warning: The `{}` of the configuration file does not exists, it has been replaced by `{}`.'.format(self._user, user))
            self._user=user
            
        self._paths=Paths(self._user)
        
        # Initialize the daemon
        #
        self._ccp=CCParser(self._paths.CONFIGURATION_PATH,'GUI Configuration')
        
        self._controller = Controller(self._driver)     
        
        self._indicator_pyro=False
        self._computer = self._driver.computer

        self.reload_configurations(self._user)
        self.set_lights(self._user, self._ccp.get_bool_defval('boot', True))

        
    def _iluminate_keyboard(self):

        self._lights_state = True
        
        self._controller.Set_Loop_Conf(False, self._computer.BLOCK_LOAD_ON_BOOT)
        self._controller.Add_Speed_Conf(self._theme.speed)

        try: # Patch (#12)
            os.utime(self.theme.path, None)
        except Exception as e:
            print('Warning: It was not possible to os.utime the profile path: \n{}'.format(self._theme.path))
            print(format_exc())

        try:
            self._indicator_send_code(100)
            self._indicator_pyro.load_profiles(list(Configuration.profiles.keys()), self.profile_name, self._lights_state)
        except Exception as e:
            print(format_exc())

        
        for key in sorted(self._theme.area.keys()):            
            area=self._theme.area[key]
            for zone in area:
                self._controller.Add_Loop_Conf( zone.regionId,
                                                zone.mode,
                                                zone.color1,
                                                zone.color2)
                                            
            self._controller.End_Loop_Conf()

        self._controller.End_Transfert_Conf()
        self._controller.Write_Conf()

            

    def _indicator_send_code(self, val):
        if self._indicator_pyro:
            try:
                self._indicator_pyro.set_code(val)
            except Exception as e:
                format_exc()


    """
        General Bindings
    """

    @Pyro4.expose
    def ping(self):
        pass
    
    @Pyro4.expose
    def reload_configurations(self, user, indicator=True, set_default=True):
        
        if user != self._user:
            self._user=user
            self._paths=Paths(user)
        
        
        Configuration.LOAD_profiles(self._computer, self._paths.PROFILES_PATH)
        
        if set_default:
            _, self.profile_name = Configuration.GET_last_configuration()
            self._theme=Configuration.profiles[self.profile_name]
        
        if self._indicator_pyro and indicator:
            try:
                self._indicator_pyro.load_profiles(list(Configuration.profiles.keys()), self.profile_name, self._lights_state)
            except Exception as e:
                print(format_exc())


    """
        Bindings for the users
    """
    
    @Pyro4.expose
    def set_profile(self, user, profile):
        """
            Set a profile from the existing profiles.
            
            + 'profile' is the profile name
        """
        if user != self._user:
            self._user=user
            self._paths=Paths(user)
        
        
        self.reload_configurations(user, False, False)
 
        if profile in Configuration.profiles.keys():
            self._theme=Configuration.profiles[profile]
            self.profile_name=profile
            self._iluminate_keyboard()
            self._iluminate_keyboard()


    @Pyro4.expose
    def switch_lights(self, user):
        """
            If the lights are on, put them off
            or if the lights are off put them on
        """
        if self._lights_state:
            self.set_lights(user, False)
        else:
            self.set_lights(user, True)


    @Pyro4.expose
    def set_lights(self, user, state):
        """
            Turn the lights on or off.
            
            + 'state' can be a boolean or a string
        """
        if state in (False, 'False','false'):

            keep_alive_zones=self._ccp.get_str_defval('zones_to_keep_alive','')
            
            if keep_alive_zones == '':
                self._controller.Set_Loop_Conf(False, self._driver.computer.BLOCK_LOAD_ON_BOOT)
                self._controller.Reset(self._computer.RESET_ALL_LIGHTS_OFF)
            else:
                keep_alive_zones=keep_alive_zones.split('|')
                
                """
                    This hack, it will set black as color to all the lights that should be turned off
                """
                self._controller.Set_Loop_Conf(False, self._driver.computer.BLOCK_LOAD_ON_BOOT)
                self._controller.Add_Speed_Conf(1)

                for key in sorted(self._theme.area.keys()):
                    if not key in keep_alive_zones:
                        area=self._theme.area[key]
                        for zone in area:
                            self._controller.Add_Loop_Conf(zone.regionId, 'fixed', '#000000', '#000000')

                        self._controller.End_Loop_Conf()

                self._controller.End_Transfert_Conf()
                self._controller.Write_Conf()

            self._lights_state=False
            self._indicator_send_code(150)
        else:
            if user != self._user:
                self.reload_configurations(user)

            self._iluminate_keyboard()
    
    
    @Pyro4.expose
    def set_colors(self, mode, speed, colors1, colors2=None):
        """
            Change the colors and the mode of the keyboard.
            
            + The available modes are: 'fixed', 'morph', 'blink'
                'fixed' and 'blink' only takes colors1
                
            + Speed must be an integer. 1 =< speed =< 256
            
            + colors1 and colors2 can be a single hex color or a list.
              If both arguments are used, both arguments must have
              the same number of items.
        """
        
        if not mode in ('fixed','morph','blink'):
            print("Warning: Wrong mode",mode)
            return
        elif not isinstance(speed, int):
            print("Warning: Speed must be an integer")
            return
        elif speed >= 256:
            speed=255
        elif speed < 1:
            speed=1
        
        speed=speed*256

        if not isinstance(colors1, list):
            colors1=[colors1]
        
        if colors2==None:
            colors2=colors1
            
        if not isinstance(colors2, list):
            colors2=[colors2]

        if len(colors1) != len(colors2):
            print("Warning: The colors list do not have the same lenght")
            return

        self._lights_state = True
        self._controller.Set_Loop_Conf(False, self._computer.BLOCK_LOAD_ON_BOOT)
        self._controller.Add_Speed_Conf(speed)

        for zone in self._computer.regions.keys():
            for i in range(len(colors1)):
                
                self._controller.Add_Loop_Conf( self._computer.regions[zone].regionId,
                                                mode,
                                                colors1[i],
                                                colors2[i])
                                        
            self._controller.End_Loop_Conf()

        self._controller.End_Transfert_Conf()
        self._controller.Write_Conf() 
    

    """
        Bindings for the graphical interphase
    """
    
    @Pyro4.expose
    def get_computer_name(self):
        return self._driver.computer.name
    
    @Pyro4.expose
    def get_computer_info(self):
        return (self._computer.name, self._driver.vendorId, self._driver.productId, str(self._driver.dev))
    
    @Pyro4.expose    
    def modify_lights_state(self, bool):
        """ 
            This method does not changes the lights of the keyboard,
            it only updates the daemon and the indicator 
        """
        if bool in (False,'False','false'):
            self._lights_state=False
            self._indicator_send_code(150)
        else:
            self._lights_stae=True
            self._indicator_send_code(100)

    """
        Indicator Bindings
    """
    
    @Pyro4.expose
    def indicator_get_state(self):
        if self._lights_state:
            self._indicator_send_code(100)
        else:
            self._indicator_send_code(150)      
    
    
    @Pyro4.expose    
    def indicator_init(self, uri):
        try:
            self._indicator_pyro = Pyro4.Proxy(str(uri))
            self.reload_configurations(self._user)
        except Exception as e:
            print("Warning: Indicator failed its initialization")
            print(format_exc())
            self._indicator_pyro=False
        
        
    @Pyro4.expose
    def indicator_kill(self):
        self._indicator_pyro=False


if __name__ == '__main__':
    if getuser() != 'root':
        print(TEXT_ONLY_ROOT)
    else:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        ConnectDaemon()
