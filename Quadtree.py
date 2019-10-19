# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 23:37:47 2019

@author: TTM
"""

import cv2
import numpy as np

image = ""

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node():
    def __init__(self):
        self.top_left = None
        self.bottom_right = None
        self.val = 0
        
        # child nodes
        self.nw_node = None
        self.ne_node = None
        self.sw_node = None
        self.se_node = None

        
class QuadTree():
    def __init__(self, img_height, img_width):
        self.min_pix_count = 64
        self. max_data_count = 20
        self.width = img_width
        self.height = img_height
        
        self.node_list = []
        
    def check_area(self, node, img): #takes 2 points at top left and bottom right corners
        top_left = node.top_left
        bottom_right = node.bottom_right
        
        curr_val = set()
        for x in range(top_left.x, bottom_right.x):
            for y in range(top_left.y, bottom_right.y):
                 curr_val.add(img[y][x])
                 if len(curr_val) > self.max_data_count:
                     return False         

        return True
    
    def draw_boundary(self, node, img):
        for x in range(node.top_left.x, node.bottom_right.x):
            img[node.top_left.y][x] = 0
            img[node.bottom_right.y-1][x] = 0
            
        for y in range(node.top_left.y, node.bottom_right.y):
            img[y][node.top_left.x] = 0
            img[y][node.bottom_right.x-1] = 0
    
    
    def construct(self, img, top_left, bottom_right):
        size = abs((top_left.x - bottom_right.x)*(top_left.y - bottom_right.y))
        new_node = Node()
        
        new_node.bottom_right = bottom_right
        new_node.top_left = top_left
        self.node_list.append(new_node)
        
        if not self.check_area(new_node, img) and size >= self.min_pix_count:
            mid_x = (bottom_right.x + top_left.x) // 2
            mid_y = (bottom_right.y + top_left.y) // 2
            
            new_node.nw_node = self.construct(img, Point(top_left.x, top_left.y), Point(mid_x, mid_y))
            new_node.sw_node = self.construct(img, Point(top_left.x, mid_y), Point(mid_x, bottom_right.y))
            new_node.ne_node = self.construct(img, Point(mid_x, top_left.y), Point(bottom_right.x, mid_y))
            new_node.se_node = self.construct(img, Point(mid_x, mid_y), Point(bottom_right.x, bottom_right.y))    
 
        if size <= self.min_pix_count:
            col = {}
            for x in range(top_left.x, bottom_right.x):
                for y in range(top_left.y, bottom_right.y):
                    if str(img[y][x]) not in col.keys():
                        col[str(img[y][x])] = 0
                        
                    col[str(img[y][x])] += 1
            
            v = list(col.values())
            new_node.val = list(col.keys())[v.index(max(v))]
            for x in range(top_left.x, bottom_right.x):
                for y in range(top_left.y, bottom_right.y):
                    img[y][x] = new_node.val           
                    
    
img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
height, width = img.shape

new_node = Node()
new_node.top_left = Point(0,0)
new_node.bottom_right = Point(width, height)

qt = QuadTree(height, width)
qt.construct(img, new_node.top_left, new_node.bottom_right)

for i in qt.node_list:
    qt.draw_boundary(i, img)

cv2.imwrite("qt_test.png", img)
    
        
        
        
        
    
    

    
    