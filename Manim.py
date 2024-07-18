from manim import *
#scene is made by 14 * 8 squares 


class FrequencyBezierVisualization(Scene):
    def construct(self):
        background_image = ImageMobject("C:/Users/Youssef/PYvscode/channels4_banner").move_to(ORIGIN)
        background_image.scale_to_fit_height(32)  # Adjust the scale as needed
        background_image.scale_to_fit_width(16)  # Adjust the scale as needed
        self.add(background_image)  # Add the image to the scene first

        eece=Text("EECE", font="Calibri", font_size=48,color=WHITE).to_edge(UP)
        eece26=Text("2026", font="Calibri", font_size=48,color=WHITE).to_edge(UP)
        logo_group = Group(eece, eece26).move_to(ORIGIN)
        logo_group.arrange(DOWN, buff=0.5)

        node1 = Node(location=LEFT*1)
        node2 = Node(location=RIGHT*1)
        resistor = Resistor(node1, node2)
        RES_GROUP=Group(resistor, node1, node2)
        self.play(AnimationGroup(*[GrowFromCenter(obj) for obj in RES_GROUP]), run_time=0.5)
        
        self.play(ReplacementTransform(RES_GROUP, logo_group), run_time=0.5)

        #cap=Capacitor(node1, node2)
        #CAP_GROUP=Group(cap, node1, node2)
        #self.play(AnimationGroup(*[GrowFromCenter(obj) for obj in CAP_GROUP]))
        #self.play(Transform(RES_GROUP, CAP_GROUP))


        c=Circle(color=WHITE, radius=1).move_to(ORIGIN)
        c.surround(logo_group)
        group=Group(logo_group, c)
        

        
        d=Dot()
        self.play(ReplacementTransform(group, d))
        self.play(d.animate.scale(150))
        self.remove(background_image)
        self.play(FadeOut(d))

        self.wait(0.5)


class CircuitElement(VGroup):
    def __init__(self, *mobjects, **kwargs):
        super().__init__(*mobjects, **kwargs)
    
    def give_label(self, label_tex, label_direction, color=WHITE, scale_value=1, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER):
        self.label = MathTex(label_tex, color=color).scale(scale_value)
        self.label.next_to(self, label_direction, buff=buff)
        self.add(self.label)
        return self
    
class Node(CircuitElement):
    def __init__(self, location, color=YELLOW, **kwargs):
        self.dot = Dot(location, color=color).scale(0.8).set_z_index(1)
        # z_index > 0 ensures it will be drawn on top of wires and other things regardless of scene add order
        super().__init__(self.dot, **kwargs)
    
    def get_center(self): # ensures adding label does not throw off center
        return self.dot.get_center()
class Wire(CircuitElement):
    def __init__(self, node1, node2, color=WHITE, **kwargs):
        line = Line(node1.get_center(), node2.get_center(), buff=0, color=color)
        super().__init__(line, **kwargs)
        self.node1 = node1
        self.node2 = node2
        # I gave all these connectors these node attributes because I thought charges were going to know
        # which connector they were currently traveling through and then use these node endings to decide
        # where to go next. Did not end up using them because instead I told the charges where to go myself.

class Capacitor(CircuitElement):
    def __init__(self, node1, node2, color=WHITE, line_length=1, **kwargs):
        center = (node1.get_center() + node2.get_center())/2
        between_nodes_vector = node1.get_center() - node2.get_center()
        unit_node_distance = between_nodes_vector / np.linalg.norm(between_nodes_vector)
        line1 = Line(center + line_length/2*unit_node_distance, center - line_length/2*unit_node_distance, color=color)
        line1.rotate(PI/2)
        line2 = line1.copy()
        line1.shift(between_nodes_vector/2)
        line2.shift(-between_nodes_vector/2)
        super().__init__(line1, line2, **kwargs)
        self.node1 = node1
        self.node2 = node2

class Resistor(CircuitElement):
     
    # A zigzagging line between two nodes
     def __init__(self, node1, node2, number_of_zigzags=4, eccentricity=1, **kwargs):
        line = Line(node1.get_center(),node2.get_center(),buff=0)
        distance = np.linalg.norm(node1.get_center() - node2.get_center())
        tiny_step = (node1.get_center() - node2.get_center())/(2*number_of_zigzags)
        sideways_step = eccentricity*np.array([-tiny_step[1],tiny_step[0],0])
        zig_points = [
            line.point_from_proportion(i/(2*number_of_zigzags)) + sideways_step
            for i in range(1,2*number_of_zigzags,2)
        ]
        zag_points = [
            line.point_from_proportion(i/(2*number_of_zigzags)) - sideways_step
            for i in range(2,2*number_of_zigzags,2)
        ]
        zigzags = VGroup()
        zigzags.add(Line(node1.get_center(),zig_points[0]))
        for i in range(len(zig_points)-1):
            zigzags.add(Line(zig_points[i], zag_points[i]))
            zigzags.add(Line(zag_points[i], zig_points[i+1]))
        zigzags.add(Line(zig_points[-1], node2.get_center()))
        super().__init__(*zigzags, **kwargs)
        self.node1 = node1
        self.node2 = node2

class MOSFET(CircuitElement):
    def __init__(self, node1, node2, number_of_zigzags=4, eccentricity=1, **kwargs):
        center = (node1.get_center() + node2.get_center())/2
        between_nodes_vector = node1.get_center() - node2.get_center()
        unit_node_distance = between_nodes_vector / np.linalg.norm(between_nodes_vector)
        line1 = Line(center + line_length/2*unit_node_distance, center - line_length/2*unit_node_distance, color=color)
        line1.rotate(PI/2)
        line2 = line1.copy()
        line1.shift(between_nodes_vector/2)
        line2.shift(-between_nodes_vector/2)
        super().__init__(line1, line2, **kwargs)
        self.node1 = node1
        self.node2 = node2