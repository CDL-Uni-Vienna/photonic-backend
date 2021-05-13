# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 17:56:04 2020

@author: juanl
"""
from .functions_Powermeter import *
from .functions_ThorlabsMotors import*

sign = lambda x: math.copysign(1, x)


def plot_powerControl(powers, p_target, tolerance, tolerance_large):
    figure()
    plot(arange(1,len(powers)+1), powers, '.-', label='powers ')
    legend()
    title('Target: '+str(p_target)+' (uW)    Final: '+str(powers[len(powers)-1])+' (uW)')
    xlabel('iteration')
    ylabel('Power (uW)')
    axhline(p_target + tolerance_large, color='blue', ls='dotted')
    axhline(p_target + tolerance, color='red', ls='dotted')
    axhline(p_target, color='red')
    axhline(p_target - tolerance, color='red', ls='dotted')
    axhline(p_target - tolerance_large, color='blue', ls='dotted')
    tight_layout()
    show()

def get_pmin(motors, m1, wp_offset, pm):
    move_topos(motors, m1, wp_offset)
    pmin = read_power(pm)
    print('P_min (uW): ', pmin)
    print('')
    return pmin
    
def get_pmax(motors, m1, wp_offset, pm):
    move_topos(motors, m1, wp_offset + 45)
    pmax = read_power(pm)
    print('P_max (uW): ', pmax)
    print('')
    return pmax


def set_power(motors, m1, wp_offset, pm, p_target, tolerance, tolerance_large, theta_in, theta_step):

    pmin = get_pmin(motors, m1, wp_offset, pm)
    pmax = get_pmax(motors, m1, wp_offset, pm)
    
    
    angle = 90/(pi)*arcsin(sqrt(p_target/pmax))
    angle = round(angle,3)
    angle = angle + theta_in
    
    move_topos(motors, m1, wp_offset + angle)
    p = read_power(pm)
    print('power in (uW): ', p)
    print('')
    
    powers = []
    powers.append(p)
    
    power_dif = p - p_target
    theta_new = wp_offset + angle + theta_step
    
    while(1):
        
        if (abs(power_dif) > tolerance):
        
            if (p < p_target):    
                diff_old = power_dif
                
                move_topos(motors, m1, theta_new)
                p = read_power(pm)
                print('power in (uW): ', p)
                print('')
                
                powers.append(p)
                
                # theta_new = theta_new + theta_step
                power_dif = p - p_target
                
                if (sign(diff_old*power_dif) == 1):
                    theta_new = theta_new + theta_step
                else:
                    theta_step = theta_step/2
                    theta_new = theta_new - theta_step
                
            if (p > p_target): 
                diff_old = power_dif
                
                powers.append(p)
                
                # theta_new = theta_new - theta_step
                move_topos(motors, m1, theta_new)
                p = read_power(pm)
                print('power in (uW): ', p)
                print('')
                
                power_dif = p - p_target
                
                if (sign(diff_old*power_dif) == 1):
                    theta_new = theta_new - theta_step
                else:
                    theta_step = theta_step/2
                    theta_new = theta_new + theta_step            
        else:
            powers.append(p)
            time.sleep(.01)
            break   
    
    plot_powerControl(powers, p_target, tolerance, tolerance_large)
    return powers

def maintain_power(motors, m1, wp_offset, pm, p_target, tolerance, theta_in, theta_step):
      
    # angle = read_pos(motors, m1)
    # angle = round(angle,3)
    # angle = angle + theta_in
    
    # move_topos(motors, m1, wp_offset + angle)
    p = read_power(pm)
    print('power in (uW): ', p)
    print('')
    
    power_dif = p - p_target
    theta_new = read_pos(motors, m1) + theta_in
    
    while(1):
        
        if (abs(power_dif) > tolerance):
        
            if (p < p_target):    
                diff_old = power_dif
                
                move_topos(motors, m1, theta_new)
                p = read_power(pm)
                print('power in (uW): ', p)
                print('')
                
                power_dif = p - p_target
                
                if (sign(diff_old*power_dif) == 1):
                    theta_new = theta_new + theta_step
                else:
                    theta_step = theta_step/2
                    theta_new = theta_new - theta_step
                
            if (p > p_target): 
                diff_old = power_dif
                
                move_topos(motors, m1, theta_new)
                p = read_power(pm)
                print('power in (uW): ', p)
                print('')
                
                power_dif = p - p_target
                
                if (sign(diff_old*power_dif) == 1):
                    theta_new = theta_new - theta_step
                else:
                    theta_step = theta_step/2
                    theta_new = theta_new + theta_step            
        else:
            time.sleep(.01)
            break