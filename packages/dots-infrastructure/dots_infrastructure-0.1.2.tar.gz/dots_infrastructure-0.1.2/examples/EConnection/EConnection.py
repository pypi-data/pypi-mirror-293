# -*- coding: utf-8 -*-
from datetime import datetime
import random
import helics as h

from dots_infrastructure import CalculationServiceHelperFunctions
from dots_infrastructure.DataClasses import EsdlId, HelicsCalculationInformation, PublicationDescription, SubscriptionDescription
from dots_infrastructure.HelicsFederateHelpers import HelicsSimulationExecutor, HelicsCombinationFederateExecutor
from dots_infrastructure.Logger import LOGGER
from esdl.esdl import EnergySystem

class CalculationServiceEConnection(HelicsSimulationExecutor):

    def __init__(self):
        super().__init__()

        subscriptions_values = [
            SubscriptionDescription("PVInstallation", "PV_Dispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        publication_values = [
            PublicationDescription(True, "EConnection", "EConnectionDispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        e_connection_period_in_seconds = 60

        calculation_information = HelicsCalculationInformation(e_connection_period_in_seconds, 0, False, False, True, "EConnectionDispatch", subscriptions_values, publication_values, self.e_connection_dispatch)
        self.add_calculation(calculation_information)

        publication_values = [
            PublicationDescription(True, "EConnection", "Schedule", "W", h.HelicsDataType.VECTOR)
        ]

        e_connection_period_in_seconds = 21600

        calculation_information_schedule = HelicsCalculationInformation(e_connection_period_in_seconds, 0, False, False, True, "EConnectionSchedule", [], publication_values, self.e_connection_da_schedule)
        self.add_calculation(calculation_information_schedule)

    def e_connection_dispatch(self, param_dict : dict, simulation_time : datetime, esdl_id : EsdlId, energy_system : EnergySystem):
        pv_dispatch = CalculationServiceHelperFunctions.get_single_param_with_name(param_dict, "PV_Dispatch")
        ret_val = {}
        LOGGER.info(f"Executing e_connection_dispatch with pv dispatch value {pv_dispatch}")
        ret_val["EConnectionDispatch"] = pv_dispatch * random.randint(1,3)
        self.influx_connector.set_time_step_data_point(esdl_id, "EConnectionDispatch", simulation_time, ret_val["EConnectionDispatch"])
        return ret_val
    
    def e_connection_da_schedule(self, param_dict : dict, simulation_time : datetime, esdl_id : EsdlId, energy_system : EnergySystem):
        ret_val = {}
        ret_val["Schedule"] = [1.0,2.0,3.0]
        self.influx_connector.set_time_step_data_point(esdl_id, "EConnectionDispatch", simulation_time, ret_val["EConnectionDispatch"])
        return ret_val

if __name__ == "__main__":

    helics_simulation_executor = CalculationServiceEConnection()
    helics_simulation_executor.start_simulation()
    helics_simulation_executor.stop_simulation()