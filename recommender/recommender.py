from typing import List

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx

from data_structures.subject import Subject, Area, SubjectType, StudentStatus
from data_structures.course import Course
from grids.sin import subjects
from .sin_service import SinService
class Recommender:

    def __init__(self):
        print("Recommender instanced")

    @staticmethod
    def process(currentSemester: int, area: Area, subjects_completed: List[Subject], 
                course: Course):
        studentGrid: List[Subject]
        
        if course == Course.SISTEMAS_DE_INFORMACAO:
            studentGrid = Recommender.set_completed_subjects(subjects_completed, Course.SISTEMAS_DE_INFORMACAO)

        #ranking_required_subjects = Recommender.recommend_require(studentGrid, currentSemester)
        #ranking_optional_subjects = Recommender.recommend_optional(area, Recommender.get_missing_required_subjects(studentGrid))

        
        areaAdjMatrix = Recommender.create_adjacency_matrix(studentGrid)
        Recommender.plotGraph(studentGrid, areaAdjMatrix)

    @staticmethod
    def create_adjacency_matrix(grid: List[Subject]) -> np.ndarray:
        adjMatrix = np.zeros((len(grid), len(grid)), dtype=int)

        for i in range(len(grid)):
            subjectU = grid[i]
            for j in range(len(grid)):
                if i == j:
                    continue

                subjectD = grid[j]
                if subjectU.cod in subjectD.prerequisites: 
                    adjMatrix[i][j] = 1
                    
        return adjMatrix

    @staticmethod
    def plotGraph(grid: list[Subject], adjMatrix: np.ndarray) -> None:
        G = nx.DiGraph(adjMatrix)

        positions = nx.fruchterman_reingold_layout(G, k=10, iterations=1000, scale=10)
        coloredG = [SinService.color_grid_by_area(grid).get(node, 'skyblue') for node in G.nodes()]

        plt.figure(figsize=(20,20))
        labels = []
        for subject in grid:
            labels.append(str(subject.name))

        node_labels = {node: labels[node] for node in G.nodes()}

        nx.draw(G, positions, with_labels=True, labels=node_labels, font_weight='bold', 
                node_size=700, node_color=coloredG, font_size=10, font_color='black', 
                edge_color='gray', linewidths=1, alpha=0.7)
        plt.show()

    @staticmethod 
    def get_missing_required_subjects(studentGrid: List[Subject]) -> List[Subject]:
        required_subjects_missing: List[Subject] = []
        
        for subject in studentGrid:
            if subject.type == SubjectType.REQUIRED and subject.studentStatus == StudentStatus.PENDING:
                required_subjects_missing = subject

        return required_subjects_missing

    @staticmethod 
    def get_missing_optional_subjects(studentGrid: List[Subject]) -> List[Subject]:
        optional_subjects_missing: List[Subject] = []
        
        for subject in studentGrid:
            if subject.type == SubjectType.OPTIONAL and subject.studentStatus == StudentStatus.PENDING:
                optional_subjects_missing = subject

        return optional_subjects_missing

    @staticmethod
    def define_required_subject_relevance(subjectCod: str, studentCurrentSemester: int, 
                                 requiredSubjectsPending: List[Subject]):
        
        subject: Subject = filter(lambda x: x.cod == subjectCod, subjects)[0]

        return {
            'defaultSemester': subject.default_semester,
            'subject_prerequisities_len': len(subject.prerequisites),
            'remaining_subjects_len': Recommender.remaining_required_subjects(subject, studentCurrentSemester),
            'dependents_subjects_len': Recommender.count_prerequisities(subject.cod, requiredSubjectsPending),
        }
        
    @staticmethod        
    def remaining_required_subjects(subject: Subject, studentCurrentSemester: int) -> int:
        remaining_subjects = 0

        if (studentCurrentSemester > subject.default_semester and subject['Status'] == 'Pendente'):
            remaining_subjects = studentCurrentSemester - subject.default_semester

        return remaining_subjects
    
    @staticmethod
    def count_prerequisities(subjectCod: int, requiredSubjectsPending: List[Subject]):
        n = 0

        for subject in requiredSubjectsPending:
            if subjectCod in subject.prerequisites:
                n += 1

        return n
    
    @staticmethod
    def ranking_required_subjects(grid: List[Subject], studentGraph: dict[str, object]):
        
        ranking = sorted(grid, key=lambda x: x[1]['remaining_subjects_len'] + x[1]['subject_prerequisities_len'] + x[1]['dependents_subjects_len'] - x[1]['semestre'], reverse=True)

        sorted_subjects = {}
        for id, _ in ranking:
            sorted_subjects[id] = studentGraph[id]

        return sorted_subjects
    
    @staticmethod
    def set_completed_subjects(completedSubjects: List[Subject], course: Course) -> List[Subject]:
        grid: List[Subject]
        
        if(course == Course.SISTEMAS_DE_INFORMACAO):    
            grid = subjects
        
        for subject in grid:
            if subject in completedSubjects:
                subject.studentStatus = StudentStatus.COMPLETED
        
        return grid
    
    @staticmethod 
    def recommend_optional(area: Area, optionalGrid: List[Subject], sorted = dict[str, Subject]):
        sorted = Recommender.optional_area(area, optionalGrid, sorted, False)
        return Recommender.optionalGrid(area, optionalGrid, sorted, True)
    
    @staticmethod
    def optional_area(area: Area, optionalGrid: List[Subject], sorted: List[Subject], inverse: bool):
        optionals = dict[str, Subject]
        for subject in optionalGrid:
            if subject.area == area and inverse == False:
                optionals[subject.cod] = subject
            
            if subject.area != area and inverse == True:
                optionals[subject.cod] = subject

            if len(optionals) == 0:
                continue 
        return optionals

    @staticmethod
    def recommend_require(studentGraph: object, studentSemester = 1):
        required_subjects_remaining = Recommender.remaining_required_subjects(studentGraph)

        relevancia_materias_obrigatorias = {}
        for id in required_subjects_remaining:
            relevancia_materias_obrigatorias[id] = Recommender.define_subject_relevance(id, required_subjects_remaining, studentSemester)

        return Recommender.ranking_subjects(relevancia_materias_obrigatorias, studentGraph)