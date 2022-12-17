import colorsys
import socket
import numpy as np

remote_host = "192.168.1.135"
remote_tcp_port = 4242
remote_udp_port = 4243


def rgb_to_bytes(rgb):
    (r, g, b) = rgb
    return round(r * 255), round(g * 255), round(b * 255)


class PicoNeopixel:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, host_ip, num_pixels):
        """
        :param string host_ip: The IP address of the lights.
        :param int num_pixels: The number of LEDs in the light string.
        """
        self.num_pixels = num_pixels
        self.host_ip = host_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print("Connecting...")

        # Connect to the remote host and port
        self.sock.connect((host_ip, remote_tcp_port))

        print("Connected")

        self.__send_byte(10)
        self.__send_arr([self.num_pixels >> 8, self.num_pixels & 0xff])
        if self.sock.recv(1) != b'\x02':
            raise 'Failed to initialise pixels.'
        else:
            print('Successfully initialised! (' + str(num_pixels) + ' pixels)')

        self.pixels = []
        for p in range(num_pixels):
            self.pixels.append((0, 0, 0))

    def __send_arr(self, arr):
        self.sock.send(bytearray(arr))

    def __send_arr_udp(self, arr):
        self.sock_udp.sendto(bytearray(arr), (self.host_ip, remote_udp_port))

    def __send_byte(self, byte):
        self.__send_arr([byte])

    def __send_byte_udp(self, byte):
        self.__send_arr_udp([byte])

    def set_hsv(self, pixel, h, s, v):
        """
        Sets the colour of a pixel to a HSV value.

        Remember to call show() to send all pixel values to the lights.
        :param int pixel: Pixel index
        :param float h: Hue, in range [0, 1]
        :param float s: Saturation, in range [0, 1]
        :param float v: Value, in range [0, 1]
        """
        if pixel > self.num_pixels - 1:
            raise "Provided pixel index (" + str(pixel) + ") is too large (numPixels: " + str(self.num_pixels) + ")."
        if h < 0 or h > 1:
            raise "Hue must be in range [0, 1]"
        if s < 0 or s > 1:
            raise "Saturation must be in range [0, 1]"
        if v < 0 or v > 1:
            raise "Value must be in range [0, 1]"
        self.pixels[pixel] = rgb_to_bytes(colorsys.hsv_to_rgb(h, s, v))

    def set_rgb(self, pixel, r, g, b):
        """
        Sets the colour of a pixel to an RGB value.

        Remember to call show() to send all pixel values to the lights.
        :param int pixel: Pixel index
        :param float r: Red component, in range [0,1]
        :param float g: Green component, in range [0,1]
        :param float b: Blue component, in range [0,1]
        """
        if r < 0 or r > 1:
            raise "Red must be in range [0, 1]"
        if g < 0 or g > 1:
            raise "Green must be in range [0, 1]"
        if b < 0 or b > 1:
            raise "Blue must be in range [0, 1]"
        self.pixels[pixel] = rgb_to_bytes((r, g, b))

    def clear(self):
        """
        Sets all pixel values to off/black (0, 0, 0).

        Remember to call show() to send all pixel values to the lights.
        """
        for p in range(self.num_pixels):
            self.pixels[p] = (0, 0, 0)

    def show(self):
        """
        Send all pixel values to the lights.
        """
        arr = [11]
        for p in self.pixels:
            (r, g, b) = p
            arr.append(r)
            arr.append(g)
            arr.append(b)
        self.__send_arr_udp(arr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()
        self.sock_udp.close()
        print("Disconnected")


#
#
#
# # Create a socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# print("Connecting...")
#
# # Connect to the remote host and port
# sock.connect((remote_host, remote_tcp_port))
#
# print("Connected")
#
#
#
#
# def neo_init(numPixels):
#     send_byte(10)
#     send_arr([numPixels >> 8, numPixels & 0xff])
#
#
# def neo_show(pixels, frame):
#     #send_byte(11)
#     #arr = [12, (frame >> 24) & 0xff, (frame >> 16) & 0xff, (frame >> 8) & 0xff, frame & 0xff]
#     arr = [11]
#     for p in pixels:
#         (r, g, b) = p
#         arr.append(r)
#         arr.append(g)
#         arr.append(b)
#     send_arr_udp(arr)
#     #print('Sent ' + str(arr[1]) + str(arr[2]) + str(arr[3]) + str(arr[4]))
#
#
# num_pixels = 500
#
# neo_init(num_pixels)
# if sock.recv(1) != b'\x02':
#     raise 'Did not receive OK'
# else:
#     print('OK!')
#
# sleep_cs = 3
# # send_arr([11, sleep_cs, 50])
# # if sock.recv(1) != b'\x02':
# #     raise 'Did not receive OK'
# # else:
# #     print('OK!')
#
#
# t = 0
# n = 1
#
# while True:
#     # socket_list = [sock]
#     # # Get the list sockets which are readable
#     # read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
#     # for s in read_sockets:
#     #     # incoming message from remote server
#     #     if sock == s:
#     #         data = sock.recv(4096, socket.MSG_DONTWAIT)
#     #         print(list(data))
#
#     pixels = []
#
#     for p in range(num_pixels):
#         h = t / 3
#         pixels.append(rgb_to_bytes(colorsys.hsv_to_rgb(h, 1, 1)))
#     neo_show(pixels, n)
#     # print(int.from_bytes(sock.recv(1), byteorder="big"))
#     # print(int.from_bytes(sock.recv(4), byteorder="big"))
#     time.sleep(sleep_cs/100)
#     t += sleep_cs/100
#     n += 1
