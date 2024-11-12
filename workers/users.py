# from app.models import Operation, Board, SIM, SubOperation
# from tortoise.expressions import Q

# from datetime import datetime
# import logging, asyncio
# from tortoise.transactions import in_transaction
# from nanoid import generate


# async def update_operation(operation, status):
#     operation.status = status
#     await operation.save()
    
# def generate_random_string_with_datetime(board_name, sim_index):
#     datetime_part = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")  # Get current datetime formatted as a string
#     return f"board: {f'{int(board_name):02d}'} index: {f'{int(sim_index):03d}'} time: {datetime_part}"

# async def post_sub_operation(sim_id, operation_id, board_id, result=None, target_phone_number=None):
#     while True:
#         try:
#             async with in_transaction() as conn:
#                 new_sub_operation = SubOperation(
#                     id=generate(),
#                     record_time=datetime.utcnow(),
#                     target_phone_number=target_phone_number,
#                     result=result,
#                     sim_id=sim_id,
#                     board_id=board_id,
#                     operation_id=operation_id,
#                 )
#                 await new_sub_operation.save(using_db=conn)
#                 return new_sub_operation.id
#         except Exception as e:
#             logging.error(f"Error: {e}")
#             await asyncio.sleep(1)

# async def board_operation_executer(board:Board, operation:Operation):
#     if not operation.sims_num:
#         sims_count = await SIM.filter(board=board.id).count()
#         operation.sims_num = sims_count
#         await operation.save()

#         sims = await SIM.filter(board=board.id).order_by('index').all()
#     else:
#         sims = await SIM.filter(board=board.id).order_by('index').limit(operation.sims_num).all()

#     for index, sim in enumerate(sims):
#         send_token = generate_random_string_with_datetime(board.name, sim.index)
#         try:
#             create_sender_operation_response = await post_sub_operation(sim.id, operation.id, board.id)
#         except Exception as e:
#             logging.error("Failed to create sender operation: %s", str(e))
#             return False

#         start_payload = {"phone_number": sim.number, "target_phone_number": sim.number, "is_test": True}
#         sms_payload = {"base_phone_number": sim.number, "target_phone_number": sim.number, "message": send_token, "is_test": 1}

#         sim_retry = 0
#         sub_op_done = False
#         while sim_retry < 3:
#             try:
#                 sim_op, success, desc = await sim_process(send_token, start_payload, sms_payload)
#                 if sim_op:
#                     print(f"{index + 1}/{len(sims)} {sim.number}: {sim_op}")
#                     await update_sub_operation(create_sender_operation_response, sim_op, success, desc)
#                     sub_op_done = True
#                     break
#             except Exception as e:
#                 sim_retry += 1
#                 logging.error("Failed to sim process: %s", str(e))
#                 await asyncio.sleep(10)
#         if not sub_op_done:
#             await update_sub_operation(create_sender_operation_response, "server down", False)

#     try:
#         await start_sim(f"{base_url}/v2/sims/", {"Authorization": f"Bearer {token}"}, {"phone_number": sim.number, "command": "6"})
#     except Exception as e:
#         logging.error("Failed to off sims on board: %s", str(e))



# async def operation_executer(operation:Operation):
#     if operation.boards:
#         board_ids = operation.boards.split(",")
#         boards = await Board.filter(
#             Q(motherboard_id=operation.motherboard_id) & Q(id__in=board_ids)
#         ).select_related("motherboard").order_by("motherboard__name", "name")
#     else:
#         boards = await Board.filter(
#             Q(motherboard_id=operation.motherboard_id)
#             # & ~Q(status="down")  # Uncomment if you want to filter out "down" status
#         ).select_related("motherboard").order_by("motherboard__name", "name")

#     tasks = []

#     for board in boards:
#         tasks.append(asyncio.create_task(board_operation_executer(board, operation)))
#         await asyncio.sleep(60)

#     await asyncio.gather(*tasks)
#     print(f"operation: {operation.id} done")

#     await update_operation(operation, "done")




# async def fetch_ready_operation():
#     now = datetime.utcnow()
#     operation = await Operation.filter(start_at__lt=now, status="todo").order_by("-start_at").first()
#     if operation:
#         # operation.status = "doing"
#         # await operation.save()
#         return operation


# async def worker():
#     try:
#         operation = await fetch_ready_operation()
#         if operation:
#             asyncio.create_task(operation_executer(operation)) 
#     except Exception as e:
#         logging.error("An error occurred: %s", str(e))


# async def main():
#     while True:
#         try:
#             print("start to get operation")
#             # await worker()
#         except Exception as e:
#             logging.error("An error occurred: %s", str(e))
#         await asyncio.sleep(10)
