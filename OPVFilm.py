# -*- coding: utf-8 -*-

##########import package files##########
from scipy import stats
import sys
import datetime
import calendar
import os as os
import numpy as np
import matplotlib.pyplot as plt
import math
import CropElectricityYeildSimulatorConstant as constant
import Util as util
import ShadingCurtain
#######################################################

# command to show all array data
# np.set_printoptions(threshold=np.inf)
# print ("hourlyHorizontalDirectOuterSolarIrradiance:{}".format(hourlyHorizontalDirectOuterSolarIrradiance))
# np.set_printoptions(threshold=1000)

# np.set_printoptions(threshold=np.inf)
# print ("hourlySolarIncidenceAngle: {}".format(hourlySolarIncidenceAngle))
# np.set_printoptions(threshold=1000)


def getOPVArea(OPVCoverageRatio):
    '''
    return the OPV area given a certain OPV coverage ratio
    :param OPVCoverageRatio:
    :return:  [m^2]
    '''
    return OPVCoverageRatio * constant.greenhouseTotalRoofArea

def calcDeclinationAngle (year, month, day):
    '''
    calculate the declination angle [°]
    :param month: list of months.
    :param day: list of days

    :return: declinationAngle [rad]
    '''
    # number of days from January first
    n = np.zeros(year.shape[0])
    declinationAngleperHour = np.zeros(year.shape[0])

    # print "year:{}".format(year)
    # print "year.shape[0]:{}".format(year.shape[0])
    # print "month.shape:{}".format(month.shape)
    # print "day:{}".format(day)
    for i in range (0, year.shape[0]):
        n[i] = (datetime.date(year[i], month[i], day[i]) - datetime.date(year[i], 1, 1)).days + 1
        # print "n[{}]:{}".format(i,n[i])
        declinationAngleperHour[i] = math.radians(23.45 * math.sin(math.radians(360.0 * (284 + n[i]) / 365)))
        # print "i:{}, n[i]:{}".format(i, n[i])

    return declinationAngleperHour

def getSolarHourAngleKacira2003(hour):
    '''
    calculate the solar hour angle [°]
    :param hour:
    :return:solarHourAngle [degree]
    '''
    return np.radians(constant.minuteperHour*(hour - constant.noonHour ) / 4.0)
    # Be careful! The paper indicates the following equation to get hour angle, but when integrating it with Yano et al. (2009), you need to let it negative in the morning and positive in the afternoon.
    # return np.radians(constant.minuteperHour*(constant.noonHour - hour ) / 4.0)


def getSolarHourAngleYano2009(hour):
    '''
    calculate the solar hour angle [°]
    :param hour:
    :return:solarHourAngle [degree]
    '''
    # TODO: adopt the authorized way to calculate the local apparent time LAT. now it is approximated to be 0.4 based on Tucson, Arizona, US referring to Dr Kacira's calculation .
    localApparentTime = hour - 0.4
    return (math.pi/12.0) * (localApparentTime  - constant.noonHour)

    # longitude at Tucson 32.2800408,-110.9422745
    # lambda (longitude of the site) = 32.2800408 N: latitude,-110.9422745 W : longitude  [degree]
    # lambda_R ( the longitude of the time zone in which the site is situated) = 33.4484, 112.074 [degree]
    # J' (the day angle in the year ) =
    # EOT (equation of time) =



def calcSolarAltitudeAngle(hourlyDeclinationAngle, hourlySolarHourAngle):
    '''
    calculate the solar altitude angle [rad]
    constant.Latitude: symbol phi [rad]
    :param hourlyDeclinationAngle:symbol delta [rad]
    :param hourlySolarHourAngle:symbol omega [rad]
    :return: hourlySolarAltitudeAngle [rad]
    '''
    sinDelta = np.sin(hourlyDeclinationAngle)
    cosDelta = np.cos(hourlyDeclinationAngle)
    sinOmega = np.sin(hourlySolarHourAngle)
    cosOmega = np.cos(hourlySolarHourAngle)
    sinPhi = np.sin(constant.Latitude)
    cosPhi = np.cos(constant.Latitude)

    return np.arcsin(cosPhi*cosDelta*cosOmega + sinPhi*sinDelta)

def calcSolarAzimuthAngle(hourlyDeclinationAngle, hourlySolarAltitudeAngle, hourlySolarHourAngle):
    '''
    calculate the azimuth angle [rad]
    constant.Latitude: symbol phi [rad]
    :param hourlyDeclinationAngle:symbol delta [rad]
    :param hourlySolarAltitudeAngle:symbol alpha [rad]
    :param hourlySolarHourAngle:symbol omega [rad]
    :return: hourlyAzimuthAngle [rad]
    '''
    sinDelta = np.sin(hourlyDeclinationAngle)
    cosDelta = np.cos(hourlyDeclinationAngle)
    sinAlpha = np.sin(hourlySolarAltitudeAngle)
    cosAlpha = np.cos(hourlySolarAltitudeAngle)
    sinPhi = np.sin(constant.Latitude)
    cosPhi = np.cos(constant.Latitude)
    # print ("sinDelta:{}".format(sinDelta))
    # print ("sinAlpha:{}".format(sinAlpha))
    # print ("cosAlpha:{}".format(cosAlpha))
    # print ("sinPhi:{}".format(sinPhi))
    # print ("cosPhi:{}".format(cosPhi))


    # [rad]
    # hourlyAzimuthAngle is multiplied by -1 when hourlySolarHourAngle (omega) < 0

    # when using the function of "", "np.arccos((sinAlpha*sinPhi - sinDelta) / (cosAlpha * cosPhi))" value became nan when "(sinAlpha*sinPhi - sinDelta) / (cosAlpha * cosPhi)" is "-1."
    # Thus this if statement corrects this error.
    a = (sinAlpha*sinPhi - sinDelta) / (cosAlpha * cosPhi)
    for i in range (0, a.shape[0]):
        if a[i] < -1.0:
            a[i] = -1.0
        elif a[i] > 1.0:
            a[i] = 1.0
    # print("a:{}".format(a))
    hourlyAzimuthAngle = np.sign(hourlySolarHourAngle) * np.arccos(a)
    # print("hourlyAzimuthAngle:{}".format(hourlyAzimuthAngle))

    return hourlyAzimuthAngle


