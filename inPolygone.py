
# def inPolygon(polygon, point):
#     counter = 0
#     x_inters = 0
#     p1 = [0,0]
#     p2 = [0,0]
#     p1 = polygon[0]
#     N = len(polygon)

#     for i in range(1, N):
#         p2 = polygon[i % N]
#         if point[1] > min(p1[1], p2[1]):
            
#             if point[1] <= max(p1[1], p2[1]):
                
#                 if point[0] <= max(p1[0], p2[0]):
                    
#                     if p1[1] != p2.y:
#                         x_inters = (point[1] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
#                         if (p1[0] == p2[0] or point[0] <= x_inters):
#                             counter += 1
#         p1 = p2

#     if (counter % 2 == 0):
#         return "outside"
#     else:
#         return "inside"

# print(inPolygon(polygon=polygone, point=[46.804405748929035, -71.25646591858953]))

