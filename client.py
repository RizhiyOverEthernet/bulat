import grpc
import bulat_pb2 as pb2
import bulat_pb2_grpc as pb2_grpc
from random import randint
import time


def run(uid, st, et):
    """
    Функция интерфейса для протокола gRPC
    """

    start = time.time()
    with grpc.insecure_channel('127.0.0.1:50053') as channel:
        stub = pb2_grpc.TransactionServerStub(channel)

        request = pb2.SumAmountRequest(
            user_id=int(uid),
            start_time=int(st),
            end_time=int(et)
        )

        response = stub.sum_amount(request)
        total_amount = response.total_amount
        end = time.time()
        return total_amount, (end-start) * 10**3


if __name__ == '__main__':
    time_list = []
    for _ in range(25):
        amount, expire = run(randint(1, 500), randint(161_016_245_5, 171_016_245_5), 171_016_245_5)
        print(amount)
        time_list.append(expire)
    print(f"Среднее время выполнения: {sum(time_list) / len(time_list)}")