def calcSolarIncidenceAngleKacira2003(hourlyDeclinationAngle, hourlySolarHourAngle ,hourlysurfaceAzimuthAngle):
    '''
    calculate solar incidence angle
    constant.OPVAngle: symbol capital s (S) [rad]
    constant.Latitude: symbol phi [rad]
    :param hourlyDeclinationAngle: symbol delta [rad]
    :param hourlySolarHourAngle: symbol omega [rad]
    :param hourlysurfaceAzimuthAngle: symbol gamma [rad]
    :return: SolarIncidenceAngle [rad]
    '''
    sinDelta = np.sin(hourlyDeclinationAngle)
    cosDelta = np.cos(hourlyDeclinationAngle)
    sinPhi = np.sin(constant.Latitude)
    cosPhi = np.cos(constant.Latitude)
    sinOmega = np.sin(hourlySolarHourAngle)
    cosOmega = np.cos(hourlySolarHourAngle)
    sinGamma = np.sin(hourlysurfaceAzimuthAngle)
    cosGamma = np.cos(hourlysurfaceAzimuthAngle)
    sinS = np.sin(constant.OPVAngle)
    cosS  = np.cos(constant.OPVAngle)

    # TODO check which is correct
    # From Kacira et al. (2003)
    # solarIncidenceAngle = sinDelta*sinPhi*cosS - sinDelta*cosPhi*sinS*cosGamma + cosDelta*cosPhi*cosS*cosOmega \
    #                  + cosDelta*sinPhi*sinS*cosGamma*cosOmega + cosDelta*sinS*sinGamma*sinOmega
    # from ITACA: http://www.itacanet.org/the-sun-as-a-source-of-energy/part-3-calculating-solar-angles/
    solarIncidenceAngle = sinDelta*sinPhi*cosS + sinDelta*cosPhi*sinS*cosGamma + cosDelta*cosPhi*cosS*cosOmega \
                     - cosDelta*sinPhi*sinS*cosGamma*cosOmega - cosDelta*sinS*sinGamma*sinOmega

    # for i in range (0, sinDelta.shape[0]):
    #     if   -1 > solarIncidenceAngle[i] or 1 < solarIncidenceAngle[i]:
    #         solarIncidenceAngle[i] = (solarIncidenceAngle[i] + solarIncidenceAngle[i])/2.0

    return np.arccos(solarIncidenceAngle)


def calcSolarIncidenceAngleYano2009(hourlySolarAltitudeAngle, hourlySolarAzimuthAngle, hourlyModuleAzimuthAngle, OPVAngle = constant.OPVAngle):
    '''
    calculate solar incidence angle. the equation wat taken from
    constant.OPVAngle: symbol capital s (S) [rad]
    constant.Latitude: symbol phi [rad]
    :param hourlyDeclinationAngle: symbol delta [rad]
    :param hourlySolarHourAngle: symbol omega [rad]
    :param hourlySurfaceAzimuthAngle: symbol gamma [rad]
    :param hourlySolarAltitudeAngle: symbol alpha [rad]
    :param hourlySolarAzimuthAngle: symbol phi_S [rad]
    :param hourlyModuleAzimuthAngle: symbol phi_P [rad]

    :return: SolarIncidenceAngle [rad]
    '''
    # sinPhi = np.sin(constant.Latitude)
    # cosPhi = np.cos(constant.Latitude)
    sinS = np.sin(OPVAngle)
    cosS  = np.cos(OPVAngle)
    sinAlpha = np.sin(hourlySolarAltitudeAngle)
    cosAlpha = np.cos(hourlySolarAltitudeAngle)
    sinPhiS = np.sin(hourlySolarAzimuthAngle)
    cosPhiS = np.cos(hourlySolarAzimuthAngle)
    sinPhiP = np.sin(hourlyModuleAzimuthAngle)
    cosPhiP = np.cos(hourlyModuleAzimuthAngle)

    solarIncidenceAngle = np.arccos(sinAlpha*cosS + cosAlpha*sinS*np.cos(hourlySolarAzimuthAngle - hourlyModuleAzimuthAngle))
    # print("solarIncidenceAngle:{}".format(solarIncidenceAngle))
    return solarIncidenceAngle

def getMaxDirectBeamSolarRadiationKacira2003(hourlySolarAltitudeAngle, hourlyHorizontalDirectOuterSolarIrradiance, hourlyZenithAngle):
    '''
    calculate the max direct beam solar radiation
    :param hourlySolarAltitudeAngle: [rad]
    :param hourlyHorizontalDirectOuterSolarIrradiance: [W m^-2]
    :param hourlyZenithAngle: [rad]
    :return: maxDirectBeamSolarRadiation [W m^-2]
    '''
    # if the altitude angle is minus, it means it is night. Thus, the maxDirectBeamSolarRadiation becomes zero.
    maxDirectBeamSolarRadiation = np.zeros(hourlySolarAltitudeAngle.shape[0])

    # if the altitude angle is minus, it means it is night. Thus, the directBeamSolarRadiationNormalToTiltedOPV becomes zero.
    for i in range (0, hourlySolarAltitudeAngle.shape[0]):
        if hourlySolarAltitudeAngle[i] < 0:
            maxDirectBeamSolarRadiation[i] = 0
        else:
            maxDirectBeamSolarRadiation[i] = hourlyHorizontalDirectOuterSolarIrradiance[i] / np.cos(hourlyZenithAngle[i])

    # print "np.degrees(hourlyZenithAngle):{}".format(np.degrees(hourlyZenithAngle))
    # print "np.cos(hourlyZenithAngle):{}".format(np.cos(hourlyZenithAngle))
    # print"hourlyHorizontalDirectOuterSolarIrradiance:{}".format(hourlyHorizontalDirectOuterSolarIrradiance)
    # print "maxDirectBeamSolarRadiation:{}".format(maxDirectBeamSolarRadiation)

    return maxDirectBeamSolarRadiation


def getDirectHorizontalSolarRadiation(hourlySolarAltitudeAngle, hourlyHorizontalSolarIncidenceAngle):
    '''
    calculate the direct solar radiation to horizontal surface. referred to Yano 2009 equation (6)
    :param hourlySolarAltitudeAngle: [rad]
    :param hourlyHorizontalSolarIncidenceAngle: [rad]
    :return: maxDirectBeamSolarRadiation [W m^-2]
    '''

    directHorizontalSolarRadiation = constant.solarConstant * (constant.atmosphericTransmissivity**(1.0/np.sin(hourlySolarAltitudeAngle))) * \
                                    np.sin(hourlySolarAltitudeAngle)

    # TODO maybe the condition of if statement is not incidence angle but azimuth angle(alpha)
    # if the incidence angle is >|90| the radiation is 0
    for i in range (0, hourlyHorizontalSolarIncidenceAngle.shape[0]):
        # if abs(hourlyHorizontalSolarIncidenceAngle[i]) >= math.pi / 2.0:
        if hourlySolarAltitudeAngle[i] < 0.0:
            directHorizontalSolarRadiation[i] = 0.0

    return directHorizontalSolarRadiation

