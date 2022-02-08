import sys

import pygame
import geocoder
from static_map import request_static_map


class App:
    """
    Класс отвечающий за запуск приложения. По умолчанию карта загружается на Москве
    TODO логику ввода адреса и параметров поиска вывести в отдельный класс

    """
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 500
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = 50

    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, address):
        """TODO в этом методе оставить только запрос к статик мапс
                (вызывать с параметрами coordinates, delta, z, type, point)"""
        code, toponym = geocoder.request_toponym(address)
        if code == 200:
            coords = geocoder.get_coordinates(toponym)
            delta = geocoder.get_delta(toponym)
            map_file = request_static_map(coords, delta)
            image = pygame.image.load(map_file)
        else:
            image = pygame.Surface(self.screen.get_size())
            image.fill(pygame.Color("lightblue"))

            font = pygame.font.Font(None, 40)
            text = font.render(f'Ошибка запроса! Http статус: {code}', True, (230, 255, 200))
            text_x = self.width // 2 - text.get_width() // 2
            text_y = self.height // 2 - text.get_height() // 2
            image.blit(text, (text_x, text_y))

        return image

    def run_app(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

            self.screen.fill(pygame.Color('lightblue'))
            self.screen.blit(self.load_image('Москва'), (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    app = App()
    app.run_app()
