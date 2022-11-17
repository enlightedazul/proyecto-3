import grpc
import cyberdog_app_pb2
import cyberdog_app_pb2_grpc

stub = None
cyberdog_ip = None  # Write Your Cyberdog IP Here or Input while running


def BuenPerritoCMD():
    # Open grpc channel
    global cyberdog_ip
    if (cyberdog_ip is None):
        cyberdog_ip = input('Cyberdog Ip:')
    with grpc.insecure_channel(str(cyberdog_ip) + ':50051') as channel:
        print("Wait connect")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            print("Connect error, Timeout")
            return
        # Get stub from channel
        stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)

        # Stand up
        response = stub.setMode(
            cyberdog_app_pb2.CheckoutMode_request(
                next_mode=cyberdog_app_pb2.ModeStamped(
                    header=cyberdog_app_pb2.Header(
                        stamp=cyberdog_app_pb2.Timestamp(
                            sec=0,      # seem not need
                            nanosec=0   # seem not need
                        ),
                        frame_id=""     # seem not need
                    ),
                    mode=cyberdog_app_pb2.Mode(
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.MANUAL,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Stand up, result:' + str(succeed_state))

        # Execute HI_FIVE order
        if (succeed_state == False):
            return
        response = stub.setExtmonOrder(
            cyberdog_app_pb2.ExtMonOrder_Request(
                order=cyberdog_app_pb2.MonOrder(
                    id=cyberdog_app_pb2.MonOrder.MONO_ORDER_HI_FIVE,
                    para=0      # seem not need
                ),
                timeout=50))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute HI_FIVE order, result:' + str(succeed_state))

        # Get down
        if (succeed_state == False):
            return
        response = stub.setMode(
            cyberdog_app_pb2.CheckoutMode_request(
                next_mode=cyberdog_app_pb2.ModeStamped(
                    header=cyberdog_app_pb2.Header(
                        stamp=cyberdog_app_pb2.Timestamp(
                            sec=0,      # seem not need
                            nanosec=0   # seem not need
                        ),
                        frame_id=""     # seem not need
                    ),
                    mode=cyberdog_app_pb2.Mode(
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Get down, result:' + str(succeed_state))


def SendData():
    global stub
    system('clear')
    PrintState()
    stub.sendAppDecision(
        cyberdog_app_pb2.Decissage(
            twist=cyberdog_app_pb2.Twist(
                linear=cyberdog_app_pb2.Vector3(
                    x=linear.x,
                    y=linear.y,
                    z=linear.z
                ),
                angular=cyberdog_app_pb2.Vector3(
                    x=angular.x,
                    y=angular.y,
                    z=angular.z
                )
            )
        )
    )


if __name__ == '__main__':
    while True:
        mod = input('Choose mode [1:BuenPerritoCMD, 2:RunMoveCMD, else:Exit]:')
        print(mod)
        if (mod == '1'):
            BuenPerritoCMD()
        elif (mod == '2'):
            RunMoveCMD()
        else:
            break