def getDiffuseHorizontalSolarRadiation(hourlySolarAltitudeAngle, hourlyHorizontalSolarIncidenceAngle):
    '''
    calculate the diffuse solar radiation to horizontal surface. referred to Yano 2009 equation (7)
    :param hourlySolarAltitudeAngle: [rad]
    :return: maxDirectBeamSolarRadiation [W m^-2]
    '''
    diffuseHorizontalSolarRadiation = constant.solarConstant * np.sin(hourlySolarAltitudeAngle) * (1 - constant.atmosphericTransmissivity**(1.0/np.sin(hourlySolarAltitudeAngle))) \
                        / (2.0 * (1 - 1.4*np.log(constant.atmosphericTransmissivity)))

    # if the incidence angle is >|90| the radiation is 0
    for i in range (0, hourlyHorizontalSolarIncidenceAngle.shape[0]):
        # if abs(hourlyHorizontalSolarIncidenceAngle[i]) >= (math.pi) / 2.0:
        if hourlySolarAltitudeAngle[i] < 0.0:
            diffuseHorizontalSolarRadiation[i] = 0.0

    return diffuseHorizontalSolarRadiation


# def getDirectTitledSolarRadiation(simulatorClass, hourlySolarAltitudeAngle, hourlySolarIncidenceAngle, hourlyHorizontalDirectOuterSolarIrradiance = \
#         np.zeros(util.calcSimulationDaysInt() * constant.hourperDay)):
def getDirectTitledSolarRadiation(simulatorClass, hourlySolarAltitudeAngle, hourlySolarIncidenceAngle, hourlyHorizontalDirectOuterSolarIrradiance):
    '''
    calculate the direct solar radiation to tilted surface. referred to Yano 2009 for both cases
    '''

    # if we estimate the solar radiation (calculate the solar radiation without real data), get into this statement
    if simulatorClass.getEstimateSolarRadiationMode() == True:
    # if (hourlyHorizontalDirectOuterSolarIrradiance == 0.0).all():

        # print("at OPVFilm.getDirectTitledSolarRadiation, hourlyHorizontalDirectOuterSolarIrradiance does not have data")
        # if there is no data about solar radiation, assume the solar radiation from the following equation, which is cited from A. Yano, "electrical energy generated by photovoltaic modules mounted inside the roof of a north-south oriented greenhouse", 2009
        directTiltedSolarRadiation = constant.solarConstant * (constant.atmosphericTransmissivity ** (1.0 / np.sin(hourlySolarAltitudeAngle))) * \
                                     np.cos(hourlySolarIncidenceAngle)

        # direct tilted solar radiation is defined as 0 when the incidence angle is >90 or <-90 (|incidence angle| > 90 degree)
        for i in range (0, hourlySolarIncidenceAngle.shape[0]):
            # if abs(hourlySolarIncidenceAngle[i]) >= (math.pi) / 2.0:
            if hourlySolarAltitudeAngle[i] < 0.0 or directTiltedSolarRadiation[i] < 0.0:
                directTiltedSolarRadiation[i] = 0.0

        # np.set_printoptions(threshold=np.inf)
        # print ("directTiltedSolarRadiation: {}".format(directTiltedSolarRadiation))
        # np.set_printoptions(threshold=1000)


        return directTiltedSolarRadiation

    # if we calculate the solar radiation with real data, get into this statement
    else:
        directTiltedSolarRadiation = constant.solarConstant * (constant.atmosphericTransmissivity ** (1.0 / np.sin(hourlySolarAltitudeAngle))) * \
                                     np.cos(hourlySolarIncidenceAngle)

        # direct tilted solar radiation is defined as 0 when the incidence angle is >90 or <-90 (|incidence angle| > 90 degree)
        for i in range (0, hourlySolarIncidenceAngle.shape[0]):
            # if abs(hourlySolarIncidenceAngle[i]) >= (math.pi) / 2.0:
            if hourlySolarAltitudeAngle[i] < 0.0 or directTiltedSolarRadiation[i] < 0.0:
                directTiltedSolarRadiation[i] = 0.0

        # print ("directTiltedSolarRadiation:{}".format(directTiltedSolarRadiation))


        # TODO: delete the following process if not necessary
        ############ outliers data correction start ############
        # when this value is 2, then average just 1 hour before and after the ith hour
        averageHourRange = 2
        numElBefore = averageHourRange -1
        numElAfter = averageHourRange
        # [W m^-2]
        outlierLimitation = 1100.0
        print ("max light intensity:{}".format(np.max(directTiltedSolarRadiation)))
        print ("mean light intensity:{}".format(np.mean(directTiltedSolarRadiation)))

        #First correction. If the solar radiations binding the outlier are zero, then set the outlier zero.
        for i in range (1, hourlySolarIncidenceAngle.shape[0]-1):
            # if directTiltedSolarRadiation[i] > outlierLimitation and (directTiltedSolarRadiation[i -1] == 0.) and (directTiltedSolarRadiation[i + 1] == 0.):
            if (directTiltedSolarRadiation[i -1] == 0.) and (directTiltedSolarRadiation[i + 1] == 0.):
                directTiltedSolarRadiation[i] = 0.0

        # Second correction. If the solar radiations binding the outlier are not zero, then set the outlier the average of solar radiations 1 hour after and before the outlier hour.
        # print ("outlier indices before correction:{}".format([i for i, x in enumerate(directTiltedSolarRadiation) if x > 1.2 * (np.sum(directTiltedSolarRadiation[i-numElBefore :i+numElAfter]) - directTiltedSolarRadiation[i]) / (numElBefore+numElAfter -1.0)]))
        print ("outlier indices before correction:{}".format([i for i, x in enumerate(directTiltedSolarRadiation) if x > outlierLimitation]))
        # this correction was made because some outliers occured by the calculation of directTiltedSolarRadiation (= hourlyHorizontalDirectOuterSolarIrradiance * np.cos(hourlySolarIncidenceAngle) / np.sin(hourlySolarAltitudeAngle))
        # "np.cos(hourlySolarIncidenceAngle) / np.sin(hourlySolarAltitudeAngle)" can be very larger number like 2000
        # if a light intensity [W /m^2] at a certain hour is more than the maximum light intensity by 20%, the value is replaced by the average light intensity before/after 3 hours
        # directTiltedSolarRadiationExcludingOutliers = np.array([(np.sum(directTiltedSolarRadiation[i-numElBefore :i+numElAfter]) - directTiltedSolarRadiation[i]) / float(numElBefore+numElAfter -1.0) if\
        #                                                         x > 1.5 * (np.sum(directTiltedSolarRadiation[i-numElBefore :i+numElAfter]) - directTiltedSolarRadiation[i]) / (numElBefore+numElAfter -1.0) \
        #                                                         else x for i, x in enumerate(directTiltedSolarRadiation) ])
        directTiltedSolarRadiationExcludingOutliers = np.array([(np.sum(directTiltedSolarRadiation[i-numElBefore :i+numElAfter]) - directTiltedSolarRadiation[i]) / float(numElBefore+numElAfter -1.0) if\
                                                                x > outlierLimitation else x for i, x in enumerate(directTiltedSolarRadiation) ])

        print ("outlier indices after correction:{}".format([i for i, x in enumerate(directTiltedSolarRadiationExcludingOutliers) if x > outlierLimitation]))
        ############ outliers data correction end ############

        # print ("outlier indices after correction:{}".format([i for i, x in enumerate(directTiltedSolarRadiationExcludingOutliers) if x > 1.2 * (np.sum(directTiltedSolarRadiationExcludingOutliers[i-numElBefore :i+numElAfter]) - directTiltedSolarRadiationExcludingOutliers[i]) / (numElBefore+numElAfter -1.0)]))
        # print "hourlySolarIncidenceAngle:{}".format(hourlySolarIncidenceAngle)

        # print "directTiltedSolarRadiationExcludingOutliers:{}".format(directTiltedSolarRadiationExcludingOutliers)

        # return directTiltedSolarRadiation
        return directTiltedSolarRadiationExcludingOutliers


