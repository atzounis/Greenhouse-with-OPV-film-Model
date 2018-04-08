import CropElectricityYeildSimulatorConstant as constant

class SimulatorClass:

  # constructor
  def __init__(self):

    self._OPVAreaCoverageRatio = constant.OPVAreaCoverageRatio
    self._OPVCoverageRatioSummerPeriod = constant.OPVAreaCoverageRatioSummerPeriod
    self._plantGrowthModel = constant.plantGrowthModel
    self._cultivationDaysperHarvest = constant.cultivationDaysperHarvest
    self._hasShadingCurtain = constant.hasShadingCurtain
    self._shadingCurtainDeployPPFD = constant.plantGrowthModel
    self._profitVSOPVCoverageData = None
    self._monthlyElectricitySalesperArea = None
    self._monthlyElectricitySalesperAreaEastRoof = None
    self._monthlyElectricitySalesperAreaWestRoof = None
    self._totalElectricitySalesPerAreaPerMonth = None
    self._totalElectricitySalesPerMonth = None
    self._totalElectricitySales = None
    self._oPVCostUSDForDepreciationPerOPVArea = None
    self._totalOPVCostUSDForDepreciation = None
    self._totalOPVCostUSDForDepreciationPerGHFloorArea = None
    self._electricityProductionProfit = None
    self._electricityProductionProfitPerGHFloorArea = None
    self._hourlyInnerLightIntensityPPFDThroughGlazing = None
    self._hourlyInnerLightIntensityPPFDThroughInnerStructure = None
    self._directPPFDToOPVEastDirection = None
    self._directPPFDToOPVWestDirection = None
    self._diffusePPFDToOPV = None
    self._groundReflectedPPFDToOPV = None
    # self._totalDLItoPlantsBaselineShadingCuratin = None
    self._directDLIToOPVEastDirection = None
    self._directDLIToOPVWestDirection = None
    self._diffuseDLIToOPV = None
    self._groundReflectedDLIToOPV = None
    self._hourlyDirectSolarRadiationAfterMultiSpanRoof = None
    self._hourlyDiffuseSolarRadiationAfterMultiSpanRoof = None
    self._groundReflectedRadiationAfterMultiSpanRoof = None
    self._hourlyDirectPPFDAfterMultiSpanRoof = None
    self._hourlyDiffusePPFDAfterMultiSpanRoof = None
    self._groundReflectedPPFDAfterMultiSpanRoof = None
    self._shootFreshMassList = None
    self._unitDailyFreshWeightIncrease = None
    self._accumulatedUnitDailyFreshWeightIncrease = None
    self._unitDailyHarvestedFreshWeight = None
    self._totalPlantSalesperSquareMeter = None
    self._totalPlantSales = None
    self._totalPlantSalesPerGHFloorArea = None
    self._totalLaborCost = None
    self._totalLaborCostPerGHFloorArea = None
    self._totalPlantProductionCost = None
    self._totalPlantProductionCostPerGHFloorArea = None
    self._totalPlantProfit = None
    self._totalPlantProfitPerGHFloorArea = None
    self._economicProfit = None
    self._economicProfitPerGHFloorArea = None
    self._averageDLIonEachCycle = None
    self._year = None
    self._month = None
    self._day = None
    self._hour = None
    self._importedHourlyHorizontalDirectSolarRadiation = None
    self._importedHourlyHorizontalDiffuseSolarRadiation = None
    self._importedHourlyHorizontalTotalBeamMeterBodyTemperature = None
    self._importedHourlyAirTemperature = None
    self._directSolarRadiationToOPVEastDirection = None
    self._directSolarRadiationToOPVWestDirection = None
    self._diffuseSolarRadiationToOPV = None
    self._albedoSolarRadiationToOPV = None
    self._estimatedDirectSolarRadiationToOPVEastDirection = None
    self._estimatedDirectSolarRadiationToOPVWestDirection = None
    self._estimatedDiffuseSolarRadiationToOPV = None
    self._estimatedAlbedoSolarRadiationToOPV = None

    # the following variables do not have got/set methods, but have properties
    self._hourlySolarIncidenceAngleEastDirection = None
    self._hourlySolarIncidenceAngleWestDirection = None
    self._directSolarIrradianceToPlants = None
    self._diffuseSolarIrradianceToPlants = None
    self._directPPFDToPlants = None
    self._diffusePPFDToPlants = None
    self._directDLIToPlants = None
    self._diffuseDLIToPlants = None
    self._totalDLItoPlants = None
    self._hourlyDayOrNightFlag = None
    self._hourlyHorizontalDiffuseOuterSolarIrradiance = None
    self._hourlyHorizontalTotalOuterSolarIrradiance = None
    self._hourlyHorizontalDirectOuterSolarIrradiance = None
    self._hourlyHorizontalTotalBeamMeterBodyTemperature = None
    self._hourlyAirTemperature = None

    self._ifGrowForSummerPeriod = False
    # if you want to calculate the estimated data which does not require the measured data, set this variable True.
    self._estimateSolarRadiationMode = False
    self._ifHasShadingCurtain = None
    self._hourlySolarAltitudeAngle = None
    self._hourlySolarAzimuthAngle = None
    self._hourlyModuleAzimuthAngleEast = None
    self._hourlyModuleAzimuthAngleWest = None
    self._T_matForPerpendicularIrrEastOrNorthFacingRoof = None
    self._T_matForPerpendicularIrrWestOrSouthFacingRoof = None
    self._integratedT_mat = None
    self._directHorizontalSolarRadiation = None
    self._dailyWhopvoutperAreaEastRoof = None
    self._dailyWhopvoutperAreaWestRoof = None

    self._dailyShootFreshMass = None
    self._dailyUnitDailyFreshWeightIncrease = None
    self._dailyAccumulatedUnitDailyFreshWeightIncrease = None
    self._dailyUnitHarvestedFreshWeight = None

  def setOPVAreaCoverageRatio(self, OPVAreaCoverageRatio):
    self._OPVAreaCoverageRatio = OPVAreaCoverageRatio
  def getOPVAreaCoverageRatio(self):
    return self._OPVAreaCoverageRatio

  def setOPVCoverageRatioSummerPeriod(self, OPVCoverageRatioSummerPeriod):
    self._OPVCoverageRatioSummerPeriod = OPVCoverageRatioSummerPeriod
  def getOPVCoverageRatioSummerPeriod(self):
    return self._OPVCoverageRatioSummerPeriod

  def setPlantGrowthModel(self, plantGrowthModel):
    self._plantGrowthModel = plantGrowthModel
  def getPlantGrowthModel(self):
    return self._plantGrowthModel

  def setCultivationDaysperHarvest(self, cultivationDaysperHarvest):
    self._cultivationDaysperHarvest = cultivationDaysperHarvest
  def getCultivationDaysperHarvest(self):
    return self._cultivationDaysperHarvest

  def setHasShadingCurtain(self, hasShadingCurtain):
    self._hasShadingCurtain = hasShadingCurtain
  def getHasShadingCurtain(self):
    return self.hasShadingCurtain

  def setShadingCurtainDeployPPFD(self, shadingCurtainDeployPPFD):
    self._shadingCurtainDeployPPFD = shadingCurtainDeployPPFD
  def getShadingCurtainDeployPPFD(self):
    return self._shadingCurtainDeployPPFD

  def setProfitVSOPVCoverageData(self,profitVSOPVCoverageData):
    self._profitVSOPVCoverageData = profitVSOPVCoverageData
  def getProfitVSOPVCoverageData(self):
    return self._profitVSOPVCoverageData

  def setMonthlyElectricitySalesperArea(self, monthlyElectricitySalesperArea):
    self._monthlyElectricitySalesperArea = monthlyElectricitySalesperArea
  def getMonthlyElectricitySalesperArea(self):
    return self._monthlyElectricitySalesperArea

  def setMonthlyElectricitySalesperAreaEastRoof(self, monthlyElectricitySalesperAreaEastRoof):
    self._monthlyElectricitySalesperAreaEastRoof = monthlyElectricitySalesperAreaEastRoof
  def getMonthlyElectricitySalesperAreaEastRoof(self):
    return self._monthlyElectricitySalesperAreaEastRoof

  def setMonthlyElectricitySalesperAreaWestRoof(self, monthlyElectricitySalesperAreaWestRoof):
    self._monthlyElectricitySalesperAreaWestRoof = monthlyElectricitySalesperAreaWestRoof

  def getMonthlyElectricitySalesperAreaWestRoof(self):
    return self._monthlyElectricitySalesperAreaWestRoof

  @property
  def totalElectricitySalesPerMonth(self):
    return self._totalElectricitySalesPerMonth
  @totalElectricitySalesPerMonth.setter
  def totalElectricitySalesPerMonth(self, totalElectricitySalesPerMonth):
    self._totalElectricitySalesPerMonth = totalElectricitySalesPerMonth

  @property
  def totalElectricitySalesPerAreaPerMonth(self):
    return self._totalElectricitySalesPerAreaPerMonth
  @totalElectricitySalesPerAreaPerMonth.setter
  def totalElectricitySalesPerAreaPerMonth(self, totalElectricitySalesPerAreaPerMonth):
    self._totalElectricitySalesPerAreaPerMonth = totalElectricitySalesPerAreaPerMonth

  @property
  def totalElectricitySales(self):
    return self._totalElectricitySales
  @totalElectricitySales.setter
  def totalElectricitySales(self, totalElectricitySales):
    self._totalElectricitySales = totalElectricitySales

  def setOPVCostUSDForDepreciationPerOPVArea(self, oPVCostUSDForDepreciationPerOPVArea):
    self._oPVCostUSDForDepreciationPerOPVArea = oPVCostUSDForDepreciationPerOPVArea
  def getOPVCostUSDForDepreciationPerOPVArea(self):
    return self._oPVCostUSDForDepreciationPerOPVArea

  @property
  def totalOPVCostUSDForDepreciation(self):
    return self._totalOPVCostUSDForDepreciation
  @totalOPVCostUSDForDepreciation.setter
  def totalOPVCostUSDForDepreciation(self, totalOPVCostUSDForDepreciation):
    self._totalOPVCostUSDForDepreciation = totalOPVCostUSDForDepreciation

  @property
  def totalOPVCostUSDForDepreciationPerGHFloorArea(self):
    return self._totalOPVCostUSDForDepreciationPerGHFloorArea
  @totalOPVCostUSDForDepreciationPerGHFloorArea.setter
  def totalOPVCostUSDForDepreciationPerGHFloorArea(self, totalOPVCostUSDForDepreciationPerGHFloorArea):
    self._totalOPVCostUSDForDepreciationPerGHFloorArea = totalOPVCostUSDForDepreciationPerGHFloorArea

  @property
  def electricityProductionProfit(self):
    return self._electricityProductionProfit
  @electricityProductionProfit.setter
  def electricityProductionProfit(self, electricityProductionProfit):
    self._electricityProductionProfit = electricityProductionProfit

  @property
  def electricityProductionProfitPerGHFloorArea(self):
    return self._electricityProductionProfitPerGHFloorArea
  @electricityProductionProfitPerGHFloorArea.setter
  def electricityProductionProfitPerGHFloorArea(self, electricityProductionProfitPerGHFloorArea):
    self._electricityProductionProfitPerGHFloorArea = electricityProductionProfitPerGHFloorArea

  ######################## measured solar radiation to OPV start ########################
  def setDirectSolarRadiationToOPVEastDirection(self, directSolarRadiationToOPVEastDirection):
    self._directSolarRadiationToOPVEastDirection = directSolarRadiationToOPVEastDirection

  def getDirectSolarRadiationToOPVEastDirection(self):
    return self._directSolarRadiationToOPVEastDirection

  def setDirectSolarRadiationToOPVWestDirection(self, directSolarRadiationToOPVWestDirection):
    self._directSolarRadiationToOPVWestDirection = directSolarRadiationToOPVWestDirection

  def getDirectSolarRadiationToOPVWestDirection(self):
    return self._directSolarRadiationToOPVWestDirection

  def setDiffuseSolarRadiationToOPV(self, diffuseSolarRadiationToOPV):
    self._diffuseSolarRadiationToOPV = diffuseSolarRadiationToOPV

  def getDiffuseSolarRadiationToOPV(self):
    return self._diffuseSolarRadiationToOPV

  def setAlbedoSolarRadiationToOPV(self, albedoSolarRadiationToOPV):
    self._albedoSolarRadiationToOPV = albedoSolarRadiationToOPV

  def getAlbedoSolarRadiationToOPV(self):
    return self._albedoSolarRadiationToOPV
  ######################## measured solar radiation to OPV end ########################

  ######################## estimated solar radiation to OPV start ########################
  def setEstimatedDirectSolarRadiationToOPVEastDirection(self, estimatedDirectSolarRadiationToOPVEastDirection):
    self._estimatedDirectSolarRadiationToOPVEastDirection = estimatedDirectSolarRadiationToOPVEastDirection

  def getEstimatedDirectSolarRadiationToOPVEastDirection(self):
    return self._estimatedDirectSolarRadiationToOPVEastDirection

  def setEstimatedDirectSolarRadiationToOPVWestDirection(self, estimatedDirectSolarRadiationToOPVWestDirection):
    self._estimatedDirectSolarRadiationToOPVWestDirection = estimatedDirectSolarRadiationToOPVWestDirection

  def getEstimatedDirectSolarRadiationToOPVWestDirection(self):
    return self._estimatedDirectSolarRadiationToOPVWestDirection

  def setEstimatedDiffuseSolarRadiationToOPV(self, estimatedDiffuseSolarRadiationToOPV):
    self._albedoSolarRadiationToOPV = estimatedDiffuseSolarRadiationToOPV

  def getEstimatedDiffuseSolarRadiationToOPV(self):
    return self._estimatedDiffuseSolarRadiationToOPV

  def setEstimatedAlbedoSolarRadiationToOPV(self, estimatedAlbedoSolarRadiationToOPV):
    self._estimatedAlbedoSolarRadiationToOPV = estimatedAlbedoSolarRadiationToOPV

  def getEstimatedAlbedoSolarRadiationToOPV(self):
    return self._estimatedAlbedoSolarRadiationToOPV
  ######################## estimated solar radiation to OPV end ########################



  def setHourlyInnerLightIntensityPPFDThroughGlazing(self, hourlyInnerLightIntensityPPFDThroughGlazing):
    self._hourlyInnerLightIntensityPPFDThroughGlazing = hourlyInnerLightIntensityPPFDThroughGlazing
  def getHourlyInnerLightIntensityPPFDThroughGlazing(self):
    return self._hourlyInnerLightIntensityPPFDThroughGlazing

  def setHourlyInnerLightIntensityPPFDThroughInnerStructure(self, hourlyInnerLightIntensityPPFDThroughInnerStructure):
    self._hourlyInnerLightIntensityPPFDThroughInnerStructure = hourlyInnerLightIntensityPPFDThroughInnerStructure
  def getHourlyInnerLightIntensityPPFDThroughInnerStructure(self):
    return self._hourlyInnerLightIntensityPPFDThroughInnerStructure

  def setDirectPPFDToOPVEastDirection(self, directPPFDToOPVEastDirection):
    self._directPPFDToOPVEastDirection = directPPFDToOPVEastDirection
  def getDirectPPFDToOPVEastDirection(self):
    return self._directPPFDToOPVEastDirection

  def setDirectPPFDToOPVWestDirection(self, directPPFDToOPVWestDirection):
    self._directPPFDToOPVWestDirection = directPPFDToOPVWestDirection
  def getDirectPPFDToOPVWestDirection(self):
    return self._directPPFDToOPVWestDirection

  def setDiffusePPFDToOPV(self, diffusePPFDToOPV):
    self._diffusePPFDToOPV = diffusePPFDToOPV
  def getDiffusePPFDToOPV(self):
    return self._diffusePPFDToOPV

  def setGroundReflectedPPFDToOPV(self, groundReflectedPPFDToOPV):
    self._groundReflectedPPFDToOPV = groundReflectedPPFDToOPV
  def getGroundReflectedPPFDToOPV(self):
    return self._groundReflectedPPFDToOPV

  # def setTotalDLItoPlantsBaselineShadingCuratin(self, totalDLItoPlantsBaselineShadingCuratin):
  #   self._totalDLItoPlantsBaselineShadingCuratin = totalDLItoPlantsBaselineShadingCuratin
  # def getTotalDLItoPlantsBaselineShadingCuratin(self):
  #   return self._totalDLItoPlantsBaselineShadingCuratin

  def setDirectDLIToOPVEastDirection(self, directDLIToOPVEastDirection):
    self._directDLIToOPVEastDirection = directDLIToOPVEastDirection
  def getDirectDLIToOPVEastDirection(self):
    return self._directDLIToOPVEastDirection

  def setDirectDLIToOPVWestDirection(self, directDLIToOPVWestDirection):
    self._directDLIToOPVWestDirection = directDLIToOPVWestDirection
  def getDirectDLIToOPVWestDirection(self):
    return self._directDLIToOPVWestDirection

  def setDiffuseDLIToOPV(self, diffuseDLIToOPV):
    self._diffuseDLIToOPV = diffuseDLIToOPV
  def getDiffuseDLIToOPV(self):
    return self._diffuseDLIToOPV

  def setGroundReflectedDLIToOPV(self, groundReflectedDLIToOPV):
    self._groundReflectedDLIToOPV = groundReflectedDLIToOPV
  def getGroundReflectedDLIToOPV(self):
    return self._groundReflectedDLIToOPV


  ##############################solar irradiance to multi span roof start##############################
  def setHourlyDirectSolarRadiationAfterMultiSpanRoof(self, hourlyDirectSolarRadiationAfterMultiSpanRoof):
    self._hourlyDirectSolarRadiationAfterMultiSpanRoof = hourlyDirectSolarRadiationAfterMultiSpanRoof
  def getHourlyDirectSolarRadiationAfterMultiSpanRoof(self):
    return self._hourlyDirectSolarRadiationAfterMultiSpanRoof

  def setHourlyDiffuseSolarRadiationAfterMultiSpanRoof(self, hourlyDiffuseSolarRadiationAfterMultiSpanRoof):
    self._hourlyDiffuseSolarRadiationAfterMultiSpanRoof = hourlyDiffuseSolarRadiationAfterMultiSpanRoof
  def getHourlyDiffuseSolarRadiationAfterMultiSpanRoof(self):
    return self._hourlyDiffuseSolarRadiationAfterMultiSpanRoof

  def setGroundReflectedRadiationAfterMultiSpanRoof(self, groundReflectedRadiationAfterMultiSpanRoof):
    self._groundReflectedRadiationAfterMultiSpanRoof = groundReflectedRadiationAfterMultiSpanRoof
  def getGroundReflectedRadiationAfterMultiSpanRoof(self):
    return self._groundReflectedRadiationAfterMultiSpanRoof

  def setHourlyDirectPPFDAfterMultiSpanRoof(self, hourlyDirectPPFDAfterMultiSpanRoof):
    self._hourlyDirectPPFDAfterMultiSpanRoof = hourlyDirectPPFDAfterMultiSpanRoof
  def getHourlyDirectPPFDAfterMultiSpanRoof(self):
    return self._hourlyDirectPPFDAfterMultiSpanRoof

  def setHourlyDiffusePPFDAfterMultiSpanRoof(self, hourlyDiffusePPFDAfterMultiSpanRoof):
    self._hourlyDiffusePPFDAfterMultiSpanRoof = hourlyDiffusePPFDAfterMultiSpanRoof
  def getHourlyDiffusePPFDAfterMultiSpanRoof(self):
    return self._hourlyDiffusePPFDAfterMultiSpanRoof

  def setGroundReflectedPPFDAfterMultiSpanRoof(self, groundReflectedPPFDAfterMultiSpanRoof):
    self._groundReflectedPPFDAfterMultiSpanRoof = groundReflectedPPFDAfterMultiSpanRoof
  def getGroundReflectedPPFDAfterMultiSpanRoof(self):
    return self._groundReflectedPPFDAfterMultiSpanRoof
  ##############################solar irradiance to multi span roof end##############################

  def setShootFreshMassList(self, shootFreshMassList):
    self._shootFreshMassList = shootFreshMassList
  def getShootFreshMassList(self):
    return self._shootFreshMassList

  def setUnitDailyFreshWeightIncrease(self, setUnitDailyFreshWeightIncrease):
    self._unitDailyFreshWeightIncrease = setUnitDailyFreshWeightIncrease
  def getUnitDailyFreshWeightIncrease(self):
    return self._unitDailyFreshWeightIncrease

  def setAccumulatedUnitDailyFreshWeightIncrease(self, accumulatedUnitDailyFreshWeightIncrease):
    self._accumulatedUnitDailyFreshWeightIncrease = accumulatedUnitDailyFreshWeightIncrease
  def getAccumulatedUnitDailyFreshWeightIncrease(self):
    return self._accumulatedUnitDailyFreshWeightIncrease

  def setUnitDailyHarvestedFreshWeight(self, unitDailyHarvestedFreshWeight):
    self._unitDailyHarvestedFreshWeight = unitDailyHarvestedFreshWeight
  def getUnitDailyHarvestedFreshWeight(self):
    return self._unitDailyHarvestedFreshWeight

  @property
  def totalPlantSales(self):
    return self._totalPlantSales
  @totalPlantSales.setter
  def totalPlantSales(self, totalPlantSales):
    self._totalPlantSales = totalPlantSales

  @property
  def totalPlantSalesperSquareMeter(self):
    return self._totalPlantSalesperSquareMeter
  @totalPlantSalesperSquareMeter.setter
  def totalPlantSalesperSquareMeter(self, totalPlantSalesperSquareMeter):
    self._totalPlantSalesperSquareMeter = totalPlantSalesperSquareMeter

  @property
  def totalPlantSalesPerGHFloorArea(self):
    return self._totalPlantSalesPerGHFloorArea
  @totalPlantSalesPerGHFloorArea.setter
  def totalPlantSalesPerGHFloorArea(self, totalPlantSalesPerGHFloorArea):
    self._totalPlantSalesPerGHFloorArea = totalPlantSalesPerGHFloorArea


  @property
  def totalLaborCost(self):
    return self._totalLaborCost
  @totalLaborCost.setter
  def totalLaborCost(self, totalLaborCost):
    self._totalLaborCost = totalLaborCost

  @property
  def totalLaborCostPerGHFloorArea(self):
    return self._totalLaborCostPerGHFloorArea
  @totalLaborCostPerGHFloorArea.setter
  def totalLaborCostPerGHFloorArea(self, totalLaborCostPerGHFloorArea):
    self._totalLaborCostPerGHFloorArea = totalLaborCostPerGHFloorArea

  @property
  def totalPlantProductionCost(self):
    return self._totalPlantProductionCost
  @totalPlantProductionCost.setter
  def totalPlantProductionCost(self, totalPlantProductionCost):
    self._totalPlantProductionCost = totalPlantProductionCost

  @property
  def totalPlantProductionCostPerGHFloorArea(self):
    return self._totalPlantProductionCostPerGHFloorArea
  @totalPlantProductionCostPerGHFloorArea.setter
  def totalPlantProductionCostPerGHFloorArea(self, totalPlantProductionCostPerGHFloorArea):
    self._totalPlantProductionCostPerGHFloorArea = totalPlantProductionCostPerGHFloorArea

  @property
  def totalPlantProfit(self):
    return self._totalPlantProfit
  @totalPlantProfit.setter
  def totalPlantProfit(self, totalPlantProfit):
    self._totalPlantProfit = totalPlantProfit

  @property
  def totalPlantProfitPerGHFloorArea(self):
    return self._totalPlantProfitPerGHFloorArea
  @totalPlantProfitPerGHFloorArea.setter
  def totalPlantProfitPerGHFloorArea(self, totalPlantProfitPerGHFloorArea):
    self._totalPlantProfitPerGHFloorArea = totalPlantProfitPerGHFloorArea

  @property
  def economicProfit(self):
    return self._economicProfit
  @economicProfit.setter
  def economicProfit(self, economicProfit):
    self._economicProfit = economicProfit

  @property
  def economicProfitPerGHFloorArea(self):
    return self._economicProfitPerGHFloorArea
  @economicProfitPerGHFloorArea.setter
  def economicProfitPerGHFloorArea(self, economicProfitPerGHFloorArea):
    self._economicProfitPerGHFloorArea = economicProfitPerGHFloorArea

  def setAverageDLIonEachCycle(self, averageDLIonEachCycle):
    self._averageDLIonEachCycle = averageDLIonEachCycle
  def getAverageDLIonEachCycle(self):
    return self._averageDLIonEachCycle

  def setYear(self, year):
    self._year = year
  def getYear(self):
    return self._year

  def setMonth(self, month):
    self._month = month
  def getMonth(self):
    return self._month

  def setDay(self, day):
    self._day = day
  def getDay(self):
    return self._day

  def setHour(self, hour):
    self._hour = hour
  def getHour(self):
    return self._hour

  ######################### imported data start #########################
  def setImportedHourlyHorizontalDirectSolarRadiation(self, importedHourlyHorizontalDirectSolarRadiation):
    self._importedHourlyHorizontalDirectSolarRadiation = importedHourlyHorizontalDirectSolarRadiation
  def getImportedHourlyHorizontalDirectSolarRadiation(self):
    return self._importedHourlyHorizontalDirectSolarRadiation

  def setImportedHourlyHorizontalDiffuseSolarRadiation(self, importedHourlyHorizontalDiffuseSolarRadiation):
    self._importedHourlyHorizontalDiffuseSolarRadiation = importedHourlyHorizontalDiffuseSolarRadiation
  def getImportedHourlyHorizontalDiffuseSolarRadiation(self):
    return self._importedHourlyHorizontalDiffuseSolarRadiation

  def setImportedHourlyHorizontalTotalBeamMeterBodyTemperature(self, importedHourlyHorizontalTotalBeamMeterBodyTemperature):
    self._importedHourlyHorizontalTotalBeamMeterBodyTemperature = importedHourlyHorizontalTotalBeamMeterBodyTemperature
  def getImportedHourlyHorizontalTotalBeamMeterBodyTemperature(self):
    return self._importedHourlyHorizontalTotalBeamMeterBodyTemperature

  def setImportedHourlyAirTemperature(self, importedHourlyAirTemperature):
    self._importedHourlyAirTemperature = importedHourlyAirTemperature
  def getImportedHourlyAirTemperature(self):
    return self._importedHourlyAirTemperature
  ######################### imported data end #########################


  ######################### solar radiation to tilted OPV (roof) start #########################
  @property
  def dailyWhopvoutperAreaEastRoof(self):
    return self._dailyWhopvoutperAreaEastRoof
  @dailyWhopvoutperAreaEastRoof.setter
  def dailyWhopvoutperAreaEastRoof(self, dailyWhopvoutperAreaEastRoof):
    self._dailyWhopvoutperAreaEastRoof = dailyWhopvoutperAreaEastRoof

  @property
  def dailyWhopvoutperAreaWestRoof(self):
    return self._dailyWhopvoutperAreaWestRoof
  @dailyWhopvoutperAreaWestRoof.setter
  def dailyWhopvoutperAreaWestRoof(self, dailyWhopvoutperAreaWestRoof):
    self._dailyWhopvoutperAreaWestRoof = dailyWhopvoutperAreaWestRoof

  @property
  def dailykWhopvoutperAreaEastRoof(self):
    return self._dailykWhopvoutperAreaEastRoof
  @dailykWhopvoutperAreaEastRoof.setter
  def dailykWhopvoutperAreaEastRoof(self, dailykWhopvoutperAreaEastRoof):
    self._dailykWhopvoutperAreaEastRoof = dailykWhopvoutperAreaEastRoof

  @property
  def dailykWhopvoutperAreaWestRoof(self):
    return self._dailykWhopvoutperAreaWestRoof
  @dailykWhopvoutperAreaWestRoof.setter
  def dailykWhopvoutperAreaWestRoof(self, dailykWhopvoutperAreaWestRoof):
    self._dailykWhopvoutperAreaWestRoof = dailykWhopvoutperAreaWestRoof

  @property
  def totalkWhopvoutPerday(self):
    return self._totalkWhopvoutPerday
  @totalkWhopvoutPerday.setter
  def totalkWhopvoutPerday(self, totalkWhopvoutPerday):
    self._totalkWhopvoutPerday = totalkWhopvoutPerday

  @property
  def totalkWhopvoutPerMeterPerday(self):
    return self._totalkWhopvoutPerMeterPerday
  @totalkWhopvoutPerMeterPerday.setter
  def totalkWhopvoutPerMeterPerday(self, totalkWhopvoutPerMeterPerday):
    self._totalkWhopvoutPerMeterPerday = totalkWhopvoutPerMeterPerday
  ######################### solar radiation to tilted OPV (roof) end #########################

  def setIfGrowForSummerPeriod(self, ifGrowForSummerPeriod):
    self._ifGrowForSummerPeriod = ifGrowForSummerPeriod
  def getIfGrowForSummerPeriod(self):
    return self._ifGrowForSummerPeriod

  def setEstimateSolarRadiationMode(self, estimateSolarRadiationMode):
    self._estimateSolarRadiationMode = estimateSolarRadiationMode

  def getEstimateSolarRadiationMode(self):
    return self._estimateSolarRadiationMode

  def setIfHasShadingCurtain(self, ifHasShadingCurtain):
    self._ifHasShadingCurtain = ifHasShadingCurtain

  def getIfHasShadingCurtain(self):
    return self._ifHasShadingCurtain

    ############################################ angles start################
  @property
  def hourlySolarIncidenceAngleEastDirection(self):
    return self._hourlySolarIncidenceAngleEastDirection
  @hourlySolarIncidenceAngleEastDirection.setter
  def hourlySolarIncidenceAngleEastDirection(self, hourlySolarIncidenceAngleEastDirection):
    self._hourlySolarIncidenceAngleEastDirection = hourlySolarIncidenceAngleEastDirection

  @property
  def hourlySolarIncidenceAngleWestDirection(self):
    return self._hourlySolarIncidenceAngleWestDirection
  @hourlySolarIncidenceAngleWestDirection.setter
  def hourlySolarIncidenceAngleWestDirection(self, hourlySolarIncidenceAngleWestDirection):
    self._hourlySolarIncidenceAngleWestDirection = hourlySolarIncidenceAngleWestDirection

  @property
  def hourlySolarAltitudeAngle(self):
    return self._hourlySolarAltitudeAngle

  @hourlySolarAltitudeAngle.setter
  def hourlySolarAltitudeAngle(self, hourlySolarAltitudeAngle):
    self._hourlySolarAltitudeAngle = hourlySolarAltitudeAngle


  @property
  def hourlySolarAzimuthAngle(self):
    return self._hourlySolarAzimuthAngle

  @hourlySolarAzimuthAngle.setter
  def hourlySolarAzimuthAngle(self, hourlySolarAzimuthAngle):
    self._hourlySolarAzimuthAngle = hourlySolarAzimuthAngle


  @property
  def hourlyModuleAzimuthAngleEast(self):
    return self._hourlyModuleAzimuthAngleEast

  @hourlyModuleAzimuthAngleEast.setter
  def hourlyModuleAzimuthAngleEast(self, hourlyModuleAzimuthAngleEast):
    self._hourlyModuleAzimuthAngleEast = hourlyModuleAzimuthAngleEast


  @property
  def hourlyModuleAzimuthAngleWest(self):
    return self._hourlyModuleAzimuthAngleWest

  @hourlyModuleAzimuthAngleWest.setter
  def hourlyModuleAzimuthAngleWest(self, hourlyModuleAzimuthAngleWest):
    self._hourlyModuleAzimuthAngleWest = hourlyModuleAzimuthAngleWest
    ############################################ angles end################

  ##############################solar irradiance to plants start##############################
  @property
  def directSolarIrradianceToPlants(self):
      return self._directSolarIrradianceToPlants
  @directSolarIrradianceToPlants.setter
  def directSolarIrradianceToPlants(self, directSolarIrradianceToPlants):
      self._directSolarIrradianceToPlants = directSolarIrradianceToPlants

  @property
  def diffuseSolarIrradianceToPlants(self):
    return self._diffuseSolarIrradianceToPlants
  @diffuseSolarIrradianceToPlants.setter
  def diffuseSolarIrradianceToPlants(self, diffuseSolarIrradianceToPlants):
    self._diffuseSolarIrradianceToPlants = diffuseSolarIrradianceToPlants

  @property
  def directPPFDToPlants(self):
    return self._directPPFDToPlants
  @directPPFDToPlants.setter
  def directPPFDToPlants(self, directPPFDToPlants):
    self._directPPFDToPlants = directPPFDToPlants

  @property
  def diffusePPFDToPlants(self):
    return self._diffusePPFDToPlants
  @diffusePPFDToPlants.setter
  def diffusePPFDToPlants(self, diffusePPFDToPlants):
    self._diffusePPFDToPlants = diffusePPFDToPlants

  @property
  def directDLIToPlants(self):
    return self._directDLIToPlants
  @directDLIToPlants.setter
  def directDLIToPlants(self, directDLIToPlants):
    self._directDLIToPlants = directDLIToPlants

  @property
  def diffuseDLIToPlants(self):
    return self._diffuseDLIToPlants
  @diffuseDLIToPlants.setter
  def diffuseDLIToPlants(self, diffuseDLIToPlants):
    self._diffuseDLIToPlants = diffuseDLIToPlants

  @property
  def totalDLItoPlants(self):
    return self._totalDLItoPlants
  @totalDLItoPlants.setter
  def totalDLItoPlants(self, totalDLItoPlants):
    self._totalDLItoPlants = totalDLItoPlants

  ##############################solar irradiance to plants end##############################

  @property
  def hourlyDayOrNightFlag(self):
    return self._hourlyDayOrNightFlag
  @hourlyDayOrNightFlag.setter
  def hourlyDayOrNightFlag(self, hourlyDayOrNightFlag):
    self._hourlyDayOrNightFlag = hourlyDayOrNightFlag

  ##############################imported data start##############################
  @property
  def hourlyHorizontalDirectOuterSolarIrradiance(self):
    return self._hourlyHorizontalDirectOuterSolarIrradiance
  @hourlyHorizontalDirectOuterSolarIrradiance.setter
  def hourlyHorizontalDirectOuterSolarIrradiance(self, hourlyHorizontalDirectOuterSolarIrradiance):
    self._hourlyHorizontalDirectOuterSolarIrradiance = hourlyHorizontalDirectOuterSolarIrradiance

  @property
  def hourlyHorizontalDiffuseOuterSolarIrradiance(self):
    return self._hourlyHorizontalDiffuseOuterSolarIrradiance
  @hourlyHorizontalDiffuseOuterSolarIrradiance.setter
  def hourlyHorizontalDiffuseOuterSolarIrradiance(self, hourlyHorizontalDiffuseOuterSolarIrradiance):
    self._hourlyHorizontalDiffuseOuterSolarIrradiance = hourlyHorizontalDiffuseOuterSolarIrradiance

  @property
  def hourlyHorizontalTotalOuterSolarIrradiance(self):
    return self._hourlyHorizontalTotalOuterSolarIrradiance
  @hourlyHorizontalTotalOuterSolarIrradiance.setter
  def hourlyHorizontalTotalOuterSolarIrradiance(self, hourlyHorizontalTotalOuterSolarIrradiance):
    self._hourlyHorizontalTotalOuterSolarIrradiance = hourlyHorizontalTotalOuterSolarIrradiance

  @property
  def hourlyHorizontalTotalBeamMeterBodyTemperature(self):
    return self._hourlyHorizontalTotalBeamMeterBodyTemperature
  @hourlyHorizontalTotalBeamMeterBodyTemperature.setter
  def hourlyHorizontalTotalBeamMeterBodyTemperature(self, hourlyHorizontalTotalBeamMeterBodyTemperature):
    self._hourlyHorizontalTotalBeamMeterBodyTemperature = hourlyHorizontalTotalBeamMeterBodyTemperature

  @property
  def hourlyAirTemperature(self):
    return self._hourlyAirTemperature
  @hourlyAirTemperature.setter
  def hourlyAirTemperature(self, hourlyAirTemperature):
    self._hourlyAirTemperature = hourlyAirTemperature
  ##############################imported data end##############################

  ##############################multispan roof transmittance start##############################
  @property
  def T_matForPerpendicularIrrEastOrNorthFacingRoof(self):
    return self._T_matForPerpendicularIrrEastOrNorthFacingRoof
  @T_matForPerpendicularIrrEastOrNorthFacingRoof.setter
  def T_matForPerpendicularIrrEastOrNorthFacingRoof(self, T_matForPerpendicularIrrEastOrNorthFacingRoof):
    self._T_matForPerpendicularIrrEastOrNorthFacingRoof = T_matForPerpendicularIrrEastOrNorthFacingRoof

  @property
  def T_matForPerpendicularIrrWestOrSouthFacingRoof(self):
    return self._T_matForPerpendicularIrrWestOrSouthFacingRoof
  @T_matForPerpendicularIrrWestOrSouthFacingRoof.setter
  def T_matForPerpendicularIrrWestOrSouthFacingRoof(self, T_matForPerpendicularIrrWestOrSouthFacingRoof):
    self._T_matForPerpendicularIrrWestOrSouthFacingRoof = T_matForPerpendicularIrrWestOrSouthFacingRoof

  @property
  def integratedT_mat(self):
    return self._integratedT_mat
  @integratedT_mat.setter
  def integratedT_mat(self, integratedT_mat):
    self._integratedT_mat = integratedT_mat
  ##############################multispan roof transmittance end##############################

  @property
  def directHorizontalSolarRadiation(self):
    return self._directHorizontalSolarRadiation
  @directHorizontalSolarRadiation.setter
  def directHorizontalSolarRadiation(self, directHorizontalSolarRadiation):
    self._directHorizontalSolarRadiation = directHorizontalSolarRadiation

  ##############################plant weights (growth)start ##############################
  @property
  def dailyShootFreshMass(self):
    return self._dailyShootFreshMass
  @dailyShootFreshMass.setter
  def dailyShootFreshMass(self, dailyShootFreshMass):
    self._dailyShootFreshMass = dailyShootFreshMass

  @property
  def dailyUnitDailyFreshWeightIncrease(self):
    return self._dailyUnitDailyFreshWeightIncrease
  @dailyUnitDailyFreshWeightIncrease.setter
  def dailyUnitDailyFreshWeightIncrease(self, dailyUnitDailyFreshWeightIncrease):
    self._dailyUnitDailyFreshWeightIncrease = dailyUnitDailyFreshWeightIncrease

  @property
  def dailyAccumulatedUnitDailyFreshWeightIncrease(self):
    return self._dailyAccumulatedUnitDailyFreshWeightIncrease
  @dailyAccumulatedUnitDailyFreshWeightIncrease.setter
  def dailyAccumulatedUnitDailyFreshWeightIncrease(self, dailyAccumulatedUnitDailyFreshWeightIncrease):
    self._dailyAccumulatedUnitDailyFreshWeightIncrease = dailyAccumulatedUnitDailyFreshWeightIncrease

  @property
  def dailyUnitHarvestedFreshWeight(self):
    return self._dailyUnitHarvestedFreshWeight
  @dailyUnitHarvestedFreshWeight.setter
  def dailyUnitHarvestedFreshWeight(self, dailyUnitHarvestedFreshWeight):
    self._dailyUnitHarvestedFreshWeight = dailyUnitHarvestedFreshWeight

  @property
  def shootFreshMassPerAreaKgPerDay(self):
    return self._shootFreshMassPerAreaKgPerDay
  @shootFreshMassPerAreaKgPerDay.setter
  def shootFreshMassPerAreaKgPerDay(self, shootFreshMassPerAreaKgPerDay):
    self._shootFreshMassPerAreaKgPerDay = shootFreshMassPerAreaKgPerDay

  @property
  def harvestedShootFreshMassPerAreaKgPerDay(self):
    return self._harvestedShootFreshMassPerAreaKgPerDay
  @harvestedShootFreshMassPerAreaKgPerDay.setter
  def harvestedShootFreshMassPerAreaKgPerDay(self, harvestedShootFreshMassPerAreaKgPerDay):
    self._harvestedShootFreshMassPerAreaKgPerDay = harvestedShootFreshMassPerAreaKgPerDay






