from controller import Controller

#
# def load(fd):
#     items = {}
#     for line in fd.readlines():
#         item = {}
#         new_line = line[len('    put('):-4]
#         code, latitude, longitude = map(str, new_line.split(','))
#         items[code[1:-1]] = {
#             'latitude': float(latitude[len(' new LatLng('):]),
#             'longitude': float(longitude)
#         }
#     return items
#
# def write(fd, items):
#     for key, value in items.items():
#
#         fd.write("'" + key + "': ")
#         fd.write(str(value))
#         fd.write(',\n')

if __name__ == '__main__':
    controller = Controller()
