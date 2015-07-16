import pygame as pg

import prepare
import tools

class Camera:
	"""docstring for camera"""
	def __init__(self, (x, y), (w, h)):

		self.rect = pg.Rect(x, y, w, h)
		self.w = w
		self.h = h

	def update(self, player):
		self.rect.center = player.rect.center
		diff_x = prepare.SCREEN_SIZE[0] - self.w
		diff_y = prepare.SCREEN_SIZE[1] - self.h
		if self.rect.x < 0:
			self.rect.x = 0
		elif self.rect.x > diff_x:
			self.rect.x = diff_x

		if self.rect.y < 0:
			self.rect.y = 0
		elif self.rect.y > diff_y:
			self.rect.y = diff_y

	def render(self, surface):
		pg.draw.rect(surface, (255, 0, 0), self.rect, 1)
		