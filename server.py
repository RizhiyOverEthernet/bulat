from utils import database
from concurrent import futures
import grpc
import bulat_pb2 as pb2
import bulat_pb2_grpc as pb2_grpc


class TransactionServer(pb2_grpc.TransactionServerServicer):
    """
    Класс, описывающий методы взаимодействия с сервером
    """

    def sum_amount(self, request, context):
        """
        Функция, которая находит сумму операций по
        фильтру времени и пользователя
        """

        user_id = request.user_id
        start_time = request.start_time
        end_time = request.end_time
        sql_string = f"""
        SELECT 
        SUM(amount) 
        FROM 
        bulat_transactions
        WHERE 
        user_id = {user_id} 
        AND 
        timestamp >= {start_time}
        AND 
        timestamp <= {end_time}"""

        total_amount = database(sql_string)[0]
        return pb2.SumAmountResponse(total_amount=total_amount)


def serve():
    """
    Функция запуска сервера. В идеале работает в формате демона
    """

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_TransactionServerServicer_to_server(TransactionServer(), server)
    server.add_insecure_port('127.0.0.1:50053')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