def getDiffuseTitledSolarRadiation(simulatorClass, hourlySolarAltitudeAngle, estimatedDiffuseHorizontalSolarRadiation, hourlyHorizontalDiffuseOuterSolarIrradiance = \
        np.zeros(util.calcSimulationDaysInt() * constant.hourperDay)):
    '''
    calculate the diffuse solar radiation to tilted surface. referred to Yano 2009
    :param hourlySolarAltitudeAngle: [rad]
    :param diffuseHorizontalSolarRadiation: [W m^-2]

    :return: maxDirectBeamSolarRadiation [W m^-2]
    '''

    # if (hourlyHorizontalDiffuseOuterSolarIrradiance == 0.0).all():
    if simulatorClass.getEstimateSolarRadiationMode() == True:

        print("at OPVFilm.getDiffuseTitledSolarRadiation, hourlyHorizontalDiffuseOuterSolarIrradiance does not have data")
        # if there is no data about solar radiation, assume the solar radiation from the following equation, which is cited from A. Yano, "electrical energy generated by photovoltaic modules mounted inside the roof of a north-south oriented greenhouse", 2009
        diffuseTiltedSolarRadiation = estimatedDiffuseHorizontalSolarRadiation * (1 + np.cos(constant.OPVAngle)) / 2.0
    else:
        print("at OPVFilm.getDiffuseTitledSolarRadiation, hourlyHorizontalDiffuseOuterSolarIrradiance has data")
        diffuseTiltedSolarRadiation = hourlyHorizontalDiffuseOuterSolarIrradiance * (1 + np.cos(constant.OPVAngle)) / 2.0

    # diffuse tilted solar radiation is defined as 0 when the elevation/altitude angle is <= 0
    for i in range (0, hourlySolarAltitudeAngle.shape[0]):
        if hourlySolarAltitudeAngle[i] < 0.0:
            diffuseTiltedSolarRadiation[i] = 0.0

    return diffuseTiltedSolarRadiation


def getAlbedoTitledSolarRadiation(simulatorClass, hourlySolarAltitudeAngle, estimatedTotalHorizontalSolarRadiation,  hourlyHorizontalTotalOuterSolarIrradiance = \
        np.zeros(util.calcSimulationDaysInt() * constant.hourperDay)):
    '''
    calculate the albedo (reflection) solar radiation to tilted surface. referred to Yano 2009
    :param diffuseHorizontalSolarRadiation: [W m^-2]
    :param hourlySolarAltitudeAngle: [rad]
    :return: totalHorizontalSolarRadiation [W m^-2]
    '''

    # if (hourlyHorizontalTotalOuterSolarIrradiance == 0.0).all():
    if simulatorClass.getEstimateSolarRadiationMode() == True:

        print("at OPVFilm.getAlbedoTitledSolarRadiation, getAlbedoTitledSolarRadiation does not have data")
        # if there is no data about solar radiation, assume the solar radiation from the following equation, which is cited from A. Yano, "electrical energy generated by photovoltaic modules mounted inside the roof of a north-south oriented greenhouse", 2009
        albedoTiltedSolarRadiation = constant.groundReflectance * estimatedTotalHorizontalSolarRadiation * (1 - np.cos(constant.OPVAngle)) / 2.0
    else:
        print("at OPVFilm.getAlbedoTitledSolarRadiation, getAlbedoTitledSolarRadiation has data")
        albedoTiltedSolarRadiation = constant.groundReflectance * hourlyHorizontalTotalOuterSolarIrradiance * (1 - np.cos(constant.OPVAngle)) / 2.0

    # diffuse tilted solar radiation is defined as 0 when the elevation/altitude angle is <= 0
    for i in range (0, hourlySolarAltitudeAngle.shape[0]):
        # if abs(hourlySolarAltitudeAngle[i]) <= 0.0:
        if hourlySolarAltitudeAngle[i] < 0.0:
            albedoTiltedSolarRadiation[i] = 0.0

    return albedoTiltedSolarRadiation


def calcDirectBeamSolarRadiationNormalToTiltedOPVKacira2003(hourlySolarAltitudeAngle,maxDirectBeamSolarRadiation, hourlySolarIncidenceAngle):
    '''
    calculate the max direct beam solar radiation perpendicular to the tilted OPV
    :param hourlySolarAltitudeAngle: [rad]
    :param maxDirectBeamSolarRadiation: [W m^-2]
    :param hourlySolarIncidenceAngle: [rad]
    :return: directBeamSolarRadiationNormalToTiltedOPV [W m^-2]
    '''

    directBeamSolarRadiationNormalToTiltedOPV = np.zeros(hourlySolarAltitudeAngle.shape[0])
    # print "directBeamSolarRadiationNormalToTiltedOPV:{}".format(directBeamSolarRadiationNormalToTiltedOPV)

    # if the altitude angle is minus, it means it is night. Thus, the directBeamSolarRadiationNormalToTiltedOPV becomes zero.
    for i in range (0, hourlySolarAltitudeAngle.shape[0]):
        if hourlySolarAltitudeAngle[i] < 0.0:
            directBeamSolarRadiationNormalToTiltedOPV[i] = 0.0
        else:
            directBeamSolarRadiationNormalToTiltedOPV[i] = maxDirectBeamSolarRadiation[i] * np.cos(hourlySolarIncidenceAngle[i])

    # print"maxDirectBeamSolarRadiation:{}".format(maxDirectBeamSolarRadiation)
    # print "np.degrees(hourlySolarIncidenceAngle):{}".format(np.degrees(hourlySolarIncidenceAngle))


    return directBeamSolarRadiationNormalToTiltedOPV

