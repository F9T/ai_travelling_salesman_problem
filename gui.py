# -coding: UTF-8
import pygame
import sys
from city import City
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN


class Gui(object):

    def __init__(self, width=500, height=500, city_color=[10, 10, 200], city_radius=3):
        self.width = width
        self.height = height
        self.window = None
        self.screen = None
        pygame.init()
        pygame.display.set_caption('Problème du voyageur de commerce')
        self.font = pygame.font.Font(None, 30)
        self.city_color = city_color
        self.city_radius = city_radius
        self.font_color = [255, 255, 255]

    def show(self, cities=[]):
        self.window = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.display.get_surface()
        self.collection_cities(cities)

    def wait(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    pygame.display.flip()

    def collection_cities(self, cities):
        collecting = True
        self.draw_cities(cities)

        while collecting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    collecting = False
                elif event.type == MOUSEBUTTONDOWN:
                    city = City(len(cities), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    cities.append(city)
                    self.draw_cities(cities)

                self.screen.fill(0)
        pygame.display.flip()

    def draw_cities(self, cities):
        self.screen.fill(0)
        for city in cities:
            pygame.draw.circle(self.screen, self.city_color, (city.x, city.y), self.city_radius)
        text = self.font.render("Nombre: %i" % len(cities), True, self.font_color)
        textRect = text.get_rect()
        self.screen.blit(text, textRect)
        pygame.display.flip()

    ##
    def draw_best_path(self, population):
        ''' Permet de dessiner sur la fenêtre la liste des genes (villes) ainsi que le meilleur chemin
            Argument :
            population -- La population actuelle
        '''
        self.window.fill(0)
        text = self.font.render("Nombre: %i" % len(cities), True, self.font_color)
        textRect = text.get_rect()
        self.screen.blit(text, textRect)

        for point in cities:
            pygame.draw.rect(self.window, self.city_color, [point.x, point.y, self.city_radius, self.city_radius])

        list_points = []
        best_genes_list = population[0].genes
        for gene in best_genes_list:
            list_points.append((cities[gene].x, cities[gene].y))

        list_points.append((cities[best_genes_list[0]].x, cities[best_genes_list[0]].y))
        pygame.draw.lines(self.window, self.city_color, False, list_points, 1)
        pygame.display.update()
