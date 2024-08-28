# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 11:25:51 2022

@author: dingq
"""

import pandas as pd
from datetime import datetime, timedelta

from caplibproto.dqnumerics_pb2 import *
from caplibproto.dqdatetime_pb2 import *
from caplibproto.dqanalytics_pb2 import *

from caplib.numerics import *
from caplib.datetime import *

# CompoundingType
def to_compounding_type(src):
    '''
    将字符串转换为 CompoundingType类型.
    
    Parameters
    ----------
    src : str
        表示复利类型的字符串，如‘CONTINUOUS_COMPOUNDING’.

    Returns
    -------
    CompoundingType       

    '''
    if src is None:
        return INVALID_COMPOUNDING_TYPE
    if src in ['', 'nan']:
        return INVALID_COMPOUNDING_TYPE
    else:
        return CompoundingType.DESCRIPTOR.values_by_name[src.upper()].number


# PricingModelName
def to_pricing_model_name(src):
    '''
    将字符串转换为 PricingModelName 类型.
    
    Parameters
    ----------
    src : str
        表示定价模型的字符串，如‘BLACK_SCHOLES_MERTON’.

    Returns
    -------
    PricingModelName       

    '''
    if src is None:
        return INVALID_PRICING_MODEL_NAME
    if src in ['', 'nan']:
        return INVALID_PRICING_MODEL_NAME
    else:
        return PricingModelName.DESCRIPTOR.values_by_name[src.upper()].number


# PricingMethodName
def to_pricing_method_name(src):
    '''
    将字符串转换为 PricingMethodName 类型.

    Parameters
    ----------
    src : str
        表示定价方法类型的字符串，如‘ANALYTICAL’.

    Returns
    -------
    PricingMethodName       

    '''
    if src is None:
        return ANALYTICAL
    if src in ['', 'nan']:
        return ANALYTICAL
    else:
        return PricingMethodName.DESCRIPTOR.values_by_name[src.upper()].number


# FiniteDifferenceMethod
def to_finite_difference_method(src):
    '''
    将字符串转换为 FiniteDifferenceMethod 类型.
    
    Parameters
    ----------
    src : str
        表示差分方法类型的字符串，如‘CENTRAL_DIFFERENCE_METHOD’.

    Returns
    -------
    FiniteDifferenceMethod       

    '''
    if src is None:
        return CENTRAL_DIFFERENCE_METHOD
    if src in ['', 'nan']:
        return CENTRAL_DIFFERENCE_METHOD
    else:
        return FiniteDifferenceMethod.DESCRIPTOR.values_by_name[src.upper()].number


# ThreadingMode
def to_threading_mode(src):
    '''
    将字符串转换为 ThreadingMode 类型.
    
    Parameters
    ----------
    src : str
        表示线程模式的字符串，如‘SINGLE_THREADING_MODE’.

    Returns
    -------
    ThreadingMode       

    '''
    if src is None:
        return SINGLE_THREADING_MODE
    if src in ['', 'nan']:
        return SINGLE_THREADING_MODE
    else:
        return ThreadingMode.DESCRIPTOR.values_by_name[src.upper()].number


# RiskGranularity
def to_risk_granularity(src):
    '''
    将字符串转换为 RiskGranularity 类型.
    
    Parameters
    ----------
    src : str
        表示风险颗粒度模式的字符串，如‘TOTAL_RISK’.

    Returns
    -------
    RiskGranularity       

    '''
    if src is None:
        return TOTAL_RISK
    if src in ['', 'nan']:
        return TOTAL_RISK
    else:
        return RiskGranularity.DESCRIPTOR.values_by_name[src.upper()].number


# IrYieldCurveBuildingMethod
def to_ir_yield_curve_building_method(src):
    '''
    将字符串转换为 IrYieldCurveBuildingMethod 类型.

    Parameters
    ----------
    src : str
        表示收益率曲线构建类型的字符串，如‘BOOTSTRAPPING_METHOD’.

    Returns
    -------
    IrYieldCurveBuildingMethod

    '''
    if src is None:
        return BOOTSTRAPPING_METHOD
    if src in ['', 'nan']:
        return BOOTSTRAPPING_METHOD
    else:
        return IrYieldCurveBuildingMethod.DESCRIPTOR.values_by_name[src.upper()].number


# IrYieldCurveType
def to_ir_yield_curve_type(src):
    '''
    将字符串转换为 IrYieldCurveType.

    Parameters
    ----------
    src : str
        表示收益率曲线类型的字符串，如‘ZERO_RATE’.

    Returns
    -------
    IrYieldCurveType

    '''
    if src is None:
        return ZERO_RATE
    if src in ['', 'nan']:
        return ZERO_RATE
    else:
        return IrYieldCurveType.DESCRIPTOR.values_by_name[src.upper()].number
    
    
# Pricing Model Settings
def create_model_settings(model_name: str,
                          constant_params=[0.0],
                          time_homogeneous_model_params=[],
                          underlying='',
                          model_calibrated=False):
    '''
    创建定价模型的参数设置对象.
    
    Parameters
    ----------
    model_name : str
        模型名称，查看可支持的模型:'PricingModelName'.
    constant_params : list, optional
        非时间函数的模型参数值，如Displaced Black模型中的Displacement参数.
    time_homogeneous_model_params : list, optional
        期限结构的模型参数值,如Hull-White利率模型中的期限结构波动率P参数.
    underlying : str, optional
        模型所对应的标的资产名称，如货币对‘USDCNY’， 沪深300指数等.
    model_calibrated : bool, optional
        标识模型参数是否已校验，默认值为否.

    Returns
    -------
    PricingModelSettings
        定价模型的Parameters设置对象
    '''
    return dqCreateProtoPricingModelSettings(to_pricing_model_name(model_name),
                                             constant_params,
                                             time_homogeneous_model_params,
                                             underlying,
                                             model_calibrated)


# PDE Settings
def create_pde_settings(t_size=50,
                        x_size=100, x_min=-4.0, x_max=4.0, x_min_max_type='MMT_NUM_STDEVS',
                        x_density=1.0, x_grid_type='UNIFORM_GRID', x_interp_method='LINEAR_INTERP',
                        y_size=3, y_min=-4.0, y_max=4.0, y_min_max_type='MMT_NUM_STDEVS',
                        y_density=1.0, y_grid_type='UNIFORM_GRID', y_interp_method='LINEAR_INTERP',
                        z_size=3, z_min=-4.0, z_max=4.0, z_min_max_type='MMT_NUM_STDEVS',
                        z_density=1.0, z_grid_type='UNIFORM_GRID', z_interp_method='LINEAR_INTERP'):
    '''
    创建PDE数值解法需要的参数设置对象.
    
    Parameters
    ----------
    t_size : int, optional
        时间网格的点数尺寸，默认值为50.
    x_size : int, optional
        空间第一维度网格的点数尺寸，默认值为100.
    x_min : float, optional
        空间第一维度网格的下边界值，可以为绝对值或标准差数，默认值为4个标准差.
    x_max : float, optional
        空间第一维度网格的上边界值，可以为绝对值或标准差数，默认值为4个标准差.
    x_min_max_type : PdeSettings.MinMaxType, optional
        空间第一维度网格的边界值类型，可以为绝对值或标准差类型，默认值为标准差 MMT_NUM_STDEVS.
    x_density : float, optional
        空间第一维度网格的密度Parameters，这是针对非均匀网格的时候。默认值为1.0.
    x_grid_type : GridType, optional
        空间第一维度网格的类型，分为均匀网格和非均匀网格。默认值为1.0.
    x_interp_method : InterpMethod, optional
        空间第一维度网格使用的插值方法，默认为线性插值（LINEAR_INTERP）.
    y_size : int, optional
        Size of 2nd dimension spatial grid. The default is 3.
    y_min : float, optional
        Lower boundary of 2nd dimension spatial grid and it can be either an absolute boundary value or standard devidation. The default is -4.0.
    y_max : float, optional
        Upper boundary of 2nd dimension spatial grid and it can be either an absolute boundary value or standard devidation. The default is 4.0.
    y_min_max_type : PdeSettings.MinMaxType, optional
        The boundary value type for 2nd dimension spatial grid. The default is 'MMT_NUM_STDEVS'.
    y_density : float, optional
        The density of 2nd dimension spatial grid when the grid is non-uniform. The default is 1.0.
    y_grid_type : GridType, optional
        The type of 2nd dimension spatial grid. The default is 'UNIFORM_GRID'.
    y_interp_method : InterpMethod, optional
        The interpolation method for 2nd dimension spatial grid. The default is 'LINEAR_INTERP'.
    z_size : int, optional
        Size of 3rd dimension spatial grid. The default is 3.
    z_min : float, optional
        Lower boundary of 3rd dimension spatial grid and it can be either an absolute boundary value or standard devidation. The default is -4.0.
    z_max : float, optional
        Upper boundary of 3rd dimension spatial grid and it can be either an absolute boundary value or standard devidation. The default is 4.0.
    z_min_max_type : PdeSettings.MinMaxType, optional
        The boundary value type for 3rd dimension spatial grid. The default is 'MMT_NUM_STDEVS'.
    z_density : float, optional
        The density of 3rd dimension spatial grid when the grid is non-uniform. The default is 1.0.
    z_grid_type : GridType, optional
        The type of 3rd dimension spatial grid. The default is 'UNIFORM_GRID'.
    z_interp_method : InterpMethod, optional
        The interpolation method for 3rd dimension spatial grid. The default is 'LINEAR_INTERP'.

    Returns
    -------
    PdeSettings
        PDE数值解法需要的参数设置对象
    '''
    return dqCreateProtoPdeSettings(t_size,
                                    x_size, x_min, x_max, to_pde_min_max_type(x_min_max_type),
                                    y_size, y_min, y_max, to_pde_min_max_type(y_min_max_type),
                                    z_size, z_min, z_max, to_pde_min_max_type(z_min_max_type),
                                    x_density, y_density, z_density,
                                    to_grid_type(x_grid_type),
                                    to_grid_type(y_grid_type),
                                    to_grid_type(z_grid_type),
                                    to_interp_method(x_interp_method),
                                    to_interp_method(y_interp_method),
                                    to_interp_method(z_interp_method))


# Monte Carlo Settings
def create_monte_carlo_settings(num_simulations=1024,
                                uniform_number_type='SOBOL_NUMBER',
                                seed=1024,
                                wiener_process_build_method='BROWNIAN_BRIDGE_METHOD',
                                gaussian_number_method='INVERSE_CUMULATIVE_METHOD',
                                use_antithetic=False,
                                num_steps=1):
    '''
    创建蒙特卡洛仿真需要的参数设置对象.

    Parameters
    ----------
    num_simulations : int, optional
        蒙特卡洛仿真次数，默认值为1024.
    uniform_number_type : UniformRandomNumberType, optional
        均匀分布随机数类型，默认值为Sobol随机数（SOBOL_NUMBER）.
    seed : int, optional
        产生均匀分布随机数需要的种子值，默认为1024.
    wiener_process_build_method : WienerProcessBuildMethod, optional
        构建布朗运动过程的方法，默认为布朗桥方法（BROWNIAN_BRIDGE_METHOD）.
    gaussian_number_method : GaussianNumberMethod, optional
        根据均匀分布随机数生成正态分布随机数的方法，默认为INVERSE_CUMULATIVE_METHOD.
    use_antithetic : bool, optional
        设置是否使用Antithetic的方差减少方法，默认为否（False）.
    num_steps : int, optional
        设置在创建布朗运动过程中每个时间区间中所需的额外步长，默认为1.

    Returns
    -------
    MonteCarloSettings    
        蒙特卡洛仿真需要的参数设置对象.
    '''
    return dqCreateProtoMonteCarloSettings(num_simulations,
                                           to_uniform_random_number_type(uniform_number_type),
                                           seed,
                                           to_wiener_process_build_method(wiener_process_build_method),
                                           to_gaussian_number_method(gaussian_number_method),
                                           use_antithetic,
                                           num_steps)


# Pricing Settings:
def create_pricing_settings(pricing_currency,
                            inc_current,
                            model_settings,
                            pricing_method,
                            pde_settings,
                            mc_settings,
                            specific_pricing_requests=[],
                            cash_flows=False):
    '''
    创建产品定价所需的参数设置，包括模型参数，定价方法，PDE数值解法参数，蒙特卡洛参数，以及用户指定指标.
    
    Parameters
    ----------
    pricing_currency: str, optional
        产品定价所指定的货币.
    inc_current : bool
        设置是否将当前的现金流计入产品现值中.
    model_settings : PricingModelSettings
        设置定价模型参数.
    pricing_method : str
        指定定价方法，如解析解或其它数值解法.
    pde_settings : PdeSettings
        设置PDE数值解法参数，如果定价方法为PDE.
    mc_settings : MonteCarloSettings
        设置蒙特卡洛仿真参数，如果定价方法为蒙特卡洛.
    specific_pricing_requests : list, optional
        设置针对特定产品的计算指标，如对于债券，有到期收益率，全价，净价等， 默认为空.
    cash_flows: bool, optional
    
    Returns
    -------
    PricingSettings
        产品定价所需的参数设置.
    '''
    return dqCreateProtoPricingSettings(pricing_currency,
                                        inc_current,
                                        pde_settings,
                                        mc_settings,
                                        model_settings,
                                        to_pricing_method_name(pricing_method),
                                        specific_pricing_requests,
                                        cash_flows)


# Default Pricing Settings:
def create_model_free_pricing_settings(pricing_currency='',
                                       inc_current=True,
                                       specific_pricing_requests=[],
                                       cash_flows=False):
    '''
    创建无需模型的产品定价所需的参数设置.
    
    Parameters
    ----------
    pricing_currency: str, optional
        Currency specified for instrument pricing.
    inc_current : bool, optional
        设置是否将当前的现金流计入产品现值中， 默认为是（True） .
    specific_pricing_requests : list, optional
        设置针对特定产品的计算指标，如对于债券，有到期收益率，全价，净价等， 默认为空.
    cash_flows: bool, optional

    Returns
    -------
    PricingSettings
        产品定价所需的参数设置.

    '''
    return create_pricing_settings(pricing_currency,
                                   inc_current,
                                   create_model_settings(''),
                                   'ANALYTICAL',
                                   create_pde_settings(),
                                   create_monte_carlo_settings(),
                                   specific_pricing_requests,
                                   cash_flows)


# IR Curve Risk Settings:
def create_ir_curve_risk_settings(delta=False,
                                  gamma=False,
                                  curvature=False,
                                  shift=1.0e-4,
                                  curvature_shift=5.0e-3,
                                  method='CENTRAL_DIFFERENCE_METHOD',
                                  granularity='TOTAL_RISK',
                                  scaling_factor=1.0e-4,
                                  threading_mode='SINGLE_THREADING_MODE'):
    '''
    创建计算利率收益率曲线敏感度的风险参数设置.
    
    Parameters
    ----------
    delta : bool, optional
        设置是否计算曲线Delta（DV01），默认为否.
    gamma : bool, optional
        设置是否计算曲线Gamma，默认为否.
    curvature : bool, optional
        设置是否计算曲线Curvature,根据FRTB定义，默认为否.
    shift : float, optional
        计算曲线Delta和Gamma时的扰动大小，默认为1基点.
    curvature_shift : float, optional
        计算曲线Curvature的扰动大小，默认为50基点.
    method : FiniteDifferenceMethod, optional
        计算曲线Delta的差分方法，默认为中央差分法（CENTRAL_DIFFERENCE_METHOD）.
    granularity : RiskGranularity, optional
        设置计算曲线Delta和Gamma的颗粒度，默认为整体平移（TOTAL_RISK）.
    scaling_factor : float, optional
        将百分比型的敏感度转换成实际的价格变化绝对值的因子值，默认为1基点.
    threading_mode : ThreadingMode, optional
        计算敏感度时的线程模式，可以设为单线程和多线程两种，默认为单线程.

    Returns
    -------
    IrCurveRiskSettings
        计算利率收益率曲线敏感度的风险参数设置对象.
    '''
    return dqCreateProtoIrCurveRiskSettings(delta, gamma, curvature, shift, curvature_shift,
                                            to_finite_difference_method(method),
                                            to_risk_granularity(granularity),
                                            scaling_factor,
                                            to_threading_mode(threading_mode))


# Credit Curve Risk Settings:
def create_credit_curve_risk_settings(delta=False,
                                      gamma=False,
                                      shift=1.0e-4,
                                      method='CENTRAL_DIFFERENCE_METHOD',
                                      granularity='TOTAL_RISK',
                                      scaling_factor=1.0e-4,
                                      threading_mode='SINGLE_THREADING_MODE'):
    '''
    创建计算信用曲线敏感度需要的风险参数设置.
    
    Parameters
    ----------
    delta : bool, optional
        设置是否计算曲线Delta（CS01），默认为否.
    gamma : bool, optional
        设置是否计算曲线Gamma，默认为否
    shift : float, optional
        计算曲线Delta和Gamma时的扰动大小，默认为1基点.
    method : FiniteDifferenceMethod, optional
        计算曲线Delta的差分方法，默认为中央差分法（CENTRAL_DIFFERENCE_METHOD）.
    granularity : RiskGranularity, optional
        设置计算曲线Delta和Gamma的颗粒度，默认为整体平移（TOTAL_RISK）.
    scaling_factor : float, optional
        将百分比型的敏感度转换成实际的价格变化绝对值的因子值，默认为1基点.
    threading_mode : ThreadingMode, optional
        计算敏感度时的线程模式，可以设为单线程和多线程两种，默认为单线程.

    Returns
    -------
    CreditCurveRiskSettings
        计算信用曲线敏感度需要的风险参数设置对象.

    '''
    return dqCreateProtoCreditCurveRiskSettings(delta, gamma, shift,
                                                to_finite_difference_method(method),
                                                to_risk_granularity(granularity),
                                                scaling_factor,
                                                to_threading_mode(threading_mode))


# Theta Risk Settings:
def create_theta_risk_settings(theta=False, shift=1, scaling_factor=1. / 365.):
    '''
    创建计算Theta的参数设置.
    
    Parameters
    ----------
    theta : bool, optional
        设置是否计算Theta，默认为否.
    shift : int, optional
        计算曲线Delta和Gamma时的扰动大小，默认为1天.
    scaling_factor : float, optional
        将百分比型的敏感度转换成实际的价格变化绝对值的因子值，默认为1./365.

    Returns
    -------
    ThetaRiskSettings
        计算Theta的参数设置对象.

    '''
    return dqCreateProtoThetaRiskSettings(theta, shift, scaling_factor)


# IR Yield Curve:
def create_ir_yield_curve(as_of_date,
                          currency,
                          term_dates,
                          zero_rates,
                          day_count='ACT_365_FIXED',
                          interp_method='LINEAR_INTERP',
                          extrap_method='FLAT_EXTRAP',
                          compounding_type='CONTINUOUS_COMPOUNDING',
                          frequency='ANNUAL',
                          jacobian=[0.0],
                          curve_name='',
                          pillar_names=['']):
    '''
    创建利率收益率曲线.
    
    Parameters
    ----------
    as_of_date : datetime
        利率收益率曲线的参考日期
    currency : str
        利率收益率曲线的参考货币.
    term_dates : list of datetime
        一组递增的日期，并且每个日期必须在参考日期之后.
    zero_rates : list
        一组零息利率值，对应上面的一组日期.
    day_count : str, optional
        计息区间惯例，默认为ACT_365_FIXED.
    interp_method : str, optional
        曲线零息利率的插值方法，默认为线性插值.
    extrap_method : str, optional
        曲线零息利率的外插方法，默认为平推.
    compounding_type : str, optional
        计算折现率使用的复利类型，默认为连续复利.
    frequency : Frequency, optional
        当复利为离散型时，计算折现率使用的频率参数.
    jacobian : list, optional
        市场行情曲线对零息曲线的Jacobian矩阵，默认为单值为0的列表.
    curve_name : str, optional
        创建曲线时用户给定的曲线名称，默认为空.
    pillar_names : list, optional
        曲线每个关键期限点的名称，如['1M', '3M'].

    Returns
    -------
    IrYieldCurve
        利率收益率曲线对象.
    '''    
    pillar_dates = [create_date(d) for d in term_dates]
    p_ts_curve = dqCreateProtoTermStructureCurve(create_date(as_of_date),
                                                 to_day_count_convention(day_count),
                                                 pillar_dates, pillar_names, dqCreateProtoVector(zero_rates),
                                                 to_interp_method(interp_method),
                                                 to_extrap_method(extrap_method),
                                                 curve_name)
    p_asset_curve = dqCreateProtoAssetYieldCurve(p_ts_curve,
                                                 to_compounding_type(compounding_type))
    p_mat = dqCreateProtoMatrix(len(jacobian), 1,
                                jacobian,
                                Matrix.StorageOrder.ColMajor)
    p_jacobian = dqCreateProtoIrYieldCurve_Jacobian(curve_name, p_mat)
    
    zero_curve = dqCreateProtoIrYieldCurve(IrYieldCurveType.ZERO_RATE,
                                           p_asset_curve,
                                           currency,
                                           to_frequency(frequency),
                                           [p_jacobian])
    return zero_curve


# Flat IR Yield Curve
def create_flat_ir_yield_curve(as_of_date,
                               currency,
                               rate):
    '''
    创建一条水平利率收益率曲线.
    
    Parameters
    ----------
    as_of_date : datetime
        利率收益率曲线的参考日期.
    currency : str
        利率收益率曲线的参考货币.
    rate : float
        曲线收益率水平.

    Returns
    -------
    IrYieldCurve
        利率收益率曲线对象.
    '''
    start = as_of_date + timedelta(days=1)
    end = as_of_date + timedelta(days=365.25 * 100)
    term_dates = [start, end]
    rates = [rate] * 2
    return create_ir_yield_curve(as_of_date, currency, term_dates, rates)


# Credit Curve:
def create_credit_curve(as_of_date,
                        term_dates,
                        hazard_rates,
                        day_count='ACT_365_FIXED',
                        interp_method='LINEAR_INTERP',
                        extrap_method='FLAT_EXTRAP',
                        curve_name='',
                        pillar_names=['']):
    '''
    创建一条信用利差曲线.
    
    Parameters
    ----------
    as_of_date : Date
        信用利差曲线的参考日期.
    term_dates : list
        一组递增的日期，并且每个日期必须在参考日期之后.
    hazard_rates : list
        一组风险率，对应上面的一组日期.
    day_count : DayCountConvention, optional
        计息区间惯例，默认为ACT_365_FIXED.
    interp_method : InterpMethod, optional
        曲线插值方法，默认为线性插值.
    extrap_method : ExtrapMethod, optional
        曲线外插方法，默认为平推.
    curve_name : str, optional
        创建曲线时用户给定的曲线名称，默认为空.
    pillar_names : list, optional
        曲线每个关键期限点的名称，如['1M', '3M'].

    Returns
    -------
    CreditCurve
        信用利差曲线对象.

    '''
    pillar_dates = [create_date(d) for d in term_dates]
    p_ts_curve = dqCreateProtoTermStructureCurve(create_date(as_of_date),
                                                 to_day_count_convention(day_count),
                                                 pillar_dates, pillar_names, dqCreateProtoVector(hazard_rates),
                                                 to_interp_method(interp_method),
                                                 to_extrap_method(extrap_method),
                                                 curve_name)

    cs_curve = dqCreateProtoCreditCurve(p_ts_curve, dqCreateProtoVector(hazard_rates))
    return cs_curve


# Flat Credit Curve
def create_flat_credit_curve(as_of_date,
                             hazard_rate):
    '''
    创建一条水平风险率的信用曲线.
    
    Parameters
    ----------
    as_of_date : Date
        信用利差曲线的参考日期.
    hazard_rate : float
        曲线风险率水平.

    Returns
    -------
    CreditCurve.
        信用利差曲线对象.

    '''
    start = as_of_date + timedelta(days=1)
    end = as_of_date + timedelta(days=365.25 * 100)
    term_dates = [start, end]
    hazard_rates = [hazard_rate] * 2
    return create_credit_curve(as_of_date, term_dates, hazard_rates)


def print_term_structure_curve(curve):
    '''
    将任意期限结构曲线以pandas.DataFrame的结构展示

    Parameters
    ----------
    curve : TermStructuredCurve
        一条期限结构曲线
    
    Returns
    -------
    pandas.DataFrame

    '''
    curve_dates = list()
    curve_values = list()
    for i in range(len(curve.pillar_date)):
        p_date = curve.pillar_date[i]
        curve_dates.append(dt.datetime(p_date.year, p_date.month, p_date.day).strftime('%Y-%m-%d'))
        curve_values.append(curve.pillar_values.data[i])
    df = pd.DataFrame(columns=['Date', 'Value'])
    df['Date'] = curve_dates
    df['Value'] = curve_values
    return df


def to_vol_smile_type(src):
    '''
    将字符串转换为VolSmileType类型.

    Parameters
    ----------
    src : str
        a string of vol smile type, i.e. 'STRIKE_VOL_SMILE'.

    Returns
    -------
    VolSmileType

    '''
    if src is None:
        return INVALID_VOL_SMILE_TYPE
    if src in ['', 'nan']:
        return INVALID_VOL_SMILE_TYPE
    else:
        return VolSmileType.DESCRIPTOR.values_by_name[src.upper()].number


def to_vol_smile_method(src):
    '''
    将字符串转换为VolSmileMethod类型.

    Parameters
    ----------
    src : str
        a string of vol smile method, i.e. 'LINEAR_SMILE_METHOD'.

    Returns
    -------
    VolSmileMethod

    '''
    if src is None:
        return INVALID_VOL_SMILE_METHOD
    if src in ['', 'nan']:
        return INVALID_VOL_SMILE_METHOD
    else:
        return VolSmileMethod.DESCRIPTOR.values_by_name[src.upper()].number

#VolTermInterpMethod
def to_vol_term_time_interp_method(src):
    if src is None:
        return LINEAR_IN_VARIANCE
    
    if src in ['', 'nan']:
        return LINEAR_IN_VARIANCE
    else:
        return VolTermInterpMethod.DESCRIPTOR.values_by_name[src.upper()].number

#VolTermExtrapMethod 
def to_vol_termtime_extrap_method(src):
    if src is None:
        return FLAT_IN_VOLATILITY
    
    if src in ['', 'nan']:
        return FLAT_IN_VOLATILITY
    else:
        return VolTermExtrapMethod.DESCRIPTOR.values_by_name[src.upper()].number

#VolatilityType 
def to_volatility_type(src):
    if src is None:
        return LOG_NORMAL_VOL_TYPE
    
    if src in ['', 'nan']:
        return LOG_NORMAL_VOL_TYPE
    else:
        return VolatilityType.DESCRIPTOR.values_by_name[src.upper()].number
    
#WingStrikeType 
def to_wing_strike_type(src):
    if src is None:
        return DELTA
    
    if src in ['', 'nan']:
        return DELTA
    else:
        return WingStrikeType.DESCRIPTOR.values_by_name[src.upper()].number
    
def create_volatility_surface_definition(vol_smile_type,
                                         smile_method,
                                         smile_extrap_method,
                                         time_interp_method,
                                         time_extrap_method,
                                         day_count_convention,
                                         vol_type,
                                         wing_strike_type,
                                         lower,
                                         upper):
    """
    创建一个 volatility surface definition 对象.

    Parameters
    ----------
    vol_smile_type: str, VolSmileType
    smile_method: str, VolSmileMethod
    smile_extrap_method: str, ExtrapMethod
    time_interp_method: str, VolTermInterpMethod
    time_extrap_method: str, VolTermExtrapMethod
    day_count_convention: str, DayCountConvention
    vol_type: str, VolatilityType
    wing_strike_type: str, WingStrikeType
    lower: float
    upper: float

    Returns
    -------
    VolatilitySurfaceDefinition

    """
    return dqCreateProtoVolatilitySurfaceDefinition(to_vol_smile_type(vol_smile_type),
                                                    to_vol_smile_method(smile_method),
                                                    to_extrap_method(smile_extrap_method),
                                                    to_vol_term_time_interp_method(time_interp_method),
                                                    to_vol_termtime_extrap_method(time_extrap_method),
                                                    to_day_count_convention(day_count_convention),
                                                    to_volatility_type(vol_type),
                                                    to_wing_strike_type(wing_strike_type),
                                                    lower,
                                                    upper)


def create_volatility_smile(vol_smile_type,
                            reference_date,
                            strikes,
                            vols,
                            smile_method,
                            extrap_method,
                            time_interp_method,
                            time_extrap_method,
                            term,
                            model_params,
                            auxilary_params,
                            lower,
                            upper):
    """
    创建一个波动率微笑对象.

    Parameters
    ----------
    vol_smile_type: str, VolSmileType
    reference_date: datetime
    lower: float
    upper: float
    curve: Curve
    smile_method: str, VolSmileMethod
    term: float

    Returns
    -------
    VolatilitySmile

    """    
    return dqCreateProtoVolatilitySmile(to_vol_smile_type(vol_smile_type),                                        
                                        create_date(reference_date),
                                        lower,
                                        upper,
                                        dqCreateProtoVector(strikes),
                                        dqCreateProtoVector(vols),                                        
                                        to_vol_smile_method(smile_method),
                                        term,
                                        dqCreateProtoVector(model_params),
                                        dqCreateProtoVector(auxilary_params),
                                        to_extrap_method(extrap_method))


def create_yield_curve(as_of_date,
                       term_dates,
                       zero_rates,
                       day_count=ACT_365_FIXED,
                       interp_method=LINEAR_INTERP,
                       extrap_method=FLAT_EXTRAP,
                       curve_name=''):
    '''
    创建一个收益率曲线.

    Parameters
    ----------
    as_of_date : Date
        Reference date for the IR yield curve.
    term_dates : list
        A list of dates in ascending order. The dates must be in the future relative to the reference date.
    zero_rates : list
        A list of zero rates correspoding to the dates.
    day_count : DayCountConvention, optional
        Day count convention. The default is 'ACT_365_FIXED'.
    interp_method : InterpMethod, optional
        Interpolation method for the curve zero rates. The default is 'LINEAR_INTERP'.
    extrap_method : ExtrapMethod, optional
        Extrapolation method for the curve zero rates. The default is 'FLAT_EXTRAP'.
    curve_name : str, optional
        Curve name given by the user. The default is ''.

    Returns
    -------
    Curve

    '''
    size = len(term_dates)

    terms = [0.0] * size
    for i in range(size):
        terms[i] = year_frac_calculator(as_of_date, term_dates[i], day_count, as_of_date, term_dates[i], term_dates[i])

    p_interpolator = dqCreateProtoInterpolator1D(interp_method,
                                                 extrap_method,
                                                 size,
                                                 dqCreateProtoVector(terms),
                                                 dqCreateProtoVector(zero_rates),
                                                 dqCreateProtoVector([]), dqCreateProtoVector([]))
    return dqCreateProtoCurve(p_interpolator, curve_name)


def create_volatility_surface(definition,
                              reference_date,
                              vol_smiles,
                              term_dates,
                              name=""):
    """
    创建一个波动率曲面.

    Parameters
    ----------
    definition: VolatilitySurfaceDefinition
    reference_date: Date
    vol_smiles: list
    term_dates: Date
    terms: Vector
    name: str

    Returns
    -------
    VolatilitySurface

    """
    vol_dates = [create_date(d) for d in term_dates]
    return dqCreateProtoVolatilitySurface(definition,
                                          create_date(reference_date),
                                          vol_smiles,
                                          vol_dates,
                                          name)


def create_price_risk_settings(delta=False,
                               gamma=False,
                               curvature=False,
                               shift=1.0e-4,
                               curvature_shift=5.0e-3,
                               method='CENTRAL_DIFFERENCE_METHOD',
                               scaling_factor=1.0e-4,
                               threading_mode='SINGLE_THREADING_MODE'):
    """

    Parameters
    ----------
    delta : bool, optional
        Flag for indicating whether to calculate the curve delta (DV01). The default is False.
    gamma : bool, optional
        Flag for indicating whether to calculate the curve gamma. The default is False.
    curvature : bool, optional
        Flag for indicating whether to calculate the curve curvature，as defined in FRTB. The default is False.
    shift : float, optional
        The shift size for the curve delta and gamma calculation. The default is 1.0e-4.
    curvature_shift : float, optional
        The shift size for the curvature calculation. The default is 5.0e-3.
    method : FiniteDifferenceMethod, optional
        The finite difference method for the curve delta calculation. The default is 'CENTRAL_DIFFERENCE_METHOD'.
    scaling_factor : float, optional
        The scaling factor for calculating USD amount sensitivity. The default is 1.0e-4.
    threading_mode : ThreadingMode, optional
        The threading mode in the calculation of sensitivities. Two modes are single and multi threading. The default is 'SINGLE_THREADING_MODE'.

    Returns
    -------
    PriceRiskSettings

    """
    return dqCreateProtoPriceRiskSettings(delta,
                                          gamma,
                                          curvature,
                                          shift,
                                          curvature_shift,
                                          to_finite_difference_method(method),
                                          scaling_factor,
                                          to_threading_mode(threading_mode))


def create_vol_risk_settings(vega=False,
                             volga=False,
                             shift=1.0e-4,
                             method='CENTRAL_DIFFERENCE_METHOD',
                             granularity='TOTAL_RISK',
                             scaling_factor=1.0e-4,
                             threading_mode='SINGLE_THREADING_MODE'):
    """

    Parameters
    ----------
    vega: bool
    volga: bool
    shift: bool
    method: FiniteDifferenceMethod
    granularity: RiskGranularity
    scaling_factor: float
    threading_mode: ThreadingMode

    Returns
    -------
    VolRiskSettings

    """
    return dqCreateProtoVolRiskSettings(vega,
                                        volga,
                                        shift,
                                        to_finite_difference_method(method),
                                        to_risk_granularity(granularity),
                                        scaling_factor,
                                        to_threading_mode(threading_mode))


def create_price_vol_risk_settings(vanna=False,
                                   price_shift=1.0e-4,
                                   vol_shift=1.0e-4,
                                   method='CENTRAL_DIFFERENCE_METHOD',
                                   granularity='TOTAL_RISK',
                                   price_scaling_factor=1.0e-4,
                                   vol_scaling_factor=1.0e-4,
                                   threading_mode='SINGLE_THREADING_MODE'):
    """

    Parameters
    ----------
    vanna: bool
    price_shift: float
    vol_shift: float
    method: FiniteDifferenceMethod
    granularity: RiskGranularity
    price_scaling_factor: float
    vol_scaling_factor: float
    threading_mode: ThreadingMode

    Returns
    -------
    PriceVolRiskSettings

    """
    return dqCreateProtoPriceVolRiskSettings(vanna,
                                             price_shift,
                                             vol_shift,
                                             to_finite_difference_method(method),
                                             to_risk_granularity(granularity),
                                             price_scaling_factor,
                                             vol_scaling_factor,
                                             to_threading_mode(threading_mode))