def calcOPVElectricEnergyperArea(simulatorClass, hourlyOPVTemperature, solarRadiationToOPV):
    '''
    calculate the electric energy per OPV area during the defined days [J/day/m^2]
    :param hourlyOPVTemperature:
    :param Popvin:
    :return:
    '''
    # print("at OPVfilm.py, hourlyOPVTemperature.shape:{}".format(hourlyOPVTemperature.shape))

    dailyJopvout = np.zeros(util.calcSimulationDaysInt())

    # make the list of OPV coverage ratio at each hour changing during summer
    # OPVAreaCoverageRatioChangingInSummer = getDifferentOPVCoverageRatioInSummerPeriod(constant.OPVAreaCoverageRatio, simulatorClass)

    # the PV module degradation ratio by time
    PVDegradationRatio = np.array([1.0 - constant.PVDegradationRatioPerHour * i for i in range (0, hourlyOPVTemperature.shape[0])])

    for day in range (0, util.calcSimulationDaysInt()):
        # print "day:{}, Popvin[day*constant.hourperDay : (day+1)*constant.hourperDay]:{}".format(day, Popvin[day*constant.hourperDay : (day+1)*constant.hourperDay])
        # unit: [W/m^2] -> [J/m^2] per day
        dailyJopvout[day] = calcOPVElectricEnergyperAreaperDay(\
            hourlyOPVTemperature[day*constant.hourperDay : (day+1)*constant.hourperDay], \
            solarRadiationToOPV[day*constant.hourperDay : (day+1)*constant.hourperDay], PVDegradationRatio[day*constant.hourperDay : (day+1)*constant.hourperDay])


    return dailyJopvout

def calcOPVElectricEnergyperAreaperDay(hourlyOPVTemperature, Popvin, PVDegradationRatio):
    '''
    calculate the electric energy per OPV area only for a  day [J/day/m^2]
    [the electric energy per OPV area per day]
    W_opvout=0.033∫_(t_sunrise)^(t_sunset) (1+C_Voctemp * (T_opv - 25[°C]))(1+ C_Isctemp * (T_opv - 25[°C])) * P_opvin
    param: Popvin: Hourly Outer Light Intensity [Watt/m^2] = [J/second/m^2]
    param: HourlyOuterTemperature: Hourly Outer Temperature [Celsius/hour]
    return: Wopvout, scalar: OPV Electric Energy production per Area per day [J/day/m^2].
    '''
    #unit [W/m^2]
    JopvoutAday = 0

    ##change the unit from second to hour [J/second/m^2] -> [J/hour/m^2]
    Popvin = Popvin * 60.0 * 60.0

    #print"int(constant.hourperDay):{}".format(int(constant.hourperDay))
    #calculate the electric energy per OPV area (watt/m^2)
    for hour in range (0, int(constant.hourperDay)):
        # Jopvout += constant.OPVEfficiencyRatioSTC * constant.degradeCoefficientFromIdealtoReal * \
        #            (1.0 + constant.TempCoeffitientVmpp * (hourlyOPVTemperature[hour] - constant.STCtemperature)) * \
        #            (1.0 + constant.TempCoeffitientImpp * (hourlyOPVTemperature[hour] - constant.STCtemperature)) * \
        #            Popvin [hour]
        JopvoutAday += constant.OPVEfficiencyRatioSTC * constant.degradeCoefficientFromIdealtoReal * PVDegradationRatio[hour] * \
                   (1.0 + constant.TempCoeffitientPmpp * (hourlyOPVTemperature[hour] - constant.STCtemperature)) * Popvin[hour]

    #print "Jopvout:{} (J/m^2)".format(Wopvout)
    return JopvoutAday

def getMonthlyElectricityProductionFromDailyData (dailyElectricityPerArea, yearOfeachDay, monthOfeachDay):
    '''
    summing the daily electricity produce to monthly produce
    '''
    # print "yearOfeachDay:{}".format(yearOfeachDay)
    # print "monthOfeachDay:{}".format(monthOfeachDay)

    numOfMonths = util.getSimulationMonthsInt()
    # print "numOfMonths:{}".format(numOfMonths)
    monthlyElectricityPerArea = np.zeros(numOfMonths)
    month = 0
    # insert the initial value
    monthlyElectricityPerArea[month] += dailyElectricityPerArea[0]
    for day in range (1, util.calcSimulationDaysInt()):
        if monthOfeachDay[day-1] != monthOfeachDay[day]:
            month += 1
        monthlyElectricityPerArea[month] += dailyElectricityPerArea[day]

    return monthlyElectricityPerArea

def getMonthlyElectricitySalesperArea(monthlyKWhopvoutperArea, monthlyResidentialElectricityPrice):
    '''

    :param monthlyKWhopvoutperArea:
    :param monthlyResidentialElectricityPrice:
    :return: [USD/month/m^2]
    '''
    # devided by 100 to convert [USCent] into [USD]
    return monthlyKWhopvoutperArea * (monthlyResidentialElectricityPrice / 100.0)


def calcRevenueOfElectricityProductionperMonth(WopvoutperHarvestperMonth, monthlyAverageElectricityPrice):
    '''
    calculate the electric energy wholesale price per month.
    param: WopvoutperHarvestperMonth: electric energy produced per month with given area [J/month]
    param: monthlyTucsonAverageWholesalelPriceOfElectricity: wholesale price of electricity in Tucson [USD/Mega Watt hour (MWh) for each month]

    return: revenueOfElectricityProductionperMonth, scalar: the wholesale price revenue of electricity per month (USD/month).
    '''
    #unit conversion [J/month = Watt*sec/month -> MWh/month]
    #WopvoutperHarvestMWhperMonth = WopvoutperHarvestperMonth * 3600.0 / (10.0**6)
    WopvoutperHarvestMWhperMonth = WopvoutperHarvestperMonth / (10.0**6) / 3600.0
    #print "WopvoutperHarvestMWhperMonth:{}".format(WopvoutperHarvestMWhperMonth)
    #print "monthlyTucsonAverageWholesalelPriceOfElectricity:{}".format(monthlyTucsonAverageWholesalelPriceOfElectricity)

    #unit: USD/month
    revenueOfElectricityProductionperMonth = WopvoutperHarvestMWhperMonth * monthlyAverageElectricityPrice
    #print "revenueOfElectricityProductionperMonth(USD/month):{}".format(revenueOfElectricityProductionperMonth)

    return revenueOfElectricityProductionperMonth


