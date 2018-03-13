# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 06 Nov 2016
# last edit date: 19 Apr 2017
#######################################################

##########import package files##########
import numpy as np
import math

#########################################################################
########### Reinforcement Learning (RL) constants start##################
#########################################################################
# labels of weights for features
w_0 = "bias(w_0)"
##### 1 DLI to plants with the state and action
w_1 = "DLIEachDayToPlants(w_1)"
##### 2 plant weight increase with the state and action
w_2 = "unitDailyFreshWeightIncrease(w_2)"
##### 3 plant weight at the state
w_3 = "accumulatedUnitDailyFreshWeightIncrease(w_3)"
##### 4 averageDLITillTheDay
w_4 = "averageDLITillHarvestDay(w_4)"
##### 5 season effects (winter) representing dates.
w_5 = "isSpring(w_5)"
##### 6 season effects (spring) representing dates.
w_6 = "isSummer(w_6)"
##### 7 season effects (summer) representing dates.
w_7 = "isAutumn(w_7)"
##### 8 season effects (autumn) representing dates.
w_8 = "isWinter(w_8)"

# starts from middle of Feb
daysFromJanStartApril = 45
# starts from May first
daysFromJanStartSummer = 121
# starts from middle of September
daysFromJanStartAutumn = 259
# starts from middle of Winter
daysFromJanStartWinter = 320

fileNameQLearningTrainedWeight = "qLearningTraintedWeights"

ifRunTraining = True
ifSaveCalculatedWeight = True
ifLoadWeight = True
##############################################
########### RL constants end##################
##############################################


###############################################################
####################### If branch start #######################
###############################################################
# True: use the real data (the imported data whose source is the local weather station "https://midcdmz.nrel.gov/ua_oasis/),
# False: use the
ifUseOnlyRealData = False
# ifUseOnlyRealData = True

#If True,  export measured horizontal and estimated data when the simulation day is one day.
ifExportMeasuredHorizontalAndExtimatedData = True

#If True, export measured horizontal and estimated data only on 15th day each month.
ifGet15thDayData = False
#############################################################
####################### If branch end #######################
#############################################################

