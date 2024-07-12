from manim import *
#scence is made by 14 * 8 squares 


class FrequencyBezierVisualization(Scene):
    def construct(self):
        rect1=Rectangle(height=0.5, width=0.5,fill_opacity=1).shift(LEFT*5,DOWN*3)
        rect2=Rectangle(height=0.5, width=0.5,fill_opacity=1).move_to(RIGHT*5,UP*3)
        
        c= NumberPlane().add_coordinates()
        self.play(Write(c))
        self.play(Write(rect1))
        self.play(Write(rect2))
        
        self.wait(3)
