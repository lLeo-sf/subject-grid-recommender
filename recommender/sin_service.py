from typing import List
from data_structures.subject import Subject, Area


class SinService:

    def __init__(self):
        print("SinService instanced")

    @staticmethod
    def color_grid_by_area(grid: List[Subject]) -> dict[str, Subject]:

        software_development_and_engineering = "blue"
        data_persistence_and_analysis = "yellow"
        computational_methodologies_and_optimization = "orange"
        computer_networks_and_systems = "brown"
        computation_theory = "gold"
        mathematics_of_computation = "red"
        management_and_administration = "pink"
        human_aspects_in_computing = "green"

        coloredGridByArea: dict[str, Subject] = {}
        for (subject) in grid:
            if subject.area == Area.SOFTWARE_DEVELOPMENT_AND_ENGINEERING:
                coloredGridByArea[subject.cod] = software_development_and_engineering
            elif subject.area == Area.MANAGEMENT_AND_ADMINISTRATION:
                coloredGridByArea[subject.cod] = management_and_administration
            elif subject.area == Area.COMPUTATIONAL_METHODOLOGIES_AND_OPTIMIZATION:
                coloredGridByArea[subject.cod] = computation_theory
            elif subject.area == Area.HUMAN_ASPECTS_IN_COMPUTING:
                coloredGridByArea[subject.cod] = human_aspects_in_computing
            elif subject.area == Area.DATA_PERSISTENCE_AND_ANALYSIS:
                coloredGridByArea[subject.cod] = data_persistence_and_analysis
            elif subject.area ==  Area.COMPUTER_NETWORKS_AND_SYSTEMS:
                coloredGridByArea[subject.cod] = computer_networks_and_systems

        return coloredGridByArea
    
    
    
    

    
    
    