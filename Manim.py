from manim import *
#scene is made by 14 * 8 squares 


class FrequencyBezierVisualization(Scene):
    def construct(self):
        # Load and position the background image
        #background_image = ImageMobject("C:/Users/Youssef/PYvscode/channels4_banner").move_to(ORIGIN)
        #background_image.scale_to_fit_height(43)  
        #background_image.scale_to_fit_width(20)  


        #self.add(background_image)  
        Flags = ImageMobject("C:/Users/Youssef/PYvscode/Design-Keffiyeh-Pattern-Vector-90deg_crop")
        Flags_pos=Flags.get_center()
        Flags.move_to(Flags_pos+LEFT*6.3)
        #Flags.stretch_to_fit_width(0.01)
        Flags.height=8
        #self.add(Flags)

        #Flags2= ImageMobject("C:/Users/Youssef/PYvscode/flags(EGYPT and SUDAN)").next_to(ORIGIN,DOWN,buff=1)      
        # Scale the flags to 0 (invisible)
        #self.add(Flags.scale_to_fit_width(10 ).scale_to_fit_height(23))
        #Flags2.scale_to_fit_height(0.001)
        #Flags2.scale_to_fit_width(0.001)
        #Flags.set_opacity(0.7)
        #Flags2.set_opacity(0.7)
        # Animate scaling up the flags to the desired size




        # Define and position text elements
        eece = Text("EECE", font="Formata", font_size=66, color=WHITE)
        eece26 = Text("2026", font="Formata", font_size=40,color=BLUE_E).next_to(eece,DOWN)
     

        #eece26.set_color_by_gradient(RED, BLACK, WHITE, GREEN)  
        logo_group = Group(eece, eece26).move_to(ORIGIN)
        c = Circle(color=WHITE, radius=0.75).move_to(ORIGIN)
        c.surround(logo_group)
        logo_group.arrange(DOWN, buff=0.5)

        # Create nodes and resistors
        node1_1 = Node(location=LEFT * 1.2 + UP * 1.3)
        node1_2 = Node(location=RIGHT * 1.2+ UP * 1.3)
        node2_1= Node(location=LEFT * 1.2 + DOWN * 1.3)
        node2_2= Node(location=RIGHT * 1.2 + DOWN * 1.3)
        #resistor1 = Resistor(node1_1, node1_2)
        #resistor2 = Resistor(node2_1, node2_2)
        #RES_GROUP = Group(resistor1, resistor2, node1_1, node1_2, node2_1, node2_2)
        
        # Add the elements to the scene
        #self.play(AnimationGroup(*[GrowFromCenter(obj) for obj in RES_GROUP]), run_time=0.65)
        self.play(Write(eece), run_time=0.85)
        self.play(Write(eece26),Write(c), run_time=0.85)
        #self.play(Indicate(eece),runn_time=0.5)        
        group = Group(logo_group, c)
        self.play(group.animate.move_to(RIGHT * config.frame_width / 2.35 + DOWN * config.frame_height / 2.5).scale(0.35), run_time=1)
        #subject=Text("Integerated  Circuits \n Lecture #1", font="sans", font_size=35, color=WHITE).next_to(resistor1,DOWN,buff=0.5)
       # self.play(ReplacementTransform(logo_group,subject), run_time=1)
       # self.wait(0.5)


        # Transform the group to a dot and scale it
        #d = Dot()
        #self.play(ReplacementTransform(group, d), run_time=0.75)
        #self.play(d.animate.scale(150),run_time=0.75)
        
        # Remove the background image and fade out the dot
        #self.remove(background_image)


        #self.play(FadeOut(d, fade_factor=0.8))
        massage= MarkupText("لا تعتاد,لا تنسي,\n لا تتوقف عن الدعاء لاخوتنا", font="Lateef", font_size=55, color=WHITE).move_to(ORIGIN)
        #self.play(GrowFromCenter(Flags),run_time=0.75)
        self.play(FadeIn(Flags, run_time=0.75), Write(massage, run_time=1.5))
        self.play(FadeOut(Flags),FadeOut(massage),FadeOut(group),run_time=1.5)
        self.wait(0.2)
        self.remove(Flags,massage)
        



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
    def __init__(self, node_drain, node_source, node_gate, color=WHITE, line_length=1, gap=0.2, **kwargs):
        # node_drain: Drain, node_source: Source, node_gate: Gate
        center = (node_drain.get_center() + node_source.get_center()) / 2
        drain = Line(node_drain.get_center(), center + DOWN * gap, color=color)
        source = Line(center + UP * gap, node_source.get_center(), color=color)
        
        center_gate_center = (node_gate.get_center() + center) / 2
        gate = Line(node_gate.get_center(), center_gate_center, color=color)

        # Arrow for n-channel MOSFET
        arrow = Arrow(center + UP * gap, center + DOWN * gap, buff=0, color=color, stroke_width=2).scale(0.5)

        # Create the MOSFET structure
        super().__init__(drain, source, gate, arrow, **kwargs)
        self.node_drain = node_drain
        self.node_source = node_source
        self.node_gate = node_gate

