# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 15 Jun 2017
# last edit date: 15 Jun 2017
#######################################################

##########import package files##########
import os as os
import numpy as np
import matplotlib.pyplot as plt
import math
import CropElectricityYeildSimulatorConstant as constant
import Util as util
import datetime



def calcUnitDailyFreshWeightE_J_VanHenten1994(U_T, U_par, U_CO2, cropElectricityYieldSimulator1 = None):
    '''

    :param U_T: canopy temperature [`C]
    :return:
    '''

    structuralDryWeight = 0.0
    nonStructuralDryWeight = 0.0
    dt = {'day': 1}

    # [g / m**2]
    d_nonStructuralDryWeight = np.zeros(util.getSimulationDaysInt())
    # [g / m**2]
    d_structuralDryWeight = np.zeros(util.getSimulationDaysInt())
    # structured dry weight on each day [g / m**2]
    Xsdw = np.zeros(util.getSimulationDaysInt())
    # non structured dry weight on each day [g / m**2]
    Xnsdw = np.zeros(util.getSimulationDaysInt())

    i = 0
    while i  < util.getSimulationDaysInt():

        # [g / m**2]
        InitialdryWeight = 5.0
        # [g / m**2]
        Xsdw[0] = InitialdryWeight * 0.75
        # [g / m**2]
        Xnsdw[0] = InitialdryWeight * 0.25
        # # [g / m**2 / day]
        # d_nonStructuralDryWeight[0] = 0.0
        # # [g / m**2 / day]
        # d_structuralDryWeight[0] = 0.0

        for i in range (1, constant.cultivationDaysperHarvest):

            # the transfromation rate of non-structural dry weight to structural dry weight
            r_gr = constant.c_gr_max['s-1'] * Xnsdw[i] / (constant.c_gamma * Xsdw[i] + Xnsdw[i]) * (constant.c_Q10_gr ** ((U_T[i] - 20.0) / 10.0))
            # the maintenance respiration rate of the crop
            f_resp = (constant.c_resp_sht['s-1'] * (1 - constant.c_tau) * Xsdw[i] + constant.c_resp_rt['s-1'] * constant.c_tau * Xsdw[i]) * constant.c_Q10_resp


            # CO2 compensation point
            upperCaseGamma = constant.c_upperCaseGamma['ppm'] * constant.c_Q10_upperCaseGamma ** ((U_T[i] -20.0)/10.0)

            # the carboxylation conductance
            g_car = constant.c_car1 * (U_T[i])**2 + constant.c_car2 * U_T[i] + constant.c_car3
            # gross carbon dioxide assimilation rate of the canopy having an effective surface of 1m^2 per square meter soild at complete soil covering.
            g_CO2 = constant.g_bnd['m s-1']*constant.g_stm['m s-1']* g_car / (constant.g_bnd['m s-1']*g_stm.g_stm['m s-1'] + constant.g_bnd['m s-1']*g_car + g_stm.g_stm['m s-1']*g_car)
            # light use efficiency
            epsilon = {'g J-1': constant.c_epsilon['g J-1'] * (U_CO2[i] - upperCaseGamma) / ( U_CO2[i]  + 2.0 * upperCaseGamma)}

            f_photo_max = ['g m-2 s-2': epsilon['g J-1'] * U_par[i] * g_CO2 * c_omega * (U_CO2[i] - upperCaseGamma) ]
            # the gross canopy photosynthesis
            f_photo = (1 - np.exp( - constant.c_K * constant.c_lar['m2 g-2'] * (1- constant.c_tau) * Xsdw[i])) * f_photo_max['g m-2 s-2']

            d_nonStructuralDryWeight = constant.c_alpha * f_photo - r_gr * Xsdw - f_resp - (1 - constant.c_beta) / constant.c_beta * r_gr * Xsdw
            d_structuralDryWeight = r_gr * Xsdw

        # the plant weight per head
        Ydw = (Xsdw + Xnsdw) / float(constant.numOfHeadsPerArea)
