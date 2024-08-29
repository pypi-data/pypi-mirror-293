import time

from tqdm import tqdm
import concurrent.futures
import mysql.connector

from speedy.fake.dates import get_HMS
from speedy.fake.security_log_rows import SecurityLogRows
from speedy.services.config_service import config
class SecurityLogsService(): 

    workers: [] # type: ignore
    count: int = 0
            
    def fmt_workers(workers):
        output = ''.join('O' if worker['running'] else ' ' for worker in workers)
        count = sum(worker['running'] for worker in workers)
        inserted = sum(worker['rows_inserted'] for worker in workers)
        return f"{output} {count:3} {inserted}"   


    def my_callback(self, future):
        worker_id = future.result()
        self.workers[worker_id]['running'] = False
        self.workers[worker_id]['count'] += 1  
        self.workers[worker_id]['rows_inserted'] += self.batch_size 
        #to do: increment by the real rows inserted

        
    def insert_rows(self, worker_id: int, query: str, data):
        with mysql.connector.connect(**self.db_config) as cnx:
            cursor = cnx.cursor()
            cursor.executemany(query, data)
            cnx.commit()
        return worker_id


    def show_count_all(self):
        print("Counting rows in security_logs...")
        with mysql.connector.connect(**self.db_config) as cnx:
            cursor = cnx.cursor()
            query = ("select count(*) from security_logs;")
            cursor.execute(query)
            # Fetch the count result
            count_result = cursor.fetchone()[0]
            
            # Close the cursor and connection
            cursor.close()
        print(f"\033[FRows in security_logs: { count_result :,}       ")

        return count_result


    def setup_db_config(self):
        # Database configuration
        self.db_config = {
            'user': config.db_user,
            'password': config.db_password,
            'host': config.db_host,
            'database': config.db_database,
            'raise_on_warnings': True
        }

    def create_tqdms(self,):        
        main_pbar = tqdm(
            total=self.goal, 
            desc='Inserting fake rows',
            unit='K', 
            leave=True,
            position=0, 
            unit_scale=True, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]'
        )
        
        buffer_pbar = tqdm(
            total=self.buffer_size, 
            desc='Buffer of fake rows', 
            leave=True,
            position=1, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} '
        )

        return main_pbar, buffer_pbar


    def create_fast_copy_tqdms(self,):        
        main_pbar = tqdm(
            total=self.goal, 
            desc='Rows  inserted',
            unit='K', 
            leave=True,
            position=0, 
            unit_scale=True, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]'
        )
        
        buffer_pbar = tqdm(
            total=self.buffer_size * 2, 
            desc='Buffer of rows', 
            leave=True,
            position=1, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} '
        )

        return main_pbar, buffer_pbar
    
    
    def initialize_workers(self):
        # Initialize the workers
        self.workers = [{'id': i, 'future': None, 'running': False, 'count': 0, 'rows_inserted': 0} for i in range(self.num_workers)]
        
        
    def execute_fake_rows(self):
        self.setup_db_config()

        # Number of workers and batch size
        self.num_workers = config.sl_num_workers
        self.batch_size = config.sl_batch_size
        self.buffer_size = config.sl_buffer_size
        self.goal = config.sl_goal

        print (f"Batch size: {self.batch_size}  num workers: {self.num_workers}  goal: {self.goal}")
        
        rows_at_start = self.show_count_all()

        main_pbar, buffer_pbar = self.create_tqdms()

        securityLogRows = SecurityLogRows()
        securityLogRows.init_fake_rows(self.goal, self.batch_size, self.buffer_size, buffer_pbar)  

        self.initialize_workers()
        start_time = time.time()        

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            continue_loop = True

            while continue_loop:
                for worker_id, worker in enumerate(self.workers):
                    if not worker['running']:
                        batch_of_rows = securityLogRows.get_batch_of_rows()
                        query_inserts = securityLogRows.multipleInserts()
                        if batch_of_rows is None:
                            continue_loop = False
                        else:
                            worker['running'] = True
                            future = executor.submit(self.insert_rows, worker_id, query_inserts, batch_of_rows)
                            future.add_done_callback(self.my_callback)
                            worker['future'] = future 
                            main_pbar.update(self.batch_size)

        # wait until all workers completed
        while True:
            # Check if any workers are still running
            if any(worker['running'] for worker in self.workers):            
                time.sleep(1)
            else:
                break
                
        main_pbar.close()
        buffer_pbar.close()
        completed = sum(worker['rows_inserted'] for worker in self.workers)
        print (f"\nReach goal {completed}")
            #for worker in workers:
            #    print(f"{ worker['id']} {worker['count']}     {worker['rows_inserted']} ")


        end_time = time.time()
        execution_time = end_time - start_time
        print(f"The process took { get_HMS(execution_time)} to execute.")
        rows_at_end = self.show_count_all()
        print(f"Rows inserted: { (rows_at_end - rows_at_start):,}")


    def execute_fast_copy(self):
        self.setup_db_config()

        # Number of workers and batch size
        self.num_workers = config.sl_num_workers
        self.batch_size = config.sl_batch_size
        self.buffer_size = config.sl_buffer_size
        self.goal = config.sl_goal

        print (f"goal: {self.goal}  Batch size: {self.batch_size}  Buffer size: {self.buffer_size}  num workers: {self.num_workers}")
        
        starting_row = 500
        end_row = starting_row + self.goal

        #rows_at_start = self.show_count_all()
        rows_at_start = starting_row
        main_pbar, buffer_pbar = self.create_fast_copy_tqdms()
    
        securityLogRows = SecurityLogRows()
        
        securityLogRows.fast_copy_init(self.goal, self.batch_size, self.buffer_size, buffer_pbar, starting_row)  
        
        self.initialize_workers()
        start_time = time.time()        

        while securityLogRows.get_last_delivered_row() < securityLogRows.goal_row:
            batch_of_rows = securityLogRows.get_batch_of_read_rows()
            if batch_of_rows: 
                main_pbar.update(len(batch_of_rows) )
                main_pbar.refresh()
            time.sleep(0.05)
        
        # wait until all workers completed
        time.sleep(2)
        while True:
            # Check if any workers are still running
            if any(worker['running'] for worker in self.workers):            
                time.sleep(0.5)
            else:
                break

        main_pbar.close()
        buffer_pbar.close()
        time.sleep(0.5)
                    
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\nThe process took { get_HMS(execution_time)} to execute.")
        rows_at_end = securityLogRows.get_last_delivered_row() # self.show_count_all()
        print(f"Rows inserted: { (rows_at_end - rows_at_start):,}")
        return
     
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            continue_loop = True

            while continue_loop:
                part_start_time = time.time()
                not_running = False
                for worker_id, worker in enumerate(self.workers):
                    if not worker['running']:
                        not_running = True
                        batch_of_rows = securityLogRows.get_batch_of_rows()
                        query_inserts = securityLogRows.multipleInserts()
                        if batch_of_rows is None:
                            continue_loop = False
                        else:
                            worker['running'] = True
                            future = executor.submit(self.insert_rows, worker_id, query_inserts, batch_of_rows)
                            future.add_done_callback(self.my_callback)
                            worker['future'] = future 
                            main_pbar.update(self.batch_size)
                #if not_running:
                #   print (f"= {fmt_workers(workers)}")

        # wait until all workers completed
        while True:
            # Check if any workers are still running
            if any(worker['running'] for worker in self.workers):            
                time.sleep(1)
            else:
                break
                
        main_pbar.close()
        buffer_pbar.close()
        completed = sum(worker['rows_inserted'] for worker in self.workers)
        print (f"\nReach goal {completed}")
            #for worker in workers:
            #    print(f"{ worker['id']} {worker['count']}     {worker['rows_inserted']} ")


        end_time = time.time()
        execution_time = end_time - start_time
        print(f"The process took { get_HMS(execution_time)} to execute.")
        rows_at_end = self.show_count_all()
        print(f"Rows inserted: { (rows_at_end - rows_at_start):,}")



    def show_count_all_prt(self):
        print("Counting rows in process_request_token...")
        with mysql.connector.connect(**self.db_config) as cnx:
            cursor = cnx.cursor()
            query = ("select count(*) from process_request_tokens;")
            cursor.execute(query)
            # Fetch the count result
            count_result = cursor.fetchone()[0]
            
            # Close the cursor and connection
            cursor.close()
        print(f"\033[FRows in process_request_tokens: { count_result :,}       ")

        return count_result


    def execute_queue_prt_copy(self):
        print ("\n\n\n\n")
        self.setup_db_config()
        row_index = 59000
        batch_size = 1000
        total_delay = 0
                        
        count_prt = self.show_count_all_prt()
        batches = int (count_prt/ batch_size)
        print (f"Number of batches: {batches}")
                                
        print("Processing records from process_request_tokens...\n")
        main_pbar = tqdm(
            total=count_prt, 
            desc='rows in PRT table',
            leave=True,
            position=0, 
            unit_scale=True, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]'
        )
        updates_pbar = tqdm(
            total=count_prt, 
            desc='updates INTEMBEKO',
            leave=True,
            position=1, 
            unit_scale=True, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]'
        )
        delay_pbar = tqdm(
            total=total_delay, 
            desc='delay (seconds)',
            leave=True,
            position=2, 
            unit_scale=True, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]'
        )

        try:
            with mysql.connector.connect(**self.db_config) as cnx:
        
                for i in range(batches):
                    cursor = cnx.cursor(dictionary=True)
                    query = f"SELECT * FROM process_request_tokens limit {row_index}, {batch_size} ;"
                    cursor.execute(query)

                    rows = cursor.fetchall()
                    insert_count = 0
                    
                    for row in rows:
                        if row['process_id'] == 23 and row['element_type'] == 'task':
                            insert_query = """
                                INSERT INTO intembeko_data (user_id, process_id, process_request_id, element_id, element_type, element_name, status, completed_at, initiated_at, created_at, updated_at)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            cursor.execute(insert_query, (
                                row['user_id'], row['process_id'], row['process_request_id'], row['element_id'], row['element_type'], 
                                row['element_name'], row['status'], row['completed_at'], row['initiated_at'], row['created_at'], row['updated_at']
                            ))
                            insert_count += 1
                            cnx.commit()
                            updates_pbar.update(1)
                            updates_pbar.refresh()

                        row_index += 1
                        main_pbar.update(1)
                        main_pbar.refresh()
                        #print (f"  {row_index} {insert_count} ")
                    
                    for d in range(total_delay):
                        time.sleep(1)
                        delay_pbar.n = d
                        delay_pbar.refresh()
                            
            cursor.close()

            print(f"Inserted {insert_count} rows into intembeko_data.")
            return True, None

        except mysql.connector.Error as err:
            print (str(err))
            return False, str(err)
        return
     
   