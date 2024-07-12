from manim import *
#scence is made by 14 * 8 squares 


class FrequencyBezierVisualization(Scene):
    def construct(self):
        rect1 = Rectangle(height=0.5, width=0.5, fill_opacity=1).shift(LEFT*5 + DOWN*3)
        rect2 = Rectangle(height=0.5, width=0.5, fill_opacity=1).move_to(RIGHT*5 + UP*3)
        
        # Initialize r as an empty list to store rectangles
        r = []
        for i in range(5):
            # Create a new rectangle and add it to the list
            r.append(Rectangle(height=0.5, width=0.5, fill_opacity=1))
        
        group = VGroup(*r)
        group.arrange(RIGHT, buff=0.5)
        group.set_color_by_gradient(RED, ORANGE, YELLOW_C, GREEN_D, BLUE)
        

        c = NumberPlane().add_coordinates()
        self.play(Write(c))
        self.play(rect1.animate.move_to(ORIGIN),rect2.animate.move_to(ORIGIN))
        
        
        s1=SurroundingRectangle(group,color=WHITE)
        s2=SurroundingRectangle(s1,color=WHITE)
        group2=VGroup(rect1, rect2)
        self.play(ReplacementTransform(group2, group), Write(s1), Write(s2))
        self.wait(2)