def calcCostofElectricityProduction(OPVArea):
    '''
    calculate the cost to install OPV film

    param: OPVArea: area of OPV film (m^2)

    return: cost for the OPV film (USD)

    '''
    return OPVArea * constant.OPVPricePerAreaUSD


def getDirectSolarIrradianceBeforeShadingCurtain(simulatorClass):

    # get the direct solar irradiance after penetrating multi span roof [W/m^2]
    hourlyDirectSolarRadiationAfterMultiSpanRoof = simulatorClass.getHourlyDirectSolarRadiationAfterMultiSpanRoof()

    # OPVAreaCoverageRatio = simulatorClass.getOPVAreaCoverageRatio()
    OPVAreaCoverageRatio = constant.OPVAreaCoverageRatio
    # ShadingCurtainDeployPPFD = simulatorClass.getShadingCurtainDeployPPFD()
    OPVPARTransmittance = constant.OPVPARTransmittance

    # make the list of OPV coverage ratio at each hour changing during summer
    OPVAreaCoverageRatioChangingInSummer = getDifferentOPVCoverageRatioInSummerPeriod(OPVAreaCoverageRatio, simulatorClass)
    # print("OPVAreaCoverageRatioChangingInSummer:{}".format(OPVAreaCoverageRatioChangingInSummer))

    # consider the transmission ratio of OPV film
    hourlyDirectSolarRadiationAfterOPVAndRoof = hourlyDirectSolarRadiationAfterMultiSpanRoof * (1 - OPVAreaCoverageRatioChangingInSummer) \
                                                + hourlyDirectSolarRadiationAfterMultiSpanRoof * OPVAreaCoverageRatioChangingInSummer * OPVPARTransmittance
    # print "OPVAreaCoverageRatio:{}, HourlyInnerLightIntensityPPFDThroughOPV:{}".format(OPVAreaCoverageRatio, HourlyInnerLightIntensityPPFDThroughOPV)

    # consider the light reduction by greenhouse inner structures and equipments like pipes, poles and gutters
    hourlyDirectSolarRadiationAfterInnerStructure = (1 - constant.GreenhouseShadeProportionByInnerStructures) * hourlyDirectSolarRadiationAfterOPVAndRoof
    # print "hourlyInnerLightIntensityPPFDThroughInnerStructure:{}".format(hourlyInnerLightIntensityPPFDThroughInnerStructure)

    return hourlyDirectSolarRadiationAfterInnerStructure


def getDirectSolarIrradianceToPlants(simulatorClass, hourlyDirectSolarRadiationAfterInnerStructure):

    hasShadingCurtain = simulatorClass.getIfHasShadingCurtain()

    # take date and time
    year = simulatorClass.getYear()
    month = simulatorClass.getMonth()
    day = simulatorClass.getDay()
    hour = simulatorClass.getHour()

    # array storing the light intensity after penetrating the shading curtain
    hourlyDirectSolarRadiationAfterShadingCurtain= np.zeros(hour.shape[0])

    # consider the shading curtain
    if hasShadingCurtain == True:
        # if the date is between the following time and date, discount the irradiance by the shading curtain transmittance.
        # if we assume the shading curtain is deployed all time for the given period,
        if constant.IsShadingCurtainDeployOnlyDayTime == False:
            for i in range(0, hour.shape[0]):
                if (datetime.date(year[i], month[i], day[i]) >=  datetime.date(year[i], constant.ShadingCurtainDeployStartMMSpring, constant.ShadingCurtainDeployStartDDSpring ) and \
                    datetime.date(year[i], month[i], day[i]) <= datetime.date(year[i], constant.ShadingCurtainDeployEndMMSpring, constant.ShadingCurtainDeployEndDDSpring)) or\
                    (datetime.date(year[i], month[i], day[i]) >=  datetime.date(year[i], constant.ShadingCurtainDeployStartMMFall, constant.ShadingCurtainDeployStartDDFall ) and \
                    datetime.date(year[i], month[i], day[i]) <= datetime.date(year[i], constant.ShadingCurtainDeployEndMMFall, constant.ShadingCurtainDeployEndDDFall)):
                    # deploy the shading curtain
                    hourlyDirectSolarRadiationAfterShadingCurtain[i] = hourlyDirectSolarRadiationAfterInnerStructure[i] * constant.shadingTransmittanceRatio

                else:
                    # not deploy the curtain
                    hourlyDirectSolarRadiationAfterShadingCurtain[i] = hourlyDirectSolarRadiationAfterInnerStructure[i]

        # if we assume the shading curtain is deployed only for a fixed hot time defined at the constant class in a day, use this
        elif constant.IsShadingCurtainDeployOnlyDayTime == True and constant.IsDifferentShadingCurtainDeployTimeEachMonth == False:

            for i in range(0, hour.shape[0]):
                if (datetime.date(year[i], month[i], day[i]) >=  datetime.date(year[i], constant.ShadingCurtainDeployStartMMSpring, constant.ShadingCurtainDeployStartDDSpring ) and \
                    datetime.date(year[i], month[i], day[i]) <= datetime.date(year[i], constant.ShadingCurtainDeployEndMMSpring, constant.ShadingCurtainDeployEndDDSpring) and \
                    hour[i] >= constant.ShadigCuratinDeployStartHH and hour[i] <= constant.ShadigCuratinDeployEndHH) or\
                    (datetime.date(year[i], month[i], day[i]) >=  datetime.date(year[i], constant.ShadingCurtainDeployStartMMFall, constant.ShadingCurtainDeployStartDDFall ) and \
                    datetime.date(year[i], month[i], day[i]) <= datetime.date(year[i], constant.ShadingCurtainDeployEndMMFall, constant.ShadingCurtainDeployEndDDFall) and \
                    hour[i] >= constant.ShadigCuratinDeployStartHH and hour[i] <= constant.ShadigCuratinDeployEndHH):
                    # deploy the shading curtain
                    hourlyDirectSolarRadiationAfterShadingCurtain[i] = hourlyDirectSolarRadiationAfterInnerStructure[i] * constant.shadingTransmittanceRatio

                else:
                    # not deploy the curtain
                    hourlyDirectSolarRadiationAfterShadingCurtain[i] = hourlyDirectSolarRadiationAfterInnerStructure[i]

        # if we assume the shading curtain is deployed for the time which dynamically changes each month, use this
        elif constant.IsShadingCurtainDeployOnlyDayTime == True and constant.IsDifferentShadingCurtainDeployTimeEachMonth == True:

            # having shading curtain transmittance each hour. 1 = no shading curatin, the transmittance of shading curtain = deploy curtain
            transmittanceThroughShadingCurtainChangingEachMonth = simulatorClass.transmittanceThroughShadingCurtainChangingEachMonth

            hourlyDirectSolarRadiationAfterShadingCurtain = hourlyDirectSolarRadiationAfterInnerStructure * transmittanceThroughShadingCurtainChangingEachMonth

        return hourlyDirectSolarRadiationAfterShadingCurtain