########################################
##########other constant start##########
########################################
# day on each month: days of Jan, Feb, ...., December
dayperMonthArray = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
dayperMonthLepArray = np.array([31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

# keep them int
secondperMinute = 60
minuteperHour = 60
hourperDay = 24
dayperYear = 365
monthsperYear = 12
dayperLeapYear = 366
noonHour = 12

#the temperature at STC (Standard Test Conditions) unit [Celsius]
STCtemperature = 25.0
#Simulation Period (days)
SimulationPeriodDays = 365.0
# current prepared data range: 20130101-20170101", 20150101 to 20160815 was the only correctly observed period. some 2014 data work too.
# do not choose "20140201 to 20160101" specifically. somehow it does not work.
# do not include 1/19/2014 as start date because 1/19/2014 partially misses its hourly data
# do not include after 8/18/2016 because the dates after 8/18/2016 do not correctly log the body temperature.
SimulationStartDate="20150101"
# SimulationEndDate = "20151231"
SimulationEndDate = "20150103"
# one cultivation cycle
# SimulationEndDate = "20150204"

sunnyDaysList = ["20150115", "20150217", "20150316", "20150413", "20150517", "20150615", "20150711", "20150815", "20150918", "20151013", "20151117", "20151215"]

# latitude at Tucson == 32.2800408 N
Latitude = math.radians(32.2800408)
# longitude at Tucson 110.9422745 W
Longitude = math.radians(110.9422745)
# lambda (longitude of the site) = 32.2800408 N: latitude,-110.9422745 W : longitude  [degree]
# lambda_R ( the longitude of the time zone in which the site is situated) = 33.4484, 112.074 [degree]
# J' (the day angle in the year ) =

# John Page, "The Role of Solar-Radiation Climatology in the Design of Photovoltaic Systems", 2nd edition
# there is a equation calculating LAT.

# p618 (46 in pdf file)
# The passage of days is described mathematically by numbering the days continuously through the year to produce a Julian day number, J: 1
# January, J 5 1; 1 February, J 5 32; 1 March, J 5 57 in a nonleap year and 58 in a leap year; and so on. Each day in the year can be then be
# expressed in an angular form as a day angle, J0, in degrees by multiplying
# J by 360/365.25. The day angle is used in the many of the trigonometric expressions that follow.
# EOT (equation of time) =

#watt To PPFD Conversion coefficient for sunlight  (W m^-2) -> (μmol/m^2/s)
# the range of wavelength considered is around from 280 to 2800 (shortwave sunlight), not from 400nm to 700nm (visible sunlight).
wattToPPFDConversionRatio = 2.05
# wattToPPFDConversionRatio = 4.57 <- this ratio is used when the range of wavelength of PAR [W m^-2] is between 400nm and 700nm (visible sunlight)

# [W/m^2]
solarConstant = 1367.0
# ground reflectance of sunlight. source: https://www2.pvlighthouse.com.au/resources/courses/altermatt/The%20Solar%20Spectrum/The%20reflectance%20of%20the%20ground.aspx
groundReflectance = 0.1
# referred from A. Yano et. al., 2009, "Electrical energy generated by photovoltaic modules mounted inside the roof of a north–south oriented greenhouse"
# this number should be carefully definted according to the weather property of the simulation region (very cloudy: 0.0 ~ 1.0: very sunny)
atmosphericTransmissivity = 0.75

# unit conversion. [cwt] -> [kg] US standard
kgpercwt = 45.36
######################################
##########other constant end##########
######################################


#########################################################
##########Specification of the greenhouse start##########
#########################################################

# #########################################################
# # Our real greenhouse specification source:
# # http://www.gpstructures.com/pdfs/Windjammer.pdf
# # We used 6' TALL SIDEWALL HEIGHT 30' width, Free Standing Structures in our project.
# #greenhouse roof type
# greenhouseRoofType = "SimplifiedAFlame"
# #width of the greenhouse (m)
# greenhouseWidth = 9.144 # = 30 [feet]
# #depth of the greenhouse (m)
# greenhouseDepth = 14.6
# #area of the greenhouse (m**2)
# greenhouseFloorArea = greenhouseWidth * greenhouseDepth
# # print("greenhouseFloorArea[m^2]:{}".format(greenhouseFloorArea))
# #width of the greenhouse cultivation area (m)
# greenhouseCultivationFloorWidth = 7.33
# #depth of the greenhouse cultivation area(m)
# greenhouseCultivationFloorDepth = 10.89
# #floor area of greenhouse cultivation area(m**2)
# greenhouseCultivationFloorArea = greenhouseCultivationFloorWidth * greenhouseCultivationFloorDepth
# # greenhouseCultivationFloorArea = greenhouseWidth * greenhouseDepth * 0.9
# # print("greenhouseCultivationFloorArea[m^2]:{}".format(greenhouseCultivationFloorArea))
# # number of spans. If this is 1, the greenhouse is a single span greenhouse. If >1, multi-span greenhouse
# numOfSpans = 1
# # the type of roof direction
# roofDirectionNotation = "EastWestDirectionRoof"
# #side wall height of greenhouse (m)
# greenhouseHeightSideWall = 1.8288 # = 6[feet]
# #center height of greenhouse (m)
# greenhouseHeightRoofTop = 4.8768 # = 16[feet]
# #width of the rooftop. calculate from the Pythagorean theorem. assumed that the shape of rooftop is straight, not curved.
# greenhouseRoofWidth = math.sqrt((greenhouseWidth/2.0)**2.0 + (greenhouseHeightRoofTop-greenhouseHeightSideWall)**2.0)
# #print ("greenhouseRoofWidth: {}".format(greenhouseRoofWidth))
# #angle of the rooftop (theta θ). [rad]
#
# greenhouseRoofAngle = math.acos((greenhouseWidth/2.0) / greenhouseRoofWidth)
# # print ("greenhouseRoofAngle (rad) : {}".format(greenhouseRoofAngle))
# # the angle of the roof facing north or east [rad]
# roofAngleNorthOrEast = greenhouseRoofAngle
# # the angle of the roof facing south or west [rad]. This should be modified if the roof angle is different from the other side.
# roofAngleWestOrSouth = greenhouseRoofAngle
# #area of the rooftop [m^2]. summing the left and right side of rooftops from the center.
# greenhouseTotalRoofArea = greenhouseRoofWidth * greenhouseDepth * 2.0
# # print ("greenhouseRoofArea[m^2]: {}".format(greenhouseTotalRoofArea))1
# #########################################################


#########################################################
# Virtual greenhouse specification, the multi-span greenhouse virtually connected 10 of our real greenhouses.
# You can change these numbers according to your greenhouse design and specification
#greenhouse roof type
greenhouseRoofType = "SimplifiedAFlame"
#width of the greenhouse (m)
greenhouseWidth = 91.44 #
#depth of the greenhouse (m)
greenhouseDepth = 14.6
#area of the greenhouse (m**2)
greenhouseFloorArea = greenhouseWidth * greenhouseDepth
print("greenhouseFloorArea[m^2]:{}".format(greenhouseFloorArea))
#width of the greenhouse cultivation area (m)
greenhouseCultivationFloorWidth = 73.3
#depth of the greenhouse cultivation area(m)
greenhouseCultivationFloorDepth = 10.89
#floor area of greenhouse cultivation area(m**2)
greenhouseCultivationFloorArea = greenhouseCultivationFloorWidth * greenhouseCultivationFloorDepth
# greenhouseCultivationFloorArea = greenhouseWidth * greenhouseDepth * 0.9
print("greenhouseCultivationFloorArea[m^2]:{}".format(greenhouseCultivationFloorArea))
# number of spans. If this is 1, the greenhouse is a single span greenhouse. If >1, multi-span greenhouse
numOfSpans = 10.0
# the type of roof direction
roofDirectionNotation = "EastWestDirectionRoof"
#side wall height of greenhouse (m)
greenhouseHeightSideWall = 1.8288 # = 6[feet]
#center height of greenhouse (m)
greenhouseHeightRoofTop = 4.8768 # = 16[feet]
#width of the rooftop. calculate from the Pythagorean theorem. assumed that the shape of rooftop is straight (not curved), and the top height and roof angels are same at each span.
greenhouseRoofWidth = math.sqrt((greenhouseWidth/(numOfSpans*2.0))**2.0 + (greenhouseHeightRoofTop-greenhouseHeightSideWall)**2.0)
print ("greenhouseRoofWidth [m]: {}".format(greenhouseRoofWidth))
# the length of the roof facing east or north
greenhouseRoofWidthEastOrNorth = greenhouseRoofWidth
# the length of the roof facing west or south
greenhouseRoofWidthWestOrSouth = greenhouseRoofWidth

#angle of the rooftop (theta θ). [rad]
greenhouseRoofAngle = math.acos(((greenhouseWidth/(numOfSpans*2.0)) / greenhouseRoofWidth))
print ("greenhouseRoofAngle (rad) : {}".format(greenhouseRoofAngle))
# the angle of the roof facing north or east [rad]
roofAngleEastOrNorth = greenhouseRoofAngle
# the angle of the roof facing south or west [rad]. This should be modified if the roof angle is different from the other side.
roofAngleWestOrSouth = greenhouseRoofAngle
# area of the rooftop [m^2]. summing the left and right side of rooftops from the center.
greenhouseTotalRoofArea = greenhouseRoofWidth * greenhouseDepth * numOfSpans * 2.0
print ("greenhouseRoofArea[m^2]: {}".format(greenhouseTotalRoofArea))
#########################################################

#the proportion of shade made by the structure, actuator (e.g. sensors and fog cooling systems) and farming equipments (e.g. gutters) (-)
GreenhouseShadeProportion = 0.1
# GreenhouseShadeProportion = 0.05

# DLI [mol m^-2 day^-1]
DLIForButterHeadLettuceWithNoTipburn = 17.0
# PPFD [umol m^-2 s^-1]
# the PPFD was divided by 2.0 because it was assumed that the time during the day was the half of a day (12 hours)
# OptimumPPFDForButterHeadLettuceWithNoTipburn = DLIForButterHeadLettuceWithNoTipburn * 1000000.0 / float(secondperMinute*minuteperHour*hourperDay)
OptimumPPFDForButterHeadLettuceWithNoTipburn = DLIForButterHeadLettuceWithNoTipburn * 1000000.0 / float(secondperMinute*minuteperHour*hourperDay/2.0)
print("OptimumPPFDForButterHeadLettuceWithNoTipburn (PPFD):{}".format(OptimumPPFDForButterHeadLettuceWithNoTipburn))

# 1.5 is an arbitrary number
# the amount of PPFD to deploy shading curtain
shadingCurtainDeployPPFD = OptimumPPFDForButterHeadLettuceWithNoTipburn * 1.5
print("shadingCurtainDeployPPFD:{}".format(shadingCurtainDeployPPFD))
#######################################################
##########Specification of the greenhouse end##########
#######################################################

##################################################################
##########specification of glazing (covering film) start##########
##################################################################
greenhouseGlazingType = "polyethylene (PE) DoubleLayer"

#ratio of visible light (400nm - 750nm) through a glazing material (-)
#source: Nadia Sabeh, "TOMATO GREENHOUSE ROADMAP" https://www.amazon.com/Tomato-Greenhouse-Roadmap-Guide-Production-ebook/dp/B00O4CPO42
# singlePEPERTransmittance = 0.875
singlePERTransmittance = 0.85
dobulePERTransmittance = singlePERTransmittance ** 2.0

# reference: https://www.filmetrics.com/refractive-index-database/Polyethylene/PE-Polyethene
PEFilmRefractiveIndex = 1.5
# reference: https://en.wikipedia.org/wiki/Refractive_index
AirRefractiveIndex = 1.000293



################################################################
##########specification of glazing (covering film) end##########
################################################################

#####################################################################
##########specification of OPV module (film or panel) start##########
#####################################################################

# [rad]. tilt of OPV module = tilt of the greenhouse roof
# OPVAngle = math.radians(0.0)
OPVAngle = greenhouseRoofAngle

# the coverage ratio of OPV module on the greenhouse roof [-]
OPVAreaCoverageRatio = 0.25
# OPVAreaCoverageRatio = 0.0

# the coverage ratio of OPV module on the greenhouse roof [-]. If you set this value same as OPVAreaCoverageRatio, it assumed that the OPV coverage ratio does not change during the whole period
# OPVAreaCoverageRatioFallowPeriod = 1.0
OPVAreaCoverageRatioFallowPeriod = 0.5
# OPVAreaCoverageRatioFallowPeriod = 0.25
# OPVAreaCoverageRatioFallowPeriod = 0.0


#the area of OPV on the roofTop.
OPVArea = OPVAreaCoverageRatio * greenhouseTotalRoofArea
#print "OPVArea:{}".format(OPVArea)

#the ratio of degradation per day (/day)
#TODO: search the function later
OPVdegradationRatio = 0.001

#conversion efficiency from ligtht energy to electricity
#The efficiency of solar panels is based on standard testing conditions (STC),
#under which all solar panel manufacturers must test their modules. STC specifies a temperature of 25°C (77 F),
#solar irradiance of 1000 W/m2 and an air mass 1.5 (AM1.5) spectrums.
#The STC efficiency of a 240-watt module measuring 1.65 square meters is calculated as follows:
#240 watts ÷ (1.65m2 (module area) x 1000 W/m2) = 14.54%.
#source: http://www.solartown.com/learning/solar-panels/solar-panel-efficiency-have-you-checked-your-eta-lately/
OPVEfficiencyRatioSTC = 0.033
#what is an air mass??
#エアマスとは太陽光の分光放射分布を表すパラメーター、標準状態の大気（標準気圧１０１３ｈＰａ）に垂直に入射（太陽高度角９０°）した
# 太陽直達光が通過する路程の長さをＡＭ１．０として、それに対する比で表わされます。
#source: http://www.solartech.jp/module_char/standard.html

# the coefficient converting the ideal (given by manufacturers) cell efficiency to the real efficiency under actual conditions
degradeCoefficientFromIdealtoReal = 0.85


#unit[/K]. The proportion of a change of voltage which the OPV film generates under STC condition (25°C),
# mentioned in # Table 1-2-1
TempCoeffitientVmpp =  -0.0019

#unit[/K]. The proportion of a change of current which the OPV film generates under STC condition (25°C),
# mentioned in Table 1-2-1
TempCoeffitientImpp =  0.0008

#unit[/K]. The proportion of a change of power which the OPV film generates under STC condition (25°C),
# mentioned in Table 1-2-

TempCoeffitientPmpp =  0.0002

#transmission ratio of VISIBLE sunlight through OPV film.
#TODO measure later
#OPVPARTransmittance = 0.6
OPVPARTransmittance = 0.3

#source: http://energy.gov/sites/prod/files/2014/01/f7/pvmrw13_ps5_3m_nachtigal.pdf (3M Ultra-Barrier Solar Film spec.pdf)

#the price of OPV per area [EUR/m^2]
# [EUR]
originalOPVPriceEUR = 13305.6
OPVPriceEUR = 13305.6
# [m^2]
OPVSizePurchased = 6.0 * 0.925 * 10.0

# [EUR/m^2]
OPVPriceperAreaEUR = OPVPriceEUR / OPVSizePurchased

#as of 11Nov/2016 [USD/EUR]
CurrencyConversionRatioUSDEUR= 1/1.0850
#the price of OPV per area [USD/m^2]
OPVPricePerAreaUSD = OPVPriceperAreaEUR*CurrencyConversionRatioUSDEUR
print("OPVPricePerAreaUSD:{}".format(OPVPricePerAreaUSD))


# True == consider the OPV cost, False == ignore the OPV cost
ifConsiderOPVCost = False
# if you set this 730, you assume the purchase cost of is OPV zero because at the simulator class, this number divides the integer number, which gives zero.
OPVDepreciationPeriodDays = 730.0

OPVDepreciationMethod = "StraightLine"

##########specification of OPV module (film or panel) end##########

##########specification of shading curtain start##########
#the transmittance ratio of shading curtain
shadingTransmittanceRatio = 0.45

isShadingCurtainReinforcementLearning = True

#if True, a black net is covered over the roof for shading in summer
# hasShadingCurtain = False
hasShadingCurtain = True

openCurtainString = "openCurtain"
closeCurtainString = "closeCurtain"

ShadingCurtainDeployStartMMSpring = 3
ShadingCurtainDeployStartDDSpring = 16
ShadingCurtainDeployEndMMSpring = 5
ShadingCurtainDeployEndDDSpring = 31

ShadingCurtainDeployStartMMFall =9
ShadingCurtainDeployStartDDFall =16
ShadingCurtainDeployEndMMFall =10
ShadingCurtainDeployEndDDFall =31

# this is gonna be True when you want to deploy shading curtains only from  ShadigCuratinDeployStartHH to ShadigCuratinDeployEndHH
IsShadingCurtainDeployOnlyDayTime = True
ShadigCuratinDeployStartHH = 10
ShadigCuratinDeployEndHH = 14

# this is gonna be true when you want to control shading curtain opening and closing every hour
IsHourlyShadingCurtainDeploy = False

########################################################
##########specification of shading curtain end##########
########################################################


#################################################
##########Specification of plants start##########
#################################################
#unit selling price (USD/kg), which should be the daily retail/wholesale unit price
# original price
plantUnitPriceUSDperKilogram = 0.977861162
# adjusted price
# plantUnitPriceUSDperKilogram = 0.677861162

#Cost of plant production. the unit is USD/m^2
# the conversion rate was calculated from from University of California Cooperative Extension (UCEC) UC Small farm program (http://sfp.ucdavis.edu/crops/coststudieshtml/lettuce/LettuceTable1/)
plantProductionCostperSquareMeterPerYear = 1.096405

numberOfRidge = 5.0

#unit: m
distanceBetweenPlants = 0.2

#number of heads
numberOFheads = int(greenhouseCultivationFloorDepth/distanceBetweenPlants * numberOfRidge)
print("numberOFheads:{}".format(numberOFheads))

# number of head per cultivation area [heads/m^2]
numberOFheadsPerArea = float(numberOFheads / greenhouseCultivationFloorArea)

#photoperiod (time of lighting in a day). the unit is hour
# TODO: this should be revised so that the photo period is calculated by the sum of PPFD each day or the change of direct solar radiation or the diff of sunse and sunrise
photoperiod = 14.0

#number of cultivation days (days/harvest)
cultivationDaysperHarvest = 35
# cultivationDaysperHarvest = 30

# the constant of each plant growth model
TaylorExpantionWithFluctuatingDLI = "TaylorExpantionWithFluctuatingDLI"
E_J_VanHenten = "E_J_VanHenten"
# plantGrowthModel = "TaylorExpantionWithFluctuatingDLI"
# plantGrowthModel = "AccumulatedDLI"
plantGrowthModel = E_J_VanHenten


DryMassToFreshMass = 1.0/0.045

# [heads/m^2]
numOfHeadsPerArea = 45.0

# operation cost of plants [USD/m^2/year]
plantcostperSquaremeterperYear = 1.096405

# the DLI upper limitation causing some tipburn
DLIforTipBurn = 17.0

# the discount ratio when there are some tipburn observed
tipburnDiscountRatio = 0.2

# make this number 1.0 in the end. change this only for simulation experiment
plantPriceDiscountRatio_justForSimulation = 1.0

# if this is true, then continue to grow plants during the fallow period. the default value is False in the object(instance)
ifGrowForFallowPeriod = False

# fallow period
FallowPeriodStartMM = 6
FallowPeriodStartDD = 1
FallowPeriodEndMM = 9
FallowPeriodEndDD = 15

# if consider the photo inhibition by too strong sunlight, True, if not, False
IfConsiderPhotoInhibition = True


##########Specification of the plants end##########

###########################Global variable end###########################


class CropElectricityYeildSimulatorConstant:
    """
    a constant class.

    """

    ###########the constractor##################
    def __init__(self):
        print ("call CropElectricityYeildSimulatorConstant")

    ###########the constractor end##################

    ###########the methods##################
    def method(self, val):
        print("call CropElectricityYeildSimulatorConstant method")

    ###########the methods end##################
