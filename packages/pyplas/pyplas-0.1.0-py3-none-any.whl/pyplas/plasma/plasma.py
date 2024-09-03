#!/usr/bin/python3
from scipy import constants as const
import numpy as np


class plasma():
    def __init__(self, electrons=None, ions=None, neutrals=None, 
                 potential=None, B=0):
        
        self.electrons = self.e = electrons
        self.ions = self.i = ions
        self.neutral = self.n = neutrals
        self.B = B
        
        if ions:
            self.Ti = self.i.T
            self.ni = self.i.n
            self.mi = self.i.m
        
        if electrons:
            self.Te = self.e.T
            self.ne = self.e.n
            self.me = self.e.m

        if neutrals:
            self.Tg = self.n.T
            self.ng = self.n.n
            self.mg = self.n.m 
            self.P = self.n.P
        else:
            self.Tg = None
            self.ng = None
            self.mg = None
            self.P = None
        
        self.potential = self.Phi = potential
        self.ion_neutral_cx = None
        self.ion_neutral_MFP = None
        self.ion_neutral_freq = None
        
        
    def get_ion_neutral_MFP(self):
        return 1/(self.ng*self.ion_neutral_cx) # TODO check!
    
    def get_ion_neutral_freq(self):
        freq = self.ng * self.ion_neutral_cx \
                            * np.sqrt(8*const.k*self.Ti/(np.pi*self.mi))
        return freq
    
    def get_Bohm_speed(self):
        if self.Te and self.mi:
            return np.sqrt(const.k*self.Te/self.mi)
        else:
            print("Need electron temperature and ion mass for Bohm speed.")
            return None

    def get_Debye(self):
        return np.sqrt(const.epsilon_0*const.k*self.Te/(self.ne * const.e**2))
    
    def get_electron_gyro_radius(self):
        if self.B and self.e:
            return np.abs(self.me*self.e.get_vth()/(self.e.q * self.B))
        else:
            print("Need electron properties and magnetic field to calculate gyro radius.")
            return None

    def get_ion_gyro_radius(self):
        if self.B and self.i:
            return np.abs(self.mi*self.i.get_vth()/(self.i.q * self.B))
        else:
            print("Need ion properties and magnetic field to calculate gyro radius.")
            return None

    def get_electron_gyro_freq(self):
        if self.B and self.e:
            return np.abs(self.e.q * self.B/self.me)
        else:
            print("Need electron properties and magnetic field to calculate gyro frequency.")
            return None

    def get_ion_gyro_freq(self):
        if self.B and self.i:
            return np.abs(self.i.q * self.B/self.mi)
        else:
            print("Need ion properties and magnetic field to calculate gyro frequency.")
            return None