def getDiffuseSolarIrradianceBeforeShadingCurtain(simulatorClass):

    # get the diffuse solar irradiance, which has not consider the transmittance of OPV film yet.
    # diffuseHorizontalSolarRadiation = simulatorClass.getDiffuseSolarRadiationToOPV()
    diffuseHorizontalSolarRadiation = simulatorClass.diffuseHorizontalSolarRadiation
    # print("diffuseHorizontalSolarRadiation.shape:{}".format(diffuseHorizontalSolarRadiation.shape))

    # consider the influecne of the PV module on the roof
    overallRoofCoveringTrasmittance = constant.roofCoveringTransmittance * (1 - constant.OPVAreaCoverageRatio) + \
                                      (constant.roofCoveringTransmittance + constant.OPVPARTransmittance) * constant.OPVAreaCoverageRatio
    # get the average transmittance through roof and sidewall
    transmittanceThroughWallAndRoof = (constant.greenhouseSideWallArea * constant.sideWallTransmittance + constant.greenhouseTotalRoofArea * overallRoofCoveringTrasmittance) \
                                      / (constant.greenhouseSideWallArea + constant.greenhouseTotalRoofArea)
    # consider the light reflection by greenhouse inner structures and equipments like pipes, poles and gutters
    transmittanceThroughInnerStructure = (1 - constant.GreenhouseShadeProportionByInnerStructures) * transmittanceThroughWallAndRoof

    hourlyDiffuseSolarRadiationAfterShadingCurtain = diffuseHorizontalSolarRadiation * transmittanceThroughInnerStructure

    return hourlyDiffuseSolarRadiationAfterShadingCurtain


def getDiffuseSolarIrradianceToPlants(simulatorClass, hourlyDiffuseSolarRadiationAfterShadingCurtain):
    '''
    the diffuse solar radiation was calculated by multiplying the average transmittance of all covering materials of the greenhouse (side wall, roof and PV module
    '''

    transmittanceThroughShadingCurtainChangingEachMonth = simulatorClass.transmittanceThroughShadingCurtainChangingEachMonth
    # print("at OPVFilm, getDiffuseSolarIrradianceToPlants, transmittanceThroughShadingCurtainChangingEachMonth:{}".format(transmittanceThroughShadingCurtainChangingEachMonth))

    # consider the influence of shading curtain
    transmittanceThroughShadingCurtain = (constant.greenhouseSideWallArea + transmittanceThroughShadingCurtainChangingEachMonth * constant.greenhouseFloorArea) / (constant.greenhouseSideWallArea + constant.greenhouseFloorArea)

    # get the diffuse solar irradiance after penetrating the greenhouse cover material
    diffuseSolarIrradianceToPlants = hourlyDiffuseSolarRadiationAfterShadingCurtain * transmittanceThroughShadingCurtain

    return diffuseSolarIrradianceToPlants


