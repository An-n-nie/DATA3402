class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x= int(slope * y)
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


class Shape:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.name=""
        
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def area(self):
        pass

    def perimeter(self):
        pass

    def parameter_points(self):
        pass

    def is_inside(self,x,y):
        pass

    def overlap(self,other):
        #use parameter points to see if any point from a shape is in another shape
        self_part=self.parameter_points()
        other_part=other.parameter_points()
        
        for x,y in self_part:
            if other.is_inside(x,y):
                return True

        for x,y in other_part:
            if self.is_inside(x,y):
                return True
        return False

    def paint(self,canvas):
        pass


class Rectangle(Shape):
    def __init__(self,length,width,x,y):
        super().__init__(x,y)
        self.__length=length
        self.__width=width
        self.__x=x
        self.__y=y

    def area(self):
        return self.__length*self.__width 

    def perimeter(self):
        return 2*(self.__length+self.__width)

    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def parameter_points(self):
        points=list()
        points.append((self.__x,self.__y)) # could be, bottom left corner
        points.append((self.__x+self.__length,self.__y)) #bottom right corner
        points.append((self.__x+self.__length,self.__y+self.__width)) #top right corner
        points.append((self.__x,self.__y+self.__width)) # top left corner
        return points 

    def is_inside(self,x,y): 
        # point is inside if it's within x length and y length
        return self.__x <= x <= self.__x+self.__length and self.__y<= y <=self.__y+self.__width

    def paint(self,canvas):
        canvas.v_line(self.__x, self.__y, self.__width) #left line
        canvas.v_line(self.__x, self.__y + self.__length, self.__width) #right line
        canvas.h_line(self.__x, self.__y, self.__length) #bottom line
        canvas.h_line(self.__x + self.__width, self.__y, self.__length) #top line

    def __repr__(self):
        return "Rectangle ("+repr(self.__length)+","+repr(self.__width)+","+repr(self.__x)+","+repr(self.__y)+") "



class Circle(Shape):
    def __init__(self, radius, x, y):
        super().__init__(x,y)
        self.__radius=radius
        self.__x=x
        self.__y=y

    def area(self):
        return self.__radius**2*math.pi
        
    def perimeter(self):
        return self.__radius*2*math.pi

    def get_radius(self):
        return self.__radius

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def parameter_points(self):
        points=list()
        for i in range(16): #use different angles to obatin x,y coordinates
            angle=( 2*math.pi/16) * i
            x_point=self.__x + self.__radius * math.cos(angle)
            y_point=self.__y +self.__radius * math.sin(angle)
            points.append((x_point,y_point))
        return points 

    def is_inside(self,x,y): # point is inside if distance from point to circle is less than radius
        test_point_distance= math.sqrt((x - self.__x )**2 + (y - self.__y)**2)
        return test_point_distance < self.__radius

    def paint(self,canvas):
        # use parameter points to paint circle shape
        p=self.parameter_points()
        for x,y in p:
            canvas.set_pixel(int(x),int(y))

    def __repr__(self):
        return "Circle ("+repr(self.__radius)+","+repr(self.__x)+","+repr(self.__y)+") "



class Triangle(Shape):
    def __init__(self,side1,side2,side3,x,y):
        super().__init__(x,y)
        self.__side1=side1
        self.__side2=side2
        self.__side3=side3
        self.__x=x
        self.__y=y

    def area(self): # uses Heron's formula to find area 
        s=(self.__side1+self.__side2+self.__side3)/2
        return math.sqrt(s*(s-self.__side1)*(s-self.__side2)*(s-self.__side3))
    
    def perimeter(self):
        return self.__side1+self.__side2+self.__side3

    def get_x(self):
        return self.__x
        
    def get_y(self):
        return self.__y

    def get_side_lengths(self):
        return self.__side1, self.__side2, self.__side3

    def parameter_points(self):
        vertex1=(self.__x,self.__y)
        vertex2=(self.__x+self.__side3,self.__y)
        
        #use law of cosine to find angle
        angle= (self.__side2**2 + self.__side3**2 - self.__side1**2) / (2*self.__side2*self.__side3)
        angle_in_radian= math.acos(angle)
        
        #use angle to find third vertex
        x_v3=self.__x + self.__side2 * math.cos(angle_in_radian)
        y_v3=self.__y +self.__side2 * math.sin(angle_in_radian)
        vertex3=(x_v3,y_v3)
        
        return [vertex1,vertex2,vertex3]

    
    def is_inside(self,x,y):
        vertex1,vertex2,vertex3=self.parameter_points()
        x1,y1=vertex1
        x2,y2=vertex2
        x3,y3=vertex3

        big_area= abs( x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2) )/2
        
        #find area relative to point x,y
        sub_area1= abs( x*(y2-y3) + x2*(y3-y) + x3*(y-y2) )/2
        sub_area2= abs( x1*(y-y3) + x*(y3-y1) + x3*(y1-y) )/2
        sub_area3= abs( x1*(y2-y) + x2*(y-y1) + x*(y1-y2) )/2

        #find barycentric point
        b1= sub_area1/big_area
        b2= sub_area2/big_area
        b3= sub_area3/big_area

        return (0<=b1<=1) and (0<=b2<=1) and (0<=b3<=1) #points inside triangle   

    def paint(self,canvas):
        p=self.parameter_points()
        for x,y in p:
            canvas.set_pixel(int(x),int(y))

    def __repr__(self):
        return "Triangle ("+repr(self.__side1)+","+repr(self.__side2)+","+repr(self.__side3)+","+repr(self.__x)+","+repr(self.__y)+") "

