"""
Класс для создания анимированной кнопки в виде круга.
Отображает прогресс выполнения и пульсирующую анимацию.
"""

from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.graphics import Color, Ellipse
from utils.constants import COLORS, ANIMATION


class AnimatedCircle(Button):
    """
    Анимированная кнопка в виде круга.
    """
    
    def __init__(self, **kwargs):
        """
        Инициализация анимированного круга.
        
        Args:
            **kwargs: Параметры для Button
        """
        super().__init__(**kwargs)
        
        # Прозрачный фон
        self.background_color = (0, 0, 0, 0)
        
        # Начальный текст
        self.text = "0 %"
        
        # Привязка отрисовки
        self.bind(pos=self._draw, size=self._draw)
        
        # Создание анимации
        self._create_pulse_animation()
        
        # Прогресс (0-100)
        self.progress = 0

    def _create_pulse_animation(self):
        """Создает пульсирующую анимацию текста."""
        anim_up = Animation(
            font_size=ANIMATION['font_size_big'],
            duration=ANIMATION['duration']
        )
        anim_down = Animation(
            font_size=ANIMATION['font_size_small'],
            duration=ANIMATION['duration']
        )
        self.anim = anim_up + anim_down
        self.anim.repeat = True
        self.anim.start(self)

    def _draw(self, *args):
        """
        Отрисовка круга с индикацией прогресса.
        """
        self.canvas.before.clear()
        with self.canvas.before:
            # Базовый круг
            Color(*COLORS['primary'])
            Ellipse(pos=self.pos, size=self.size)
            
            # Индикатор прогресса
            Color(*COLORS['success'])
            filled_height = self.height * (self.progress / 100)
            Ellipse(pos=self.pos, size=(self.width, filled_height))

    def update_progress(self, percent):
        """
        Обновляет отображаемый прогресс.
        
        Args:
            percent (float): Процент выполнения (0-100)
        """
        self.progress = max(0, min(100, percent))
        self.text = f"{int(self.progress)} %"
        self._draw()