def calcHourlyInnerLightIntensityPPFD(HourlyOuterLightIntensityPPFD, OPVAreaCoverageRatio, OPVPARTransmissionRatio, hasShadingCurtain=False, \
                                      shadingCurtainDeployPPFD=constant.shadingCurtainDeployPPFD, cropElectricityYieldSimulator1 = None):
    '''
    calculate the light intensity inside the greenhouse (inner light intensity) each hour

    param:HourlyOuterLightIntensityPPFD, vector: [μmol/m^2/s]
    param:OPVAreaCoverageRatio: the ratio that OPV film covers the roof
    param:OPVPARTransmissionRatio: the ratio of OPV film light transmittance
    param:hasShadingCurtain:
    param:shadingCurtainDeployPPFD: the baseline of shading curtain opening/closing
    param:cropElectricityYieldSimulator1: instance

    return: vector: [μmol/m^2/s]
    '''

    #consider the transmittance ratio of glazing
    InnerLightIntensityPPFDThroughGlazing = constant.dobulePERTransmittance * HourlyOuterLightIntensityPPFD
    # print "OPVAreaCoverageRatio:{}, HourlyOuterLightIntensityPPFD:{}".format(OPVAreaCoverageRatio, HourlyOuterLightIntensityPPFD)
    # print "OPVAreaCoverageRatio:{}, InnerLightIntensityPPFDThroughGlazing:{}".format(OPVAreaCoverageRatio, InnerLightIntensityPPFDThroughGlazing)

    # make the list of OPV coverage ratio at each hour fixing the ratio during summer
    oPVAreaCoverageRatioFixingInSummer = getDifferentOPVCoverageRatioInSummerPeriod(OPVAreaCoverageRatio, cropElectricityYieldSimulator1)

    # TODO the light intensity decrease by OPV film will be considered in calculating the solar iiradiance to multispan roof. move this calculation to CropElecricityYieldSimulationDetail.getSolarIrradianceToMultiSpanRoof in the future.
    #consider the transmission ratio of OPV film
    HourlyInnerLightIntensityPPFDThroughOPV = InnerLightIntensityPPFDThroughGlazing * (1 - oPVAreaCoverageRatioFixingInSummer) + InnerLightIntensityPPFDThroughGlazing * oPVAreaCoverageRatioFixingInSummer * OPVPARTransmissionRatio
    # print "OPVAreaCoverageRatio:{}, HourlyInnerLightIntensityPPFDThroughOPV:{}".format(OPVAreaCoverageRatio, HourlyInnerLightIntensityPPFDThroughOPV)

    #consider the light reflection by greenhouse inner structures and equipments like pipes, poles and gutters
    hourlyInnerLightIntensityPPFDThroughInnerStructure = (1 - constant.GreenhouseShadeProportionByInnerStructures) * HourlyInnerLightIntensityPPFDThroughOPV
    # print "hourlyInnerLightIntensityPPFDThroughInnerStructure:{}".format(hourlyInnerLightIntensityPPFDThroughInnerStructure)
    # set the value to the instance
    # cropElectricityYieldSimulator1.setHourlyInnerLightIntensityPPFDThroughInnerStructure(hourlyInnerLightIntensityPPFDThroughInnerStructure)

    # set the value to the instance
    cropElectricityYieldSimulator1.setHourlyInnerLightIntensityPPFDThroughGlazing(InnerLightIntensityPPFDThroughGlazing)
    cropElectricityYieldSimulator1.setHourlyInnerLightIntensityPPFDThroughInnerStructure(hourlyInnerLightIntensityPPFDThroughInnerStructure)

    # take date and time
    year = cropElectricityYieldSimulator1.getYear()
    month = cropElectricityYieldSimulator1.getMonth()
    day = cropElectricityYieldSimulator1.getDay()
    hour = cropElectricityYieldSimulator1.getHour()

    # array storing the light intensity after penetrating the shading curtain
    hourlyInnerLightIntensityPPFDThroughShadingCurtain = np.zeros(hour.shape[0])
    # consider the shading curtain
    if hasShadingCurtain == True:
        # if te date is between the following time and date, then discount the PPFD by the shading curtain transmittance the information about date is taken from  cropElectricityYieldSimulator1 object
        # if we assume the shading curtain is deployed whole day for the given period,
        if constant.IsShadingCurtainDeployOnlyDayTime == False:
            for i in range(0, hour.shape[0]):
                if (datetime.date(year[i], month[i], day[i]) >=  datetime.date(year[i], constant.ShadingCurtainDeployStartMMSpring, constant.ShadingCurtainDeployStartDDSpring ) and \
                    datetime.date(year[i], month[i], day[i]) <= datetime.date(year[i], constant.ShadingCurtainDeployEndMMSpring, constant.ShadingCurtainDeployEndDDSpring)) or\
                    (datetime.date(year[i], month[i], day[i]) >=  datetime.date(year[i], constant.ShadingCurtainDeployStartMMFall, constant.ShadingCurtainDeployStartDDFall ) and \
                    datetime.date(year[i], month[i], day[i]) <= datetime.date(year[i], constant.ShadingCurtainDeployEndMMFall, constant.ShadingCurtainDeployEndDDFall)):
                    # deploy the shading curtain
                    hourlyInnerLightIntensityPPFDThroughShadingCurtain[i] = hourlyInnerLightIntensityPPFDThroughInnerStructure[i] * constant.shadingTransmittanceRatio

                else:
                    # not deploy the curtain
                    hourlyInnerLightIntensityPPFDThroughShadingCurtain[i] = hourlyInnerLightIntensityPPFDThroughInnerStructure[i]

            return hourlyInnerLightIntensityPPFDThroughShadingCurtain

        # if we assume the shading curtain is deployed only for a certain hot time in a day,
        elif constant.IsShadingCurtainDeployOnlyDayTime == True:
            for i in range(0, hour.shape[0]):
                if (datetime.date(year[i], month[i], day[i]) >=  datetime.date(year[i], constant.ShadingCurtainDeployStartMMSpring, constant.ShadingCurtainDeployStartDDSpring ) and \
                    datetime.date(year[i], month[i], day[i]) <= datetime.date(year[i], constant.ShadingCurtainDeployEndMMSpring, constant.ShadingCurtainDeployEndDDSpring) and \
                    hour[i] >= constant.ShadigCuratinDeployStartHH and hour[i] <= constant.ShadigCuratinDeployEndHH) or\
                    (datetime.date(year[i], month[i], day[i]) >=  datetime.date(year[i], constant.ShadingCurtainDeployStartMMFall, constant.ShadingCurtainDeployStartDDFall ) and \
                    datetime.date(year[i], month[i], day[i]) <= datetime.date(year[i], constant.ShadingCurtainDeployEndMMFall, constant.ShadingCurtainDeployEndDDFall) and \
                    hour[i] >= constant.ShadigCuratinDeployStartHH and hour[i] <= constant.ShadigCuratinDeployEndHH):
                    # deploy the shading curtain
                    hourlyInnerLightIntensityPPFDThroughShadingCurtain[i] = hourlyInnerLightIntensityPPFDThroughInnerStructure[i] * constant.shadingTransmittanceRatio

                else:
                    # not deploy the curtain
                    hourlyInnerLightIntensityPPFDThroughShadingCurtain[i] = hourlyInnerLightIntensityPPFDThroughInnerStructure[i]

            return hourlyInnerLightIntensityPPFDThroughShadingCurtain

        # the shading curtain algorithm which open/close shading curatin each hour
        # if PPFD is over hourlyInnerLightIntensityPPFD, then deploy the shading curtain, and decrease PPFD. otehrwise leave it
        # hourlyInnerLightIntensityPPFDThroughShadingCurtain = np.array([x * constant.shadingTransmittanceRatio\
        #     if x > shadingCurtainDeployPPFD else x for x in hourlyInnerLightIntensityPPFDThroughInnerStructure])
        # print "InnerLightIntensityPPFDThroughShadingCurtain:{}".format(InnerLightIntensityPPFDThroughShadingCurtain)
        # return hourlyInnerLightIntensityPPFDThroughShadingCurtain

    # come to here when not considering shading curtain
    return hourlyInnerLightIntensityPPFDThroughInnerStructure


def getDifferentOPVCoverageRatioInSummerPeriod(OPVAreaCoverageRatio, simulatorClass):
    '''
    this function changes the opv coverage ratio during the summer period into the constant ratio defined at the constant class.,

    :param OPVPARTransmissionRatio:
    :param cropElectricityYieldSimulator1:
    :return:
    '''

    # take date and time
    year = simulatorClass.getYear()
    month = simulatorClass.getMonth()
    day = simulatorClass.getDay()

    OPVCoverageRatio = np.zeros(year.shape[0])

    for i in range(0, year.shape[0]):
        # if it is during the summer period when shading curtain is deployed.
        if datetime.date(year[i], month[i], day[i]) >=  datetime.date(year[i], constant.SummerPeriodStartMM, constant.SummerPeriodStartDD) and \
            datetime.date(year[i], month[i], day[i]) <= datetime.date(year[i], constant.SummerPeriodEndMM, constant.SummerPeriodEndDD):
            OPVCoverageRatio[i] = constant.OPVAreaCoverageRatioSummerPeriod
        else:
            OPVCoverageRatio[i] = OPVAreaCoverageRatio

    # set the array to the  objec
    simulatorClass.OPVCoverageRatiosConsiderSummerRatio = OPVCoverageRatio
    # print("OPVCoverageRatio:{}".format(OPVCoverageRatio))

    return OPVCoverageRatio
